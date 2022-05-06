---
title: ElasticSearch集成Spring之ElasticsearchRestTemplate示例
layout: info
commentable: true
date: 2021-02-07
mathjax: true
mermaid: true
tags: [Database,ElasticSearch]
categories: [Database,ElasticSearch]
description: 
---

### ElasticsearchRestTemplate

ElasticsearchRestTemplate是spring-data-elasticsearch项目中的一个类，和其他spring项目中的template类似。

#### 引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-elasticsearch</artifactId>
</dependency>
```

<!--more-->

### 使用ElasticsearchRest

1. 参数配置：

   ```properties
   elasticsearch.address=127.0.0.1:9200
   ```

2. 配置引入：

   ```java
   import org.elasticsearch.client.RestHighLevelClient;
   import org.springframework.beans.factory.annotation.Value;
   import org.springframework.context.annotation.Bean;
   import org.springframework.context.annotation.Configuration;
   import org.springframework.data.elasticsearch.client.ClientConfiguration;
   import org.springframework.data.elasticsearch.client.RestClients;
   import org.springframework.data.elasticsearch.core.ElasticsearchRestTemplate;
   
   @Configuration
   public class ElasticSearchConfig {
   
       @Value("${elasticsearch.address}")
       private String elasticSearchAddress;
   
       @Bean
       RestHighLevelClient elasticsearchClient() {
           final ClientConfiguration configuration = ClientConfiguration.builder()
                   .connectedTo(elasticSearchAddress)
                   .build();
           RestHighLevelClient client = RestClients.create(configuration).rest();
           return client;
       }
   
       @Bean
       ElasticsearchRestTemplate elasticsearchTemplate() {
           return new ElasticsearchRestTemplate(elasticsearchClient());
       }
   }
   ```

3. 使用：

   ```java
   @Autowired
   ElasticsearchRestTemplate elasticsearchTemplate;
   ```

### 常用示例

#### 索引相关

创建索引：

```java
Map<String, Object> settings = new HashMap<>();
settings.put("index.number_of_replicas", "30");
boolean createResult = elasticsearchTemplate.createIndex(clazz,settings);
```

刷新Mapping：

```java
elasticsearchTemplate.putMapping(clazz);
elasticsearchTemplate.refresh(clazz);
```

#### 新增数据

```java
List<IndexQuery> queries = new ArrayList<IndexQuery>();
for(Person test:testList) {
    IndexQuery indexQuery = new IndexQueryBuilder().withId(test.getId()).withObject(test).build();
    queries.add(indexQuery);
}
elasticsearchTemplate.bulkIndex(queries, Person.class);
```

#### 查询数据

```java
GetQuery query = new GetQuery(id);
Person info = elasticsearchTemplate.queryForObject(query, Person.class);
```

#### 聚合数据

简化版：

```java
NativeSearchQuery query = new NativeSearchQueryBuilder()
        .addAggregation(AggregationBuilders.terms("agg_count").field("module.keyword"))
        .build();

SearchHits<PhishingLog> searchHits = elasticsearchTemplate.search(query, PhishingLog.class);
//取出聚合结果
Aggregations aggregations = searchHits.getAggregations();
Terms terms = (Terms) aggregations.asMap().get("agg_count");

for (Terms.Bucket bucket : terms.getBuckets()) {
    String keyAsString = bucket.getKeyAsString();   // 聚合字段列的值
    long docCount = bucket.getDocCount();           // 聚合字段对应的数量
    System.out.println(keyAsString + " " + docCount);
}
```

详细版：

需要格外注意类型转换，如 ParsedStringTerms、ParsedLongTerms 等。

```java
// 关键词条件筛选
BoolQueryBuilder bool = new BoolQueryBuilder();
bool.must(QueryBuilders.rangeQuery("@timestamp").from(start.getTime()));
bool.must(QueryBuilders.rangeQuery("@timestamp").to(end.getTime()));

// 分组。terms分组名称、field分组字段、size分组数量
TermsAggregationBuilder aggregationBuilderGroupBy = AggregationBuilders.terms("agg_count").field("module.keyword").size(200);

// 组合查询
NativeSearchQuery searchQuery = new NativeSearchQueryBuilder().addAggregation(aggregationBuilderGroupBy).withQuery(bool).build();

// 查询。实体类上需要有Doucment注解
SearchHits<PhishingLog> searchHits = elasticsearchTemplate.search(searchQuery, PhishingLog.class);

// 解析
Aggregations aggPage = searchHits.getAggregations();
Aggregation aggregation = aggPage.get("agg_count");
// 因为是利用String类型字段来进行的term聚合，所以结果要强转为 ParsedStringTerms 类型
List<? extends Terms.Bucket> buckets = ((ParsedStringTerms) aggregation).getBuckets();
int total = buckets.size();
for (int index = 0; index < total; index++) {
    Terms.Bucket bucket = buckets.get(index);
    ModuleDto dto = new ModuleDto();
    dto.setName(bucket.getKeyAsString());
    if(searchLevel) {
        ParsedStringTerms aggregationsTemp = bucket.getAggregations().get("get_level");
        ParsedLongTerms aggregationsTemp2 = bucket.getAggregations().get("get_time");
        for (Terms.Bucket levelBucket : aggregationsTemp.getBuckets()) {
            if("error".equalsIgnoreCase(levelBucket.getKeyAsString())) {
                // 这个 getDocCount 是每组的数量
                dto.setErrorNum((int)levelBucket.getDocCount());
            }
            if("info".equalsIgnoreCase(levelBucket.getKeyAsString())) {
                dto.setInfoNum((int)levelBucket.getDocCount());
            }
            if("debug".equalsIgnoreCase(levelBucket.getKeyAsString())) {
                dto.setDebugNum((int)levelBucket.getDocCount());
            }
        }
        for (Terms.Bucket levelBucket : aggregationsTemp2.getBuckets()) {
            dto.setUpdateTime(new DateTime(levelBucket.getKeyAsString()).toDate());
        }

    }
    list.add(dto);
}
```

### 参考资料

- https://blog.csdn.net/qq_45071180/article/details/122702830