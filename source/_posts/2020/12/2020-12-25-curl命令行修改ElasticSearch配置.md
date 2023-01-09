---
title: curl命令行修改ElasticSearch配置
layout: info
commentable: true
date: 2020-12-25
mathjax: true
mermaid: true
tags: [Database,ElasticSearch,curl]
categories: 
- [Database,ElasticSearch]
- [OS,Shell]
description: 
---

### curl

curl 是常用的命令行工具，用来请求 Web 服务器。它的名字就是客户端（client）的 URL 工具的意思。

<!--more-->

#### 常用参数

- `-d`参数用于发送 POST 请求的数据体。
- `-H`参数添加 HTTP 请求的标头。
- `-X`参数指定 HTTP 请求的方法。

### 集群

查看es集群状态：

```bash
curl http://127.0.0.1:9200/_cat/health?v
```

#### 修改系统参数

修改参数（单个查询最大的桶数，默认10000）：

```bash
curl -X PUT http://127.0.0.1:9200/_cluster/settings?flat_settings \
     -H 'content-Type:application/json' \
     -d '{"persistent":{"search":{"max_buckets":"2147483647"}}}'
```

如果不加 `-H 'content-Type:application/json'` 参数，可能会报错：

> {"error":"Content-Type header [application/x-www-form-urlencoded] is not supported","status":406}

#### 修改集群分片数量

新建索引时，出现报错：

> Validation Failed: 1: this action would add [10] shards, but this cluster currently has [996]/[1000] maximum normal shards open

这是由于 ES7.x默认分片只有1000个，目前已经用完了，导致已经没法创建新的索引了。需要提高ES的分片数量。

```bash
curl --location --request PUT 'http://127.0.0.1:9200/_cluster/settings' \
     --header 'Content-Type: application/json' \
     --data '{"persistent":{"cluster":{"max_shards_per_node":10000}}}'
```

### 节点

集群节点健康查看：

```bash
curl http://127.0.0.1:9200/_cat/nodes?v
```

### 索引管理

列出集群所有索引：

```bash
curl http://127.0.0.1:9200/_cat/indices?v
```

删除某个索引：

```bash
curl -XDELETE 'http://127.0.0.1:9200/index_name'
```

### 索引配置

查看索引配置：

```
curl http://elastic:123456@127.0.0.1:9200/index_name/_settings
```


修改索引副本数量：

```bash
curl -X PUT http://127.0.0.1:9200/index_name/_settings -H 'content-Type:application/json' -d '{"number_of_replicas": 2}'
```

更新索引配置：

```
curl -X PUT 127.0.0.1:30103/_cluster/settings -H 'content-Type:application/json' -d '{
  "persistent" : {
    "indices.breaker.fielddata.limit" : "100%",
    "indices.breaker.total.limit" : "80%" 
  }
}'
```

### 索引 Mapping 

#### 查看索引 Mapping

```bash
curl http://127.0.0.1:9200/index_name/_mapping?pretty
```

#### 更新索引Mapping

```shell
PUT userreport-2022-07-03/_mapping 
{ "properties": { 
	"clusterIgnores" : {
	  "type" : "nested",
	  "properties" : {
		"type" : {
		  "type" : "integer"
		},
		"value" : {
		  "type" : "integer"
		}
	  }
	} 
  } 
}
```

### 索引数据

#### 查看索引数据

```shell
curl http://elastic:123456@127.0.0.1:9200/index_name/_search
// 查询
curl http://127.0.0.1:9200/index_name/_search?pretty&q=column_name:column_value
// 排序
curl http://127.0.0.1:9200/index_name/_search?pretty&sort=@timestamp:asc&q=column_name:column_value
```

#### 查看索引总数

```
curl http://elastic:123456@127.0.0.1:9200/index_name/_count
```

#### 查看具体数据

查询某个索引下某条记录的具体数据：

```bash
curl http://127.0.0.1:9200/index_name/mail/1e50baf1dea339f871f9272508bc7615
curl http://127.0.0.1:9200/index_name/_doc/1e50baf1dea339f871f9272508bc7615（默认 type 为 _doc）
```


### 索引模板

#### 查看模板内容

```
curl http://127.0.0.1:9200/_template/template_name?pretty
```

#### 更新模板内容

```
curl -X PUT http://127.0.0.1:9200/_template/userreport
{
    "order" : 0,
    "index_patterns" : [
      "userreport-*",
      "qy-userreport-*"
    ]
}
```

### 测试分词效果

```
curl -X POST  127.0.0.1:9200/_analyze -H 'content-Type:application/json' -d '{   "tokenizer": "ngram",  "text": "Quick Fox"}'
```



