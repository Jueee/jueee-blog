---
title: ElasticSearch集成查询BoolQueryBuilder使用汇总
layout: info
commentable: true
date: 2023-04-27
mathjax: true
mermaid: true
tags: [ElasticSearch,Java,JavaClass,Spring]
categories: 
- [Database,ElasticSearch]
- [Java,JavaClass]
description: 
---

BoolQueryBuilder 

<!--more-->

### 创建查询对象

```
BoolQueryBuilder bool = new BoolQueryBuilder();
```

### 匹配数据

#### 精准匹配

##### 完全匹配一个值

```
bool.must(QueryBuilders.termQuery(key, value));
```

##### 完全匹配多个值

```
bool.must(QueryBuilders.termsQuery(key, value1, value2, value3));
```

#### 存在匹配

```java
QueryBuilders.existsQuery("your_field");
```

嵌套查询

```java
TermQueryBuilder termQuery = QueryBuilders.termQuery("properties.key.keyword", "head");
BoolQueryBuilder filterBoolQuery = QueryBuilders.boolQuery().filter(termQuery);
NestedQueryBuilder nestedQuery = QueryBuilders.nestedQuery("properties", filterBoolQuery, ScoreMode.None);
```

#### 不存在匹配

```java
QueryBuilders.boolQuery().mustNot(QueryBuilders.existsQuery("your_field"));
```

嵌套查询

```java
TermQueryBuilder termQuery = QueryBuilders.termQuery("properties.key", "mailInfoEsId");
BoolQueryBuilder filterBoolQuery = QueryBuilders.boolQuery().filter(termQuery);
NestedQueryBuilder nestedQuery = QueryBuilders.nestedQuery("properties", filterBoolQuery, ScoreMode.None);
BoolQueryBuilder finalBoolQuery = QueryBuilders.boolQuery().mustNot(nestedQuery);
```

#### 包含匹配

```
bool.must(QueryBuilders.matchPhraseQuery(key, value));
```

- 使用 matchQuery 时，在执行查询时，搜索的词会被分词器分词。
- 使用 matchPhraseQuery 时，不会被分词器分词，而是直接以一个短语的形式查询。

#### 应该(should) 匹配

should：代表可选满足的查询条件，类似于“或”的关系。

例如，查询文档中同时包含关键词“Elasticsearch”和“Java”，或者包含关键词“Elastic”，可以使用如下查询：

```java
bo.should(QueryBuilders.boolQuery()
        .must(QueryBuilders.matchQuery("title", "Elasticsearch"))
        .must(QueryBuilders.matchQuery("content", "search")));
```

#### 过滤(filter)匹配

