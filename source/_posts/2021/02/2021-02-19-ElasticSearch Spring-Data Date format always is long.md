---
title: ElasticSearch Spring-Data Date format always is long
layout: info
commentable: true
date: 2021-02-19
mathjax: true
mermaid: true
tags: [Database,ElasticSearch]
categories: [Database,ElasticSearch]
description: 
---

当使用spring-data插入日期类型的Elasticsearch文档时，我无法获得正确的日期格式，日期格式始终为Long。

<!--more-->

### 普通格式

#### 格式化类

```java
@Data
@Document(indexName = "person")
public class Person {
    @Id
    private String id;
    private String user_name;
    private String user_password;
    private String user_email;
    @Field(store = true, type = FieldType.Date)
    private Date insert_time;
}
```

#### Mapping 效果

```json
"insert_time":{"type":"long"}
```

#### 日志提示

> SimpleElasticsearchPersistentProperty : No DateFormat defined for property Person.insert_time. Make sure you have a Converter registered for Date

#### 查看数据

命令行获取：

```bash
$ curl http://10.196.8.149:9200/person/_doc/1cbe2a07-50dd-4d98-8ad8-fdcbaae063e7
"insert_time":1613716712745
```

接口获取：

```java
GetQuery query = new GetQuery(id);
Person info = elasticsearchTemplate.queryForObject(query, Person.class);
// insert_time=Fri Feb 19 14:38:32 CST 2021
```

### DateFormat

如果在写入数据时不加时区信息，ElasticSearch默认按UTC时区写入，默认是0时区，但是当我们查看的时候，kibana会读取我们当地的时间，即东八区，进行转换，所以我们看到的时间会晚8小时。

#### 格式化字段

```java
@Field(store = true, type = FieldType.Date,format = DateFormat.custom, pattern = "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")
@JsonFormat(shape = JsonFormat.Shape.STRING, pattern ="yyyy-MM-dd'T'HH:mm:ss.SSS'Z'")
private Date insert_time;
```

#### Mapping 效果

```json
"insert_time":{"type":"date"}
```

#### 查看数据

命令行获取：

```bash
$ curl http://10.196.8.149:9200/person/_doc/a65b91a7-0753-437b-925e-fdd9d3360f13
"insert_time":"2021-02-19T07:32:27.399Z"
```

接口获取：

```java
GetQuery query = new GetQuery(id);
Person info = elasticsearchTemplate.queryForObject(query, Person.class);
// insert_time=Fri Feb 19 15:32:27 CST 2021
```

### 自定义时区

#### 格式化字段

自定义东八区：

```java
@Field(store = true, type = FieldType.Date,format = DateFormat.custom, pattern = "yyyy-MM-dd'T'HH:mm:ss.SSS'+0800'")
@JsonFormat(shape = JsonFormat.Shape.STRING, pattern ="yyyy-MM-dd'T'HH:mm:ss.SSS'+0800'")
private Date insert_time;
```

#### Mapping 效果

```json
"insert_time":{"type":"date"}
```

#### 查看数据

命令行获取：

```bash
$ curl http://10.196.8.149:9200/person/_doc/f6fa74ce-07e8-4961-ad44-a54052ccec45
"insert_time":"2021-02-19T07:36:17.529+0800"
```

接口获取：

```java
GetQuery query = new GetQuery(id);
Person info = elasticsearchTemplate.queryForObject(query, Person.class);
// insert_time=Fri Feb 19 15:36:17 CST 2021
```

### 参考资料

- https://stackoverflow.com/questions/32042430