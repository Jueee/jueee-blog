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