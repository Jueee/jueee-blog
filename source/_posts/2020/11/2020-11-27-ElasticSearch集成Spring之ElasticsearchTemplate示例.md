---
title: ElasticSearch集成Spring之ElasticsearchTemplate示例
layout: info
commentable: true
date: 2020-11-27
mathjax: true
mermaid: true
tags: [Java,JavaClass,ElasticSearch]
categories: 
- [Java,JavaClass]
- [Database,ElasticSearch]
description: 
---

### ElasticsearchTemplate

ElasticsearchTemplate 是 Spring 对 ElasticSearch 的 Java api 进行的封装，提供了大量的相关的类来完成各种各样的查询。

#### 引入依赖

Springboot 项目：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-elasticsearch</artifactId>
</dependency>
```

普通项目：

```xml
<!-- https://mvnrepository.com/artifact/org.springframework.data/spring-data-elasticsearch -->
<dependency>
    <groupId>org.springframework.data</groupId>
    <artifactId>spring-data-elasticsearch</artifactId>
    <version>3.2.1.RELEASE</version>
</dependency>
```

<!--more-->

### 使用 Template

1. 参数配置：

   ```properties
   elasticsearch.address=127.0.0.1:9200
   elasticsearch.cluster-name=elasticsearch
   ```

2. 配置引入：

   ```java
   import lombok.extern.slf4j.Slf4j;
   import org.elasticsearch.common.settings.Settings;
   import org.elasticsearch.common.transport.TransportAddress;
   import org.elasticsearch.xpack.client.PreBuiltXPackTransportClient;
   import org.springframework.beans.factory.annotation.Value;
   import org.springframework.context.annotation.Bean;
   import org.springframework.context.annotation.Configuration;
   import org.springframework.data.elasticsearch.core.ElasticsearchTemplate;
   
   import java.net.InetAddress;
   
   @Slf4j
   @Configuration
   public class ElasticSearchConfig {
   
       @Value("${elasticsearch.address}")
       private String elasticSearchAddress;
   
       @Value("${elasticsearch.cluster-name}")
       private String elasticSearchClusterName;
   
       @Bean
       PreBuiltXPackTransportClient elasticsearchClient() {
           String clusterNodes = elasticSearchAddress;
           Settings  settings= Settings.builder()
                   .put("cluster.name", elasticSearchClusterName)
                   .build();
           PreBuiltXPackTransportClient client = new PreBuiltXPackTransportClient(settings);
           try{
               for (String clusterNode : clusterNodes.split(";")) {
                   //if (clientMap.get(DataSourceNameConstant.USER_DB + dataBase.getOrgId()) == null) {
                   String hostName = clusterNodes.split(":")[0];
                   String port = clusterNodes.split(":")[1];
                   log.info(" transport node : " + clusterNode);
                   TransportAddress socketTransportAddress = new TransportAddress(
                           InetAddress.getByName(hostName), Integer.valueOf(port));
                   client.addTransportAddress(socketTransportAddress);
                   client.addTransportAddress(socketTransportAddress);
               }
           } catch (Exception e){
               log.error(e.getMessage(),e);
           }
           return client;
       }
   
       @Bean
       ElasticsearchTemplate elasticsearchTemplate() {
           return new ElasticsearchTemplate(elasticsearchClient());
       }
   }
   ```

3. 使用：

   ```java
   @Autowired
   ElasticsearchTemplate elasticsearchTemplate;
   ```

### 使用示例

**索引是否存在**

```java
elasticsearchTemplate.indexExists(Test.class)
```

**创建索引并初始化 Mapping**

```java
boolean createResult = elasticsearchTemplate.createIndex(Test.class);
logger.info("[createResult]"+createResult);
elasticsearchTemplate.putMapping(Test.class);
elasticsearchTemplate.refresh(Test.class);
```

**分页查询并计算总数量**

```java
// 特别注意：es的分页从0页开始
SearchQuery searchQuery = new NativeSearchQueryBuilder().withQuery(bool).withPageable( PageRequest.of(page, perPage)).build();
Page<Account> list = elasticsearchTemplate.queryForPage(searchQuery, Account.class);
elasticsearchTemplate.queryForPage(searchQuery, Account.class, new SearchResultMapper() {
	@Override
	public <T> T mapSearchHit(SearchHit searchHit, Class<T> type) {
		return null;
	}
	@Override
	public <T> AggregatedPage<T> mapResults(SearchResponse response, Class<T> clazz, Pageable pageable) {
		paginator.setItems((int)response.getHits().getTotalHits());
		return null;
	}
});
```

