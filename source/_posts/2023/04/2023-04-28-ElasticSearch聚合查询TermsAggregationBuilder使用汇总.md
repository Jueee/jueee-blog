---
title: ElasticSearch聚合查询TermsAggregationBuilder使用汇总
layout: info
commentable: true
date: 2023-04-28
mathjax: true
mermaid: true
tags: [ElasticSearch,Java,JavaClass,Spring]
categories: 
- [Database,ElasticSearch]
- [Java,JavaClass]
description: 
---

整理一些 ElasticSearch 聚合查询的常用操作。

<!--more-->

### 开启聚合

聚合函数可能使用_id字段排序报错：

```
Fielddata access on the _id field is disallowed, updating the dynamic cluster setting: indices.id_field_data.enabled
```

需要请求更新es集群配置：

```
PUT _cluster/settings
{
  "persistent": {
    "indices.id_field_data.enabled": true
  }
}
```

### 普通聚合汇总

1. 构建 BoolQueryBuilder

   ```java
   BoolQueryBuilder bool = new BoolQueryBuilder();
   bool.must(QueryBuilders.rangeQuery("@timestamp").from(start.getTime()));
   bool.must(QueryBuilders.rangeQuery("@timestamp").to(end.getTime()));
   ```

2. 设置分组 TermsAggregationBuilder

   ```java
   TermsAggregationBuilder aggregationBuilderGroupBy = AggregationBuilders.terms("agg_count").field("module.keyword").size(200);
   ```

   - AggregationBuilders.terms 相当于 sql 中的 group by
   - 其中 `terms` 值自定义，`field` 为需要分组的 key

3. 分组查询

   ```java
   SearchSourceBuilder sourceBuilder = new SearchSourceBuilder().trackTotalHits(true).query(bool).aggregation(aggregationBuilderGroupBy);
   SearchRequest searchRequest = new SearchRequest(esIndexName).source(sourceBuilder);
   SearchResponse response = restHighLevelClient.search(searchRequest, RequestOptions.DEFAULT);
   Aggregations aggregations = response.getAggregations();
   ```

4. 获取查询结果

   ```java
   Aggregation sourceType = aggregations.get("agg_count");
   for (Terms.Bucket bucket : ((Terms) sourceType).getBuckets()) {
       logger.info("[LogIndex]"+bucket.getKeyAsString()+"[Count]"+bucket.getDocCount());
   }
   ```

5. 执行结果：

   ```
   [LogIndex]nlp-model[Count]101520
   [LogIndex]web-admin[Count]1106
   ```

### 聚合指标

#### Value Count

值聚合，主要用于统计文档总数，类似SQL的count函数。

```
ValueCountAggregationBuilder valueCountAggregationBuilder = AggregationBuilders.count("orders").field("order_id");
```

#### Cardinality

基数聚合，也是用于统计文档的总数，跟Value Count的区别是，基数聚合会去重，不会统计重复的值，类似SQL的 `count(DISTINCT 字段)` 用法。

```
CardinalityAggregationBuilder cardinalityAggregationBuilder = AggregationBuilders.cardinality("total").field("id");
```

- 基数聚合是一种近似算法，统计的结果会有一定误差，不过性能很好。

#### Sum 求和

```
SumAggregationBuilder sumAggregationBuilder = AggregationBuilders.sum("total_sale").field("price");
```

#### Avg 平均数

```
AvgAggregationBuilder avgAggregationBuilder = AggregationBuilders.avg("avg_price").field("price");
```

#### Max 最大值

```
MaxAggregationBuilder maxAggregationBuilder = AggregationBuilders.max("max_price").field("price");
```

#### Min 最小值

```
MinAggregationBuilder minAggregationBuilder = AggregationBuilders.min("min_price").field("price");
```



### 多字段聚合汇总

```java
LinkedHashMap<String, Long> nameCountMap = new LinkedHashMap<>();
BucketOrder bucketOrder = BucketOrder.count(false); //这里的count方法中true表示升序排列，false代表降序排列

TermsAggregationBuilder aggregationBuilder = AggregationBuilders.terms("groupInfo") //分组名可以随便填，但是必须和后面aggregations.get("${分组名}");里面填的分组名保持一致，否则会返回null，导致后续空指针异常
        .script(new Script("doc['subject.keyword'].value+'_'+doc['senderAccount.keyword'].value")) //相当于group by 4个字段，其中的@@是字段间的分隔符，最后ES返回的结果是这样的${字段1}@@${字段2}@@${字段3}@@${字段4}
        .size(20) //聚合返回20个值（不传默认返回10个值）
        .order(bucketOrder); //将上方的排序填入，让ES进行排序
SearchSourceBuilder sourceBuilder = new SearchSourceBuilder();
sourceBuilder.query(boolQueryBuilder(dataSource, orderByColumn));
sourceBuilder.aggregation(aggregationBuilder); //填入分组信息
SearchRequest searchRequest = new SearchRequest(defaultIndexName());
searchRequest.source(sourceBuilder);
try {
    SearchResponse searchResponse = restHighLevelClient.search(searchRequest, RequestOptions.DEFAULT);
    Aggregations aggregations = searchResponse.getAggregations();
    Terms terms = aggregations.get("groupInfo"); //填入上方terms()中相同的分组名
    for (Terms.Bucket bucket : terms.getBuckets()) {
        String key = bucket.getKeyAsString(); //这里的key值是这样的：${字段1}@@${字段2}@@${字段3}@@${字段4}
        long count = bucket.getDocCount(); //group by后聚合统计出来的数量
        String[] split = key.split("@@"); //切开作为分隔符的@@，取里面需要的字段放入nameCountMap就行了
        nameCountMap.put(split[0], count); //假设取第0个字段作为key
        System.out.println(key + "--" + count);
    }
} catch (IOException e) {
    log.error(e.getMessage(), e);
}
```

注意：

- 如果字段有多个类型，需要指定 keyword。

#### 汇总后拼接字符串

```java
Aggregations aggregations = searchResponse.getAggregations();
Terms terms = aggregations.get("groupInfo"); //填入上方terms()中相同的分组名
for (Terms.Bucket bucket : terms.getBuckets()) {
    String[] splitKey = bucket.getKeyAsString().split("@@");	
    long count = bucket.getDocCount();
}
```

注意：

- 这里的 key 值是这样的：`${字段1}@@${字段2}@@${字段3}@@${字段4}`，切开作为分隔符的@@，取里面需要的字段就行了

### 按索引拼接 IDs 

以下示例是先按 _index 聚合，再按 _id 聚合，最终完成 JSONArray 的拼接。

拼接查询：

```java
TermsAggregationBuilder idAggregation = AggregationBuilders.terms("id").field("_id").size(Integer.MAX_VALUE);
TermsAggregationBuilder indexAggregation = AggregationBuilders.terms("index").field("_index").subAggregation(idAggregation);
aggregationBuilder.subAggregation(indexAggregation);
```

解析查询结果：

```java
Terms indexTerms = bucket.getAggregations().get("index");
for (Terms.Bucket indexBucket : indexTerms.getBuckets()) {
    JSONArray idArray = new JSONArray();
    Terms idTerms = indexBucket.getAggregations().get("id");
    for (Terms.Bucket bucketId : idTerms.getBuckets()) {
        idArray.add(bucketId.getKeyAsString());
    }
    JSONObject jsonObject = new JSONObject();
    jsonObject.put("index", indexBucket.getKeyAsString());
    jsonObject.put("ids", idArray);
    jsonArray.add(jsonObject);
}
feature.setIds(jsonArray.toString());
```

### having 过滤聚合查询

```java
Map<String, String> bucketsPathsMap = new HashMap<>();
bucketsPathsMap.put("counts", "_count");
BucketSelectorPipelineAggregationBuilder havingBucketSelector =
        PipelineAggregatorBuilders.bucketSelector("having", bucketsPathsMap, new Script("params.counts>1"));
```

拼接过滤条件：

```java
TermsAggregationBuilder aggregationBuilder = AggregationBuilders.terms("groupInfo")
        .script(new Script(groupKey)) 
        .subAggregation(havingBucketSelector);
```