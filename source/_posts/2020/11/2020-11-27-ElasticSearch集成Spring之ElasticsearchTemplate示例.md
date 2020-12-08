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
- [ElasticSearch]
description: 
---

### ElasticsearchTemplate

ElasticsearchTemplate 是 Spring 对 ElasticSearch 的 Java api 进行的封装，提供了大量的相关的类来完成各种各样的查询。

#### 引入依赖

```xml
<!-- https://mvnrepository.com/artifact/org.springframework.data/spring-data-elasticsearch -->
<dependency>
    <groupId>org.springframework.data</groupId>
    <artifactId>spring-data-elasticsearch</artifactId>
    <version>3.2.1.RELEASE</version>
</dependency>
```

<!--more-->

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

