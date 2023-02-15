---
title: RestHighLevelClient使用es中三种查询用法
layout: info
commentable: true
date: 2022-11-04
mathjax: true
mermaid: true
tags: [Database,ElasticSearch]
categories: [Database,ElasticSearch]
description: 
---

### 三种查询用法

三者之间的区别

#### from size

- 深度分页或者size特别大的情况，会出现deep pagination问题。且es的自保机制max_result_window是10000，当查询数量超过一万就会报错
- 该查询的实现原理类似于mysql中的limit，比如查询第10001条数据，那么需要将前面的1000条都拿出来，进行过滤，最终才得到数据。（性能较差，实现简单，适用于少量数据）

#### search after

- search_after缺点是不能够随机跳转分页，只能是一页一页的向后翻（当有新数据进来，也能实时查询到），并且需要至少指定一个唯一不重复字段来排序（一般是_id和时间字段）
- 当使用search_after时，from值必须设置为0或者-1
- 可以查询10000条以上数据

#### scroll

- 高效进行滚动查询，首次查询会在内存中保存一个历史快照以及游标（scroll_id）,记录当前消息查询的终止位置，下次查询的时候将基于游标进行消费（性能良好，不具备实时性，一般是用于大量数据导出或者索引重建）
- 可以查询10000条以上数据

### from size 示例

```java
public void testSearch(String indexName,String orderName) throws IOException {
    long startTime = System.currentTimeMillis();
    // 1、创建searchRequest
    SearchRequest searchRequest = new SearchRequest(indexName);
    // 2、指定查询条件
    SearchSourceBuilder sourceBuilder = new SearchSourceBuilder();//必须加上track_total_hits，不然就只显示10000
    // 页面上的第一页等同于在es中的 0
    sourceBuilder.from(0);
    // 每页多少条数据
    sourceBuilder.size(100);
    // 设置唯一排序值定位
    sourceBuilder.sort(SortBuilders.fieldSort(orderName).order(SortOrder.DESC));
    //将sourceBuilder对象添加到搜索请求中
    searchRequest.source(sourceBuilder);
    // 发送请求
    SearchResponse searchResponse = esClient.search(searchRequest, RequestOptions.DEFAULT);
    SearchHit[] hits = searchResponse.getHits().getHits();
    List<Map<String, Object>> result = new ArrayList<>();
    if (hits != null && hits.length > 0) {
        for (SearchHit hit : hits) {
            // 获取需要数据
            Map<String, Object> sourceAsMap = hit.getSourceAsMap();
            result.add(sourceAsMap);
        }
    }
    logger.info("查询出来的数据个数为：{}", result.size());
    // 关闭客户端
    esClient.close();
    logger.info("运行时间: " + (System.currentTimeMillis() - startTime) + "ms");
}
```

如果from size 查询的数据超过10000条，会报错误：

```
Elasticsearch exception [type=search_phase_execution_exception, reason=all shards failed]

Result window is too large, from + size must be less than or equal to: [10000] but was [10030]. See the scroll api for a more efficient way to request large data sets. This limit can be set by changing the [index.max_result_window] index level setting.
```

### search after 示例

```java
public void testSearch(String indexName,String orderName) throws IOException {
    long startTime = System.currentTimeMillis();
    // 1、创建searchRequest
    SearchRequest searchRequest = new SearchRequest(indexName);
    // 2、指定查询条件
    SearchSourceBuilder sourceBuilder = new SearchSourceBuilder().trackTotalHits(true);//必须加上track_total_hits，不然就只显示10000
    //设置每页查询的数据个数
    sourceBuilder.size(1000);
    // 设置唯一排序值定位
    sourceBuilder.sort(SortBuilders.fieldSort(orderName).order(SortOrder.DESC));//多条件查询
    //将sourceBuilder对象添加到搜索请求中
    searchRequest.source(sourceBuilder);
    // 发送请求
    SearchResponse searchResponse = esClient.search(searchRequest, RequestOptions.DEFAULT);
    SearchHit[] hits1 = searchResponse.getHits().getHits();
    List<Map<String, Object>> result = new ArrayList<>();
    if (hits1 != null && hits1.length > 0) {
        do {
            for (SearchHit hit : hits1) {
                // 获取需要数据
                Map<String, Object> sourceAsMap = hit.getSourceAsMap();
                result.add(sourceAsMap);
            }
            // 取得最后得排序值sort，用于记录下次将从这个地方开始取数
            SearchHit[] hits = searchResponse.getHits().getHits();
            Object[] lastNum = hits[hits.length - 1].getSortValues();
            // 设置searchAfter的最后一个排序值
            sourceBuilder.searchAfter(lastNum);
            searchRequest.source(sourceBuilder);
            // 进行下次查询
            searchResponse = esClient.search(searchRequest, RequestOptions.DEFAULT);
        } while (searchResponse.getHits().getHits().length != 0);
    }
    logger.info("查询出来的数据个数为：{}", result.size());
    // 关闭客户端
    esClient.close();
    logger.info("运行时间: " + (System.currentTimeMillis() - startTime) + "ms");
}
```

### scroll 示例

```java
public void testSearch(String indexName,String orderName) throws IOException {
    long startTime = System.currentTimeMillis();
    // 1、创建searchRequest
    SearchRequest searchRequest = new SearchRequest(indexName);
    // 2、指定scroll信息
    searchRequest.scroll(TimeValue.timeValueMinutes(1L));
    // 3、指定查询条件
    SearchSourceBuilder searchSourceBuilder = new SearchSourceBuilder();
    searchSourceBuilder.size(1000);
    searchSourceBuilder.sort(SortBuilders.fieldSort(orderName).order(SortOrder.DESC));//多条件查询
    searchRequest.source(searchSourceBuilder);
    //4、获取返回结果scrollId，source
    SearchResponse searchResponse = esClient.search(searchRequest, RequestOptions.DEFAULT); //通过发送初始搜索请求来初始化搜索上下文
    String scrollId = searchResponse.getScrollId();
    SearchHit[] searchHits = searchResponse.getHits().getHits();
    List<Map<String, Object>> result = new ArrayList<>();
    for (SearchHit hit: searchHits) {
        result.add(hit.getSourceAsMap());
    }
    // java也是一样要查询两次，先把我们的首页给查询出来
    // 查询出来之后我们要获取他的id
    // 然后利用他的id去查询他的下一页
    while (true) {
        //5、循环  -  创建 SearchScrollRequest  创建一个新的搜索滚动请求，保存最后返回的滚动标识符和滚动间隔
        // 获取 scrollId 去查询下一页
        SearchScrollRequest scrollRequest = new SearchScrollRequest(scrollId);
        //6、指定scrollId的生存时间
        scrollRequest.scroll(TimeValue.timeValueMinutes(1L));
        //7、执行查询获取返回结果
        SearchResponse scrollResp = esClient.scroll(scrollRequest, RequestOptions.DEFAULT);
        //8、判断是否查询到了数据，输出
        SearchHit[] hits = scrollResp.getHits().getHits();
        //循环输出下一页
        if (hits != null && hits.length > 0) {
            for (SearchHit hit : hits) {
                result.add(hit.getSourceAsMap());
            }
        } else {
            //9、判断没有查询到数据，退出循环
            break;
        }
    }
    //查完之后我们把存进缓存的id给删除  完成滚动后，清除滚动上下文
    //10、创建ClearScrollRequest
    ClearScrollRequest clearScrollRequest = new ClearScrollRequest();
    //11、指定scrollId
    clearScrollRequest.addScrollId(scrollId);
    //12、删除scrollId
    ClearScrollResponse clearScrollResponse = esClient.clearScroll(clearScrollRequest, RequestOptions.DEFAULT);
    //13、输出结果
    boolean succeeded = clearScrollResponse.isSucceeded();
    logger.info("删除scrollId：{}", succeeded);
    logger.info("查询总个数：{}", result.size());
    // 关闭客户端
    esClient.close();
    logger.info("运行时间: " + (System.currentTimeMillis() - startTime) + "ms");
}
```
