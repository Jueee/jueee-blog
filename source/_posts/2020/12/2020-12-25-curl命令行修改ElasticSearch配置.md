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

### GET

查看es集群状态：

```bash
curl http://127.0.0.1:9200/_cat/health?v
```

集群节点健康查看：

```bash
curl http://127.0.0.1:9200/_cat/nodes?v
```

列出集群所有索引：

```bash
curl http://127.0.0.1:9200/_cat/indices?v
```

查看某个索引的 Mapping 配置：

```bash
curl http://127.0.0.1:9200/index_name/_mapping?pretty
```

查看索引数据：

```shell
curl http://elastic:123456@127.0.0.1:9200/index_name/_search
// 查询
curl http://127.0.0.1:9200/index_name/_search?pretty&q=column_name:column_value
// 排序
curl http://127.0.0.1:9200/index_name/_search?pretty&sort=@timestamp:asc&q=column_name:column_value
```

查看索引配置：

```
curl http://elastic:123456@127.0.0.1:9200/index_name/_settings
```

查看索引总数：

```
curl http://elastic:123456@127.0.0.1:9200/index_name/_count
```

查询某个索引下某条记录的具体数据：

```bash
curl http://127.0.0.1:9200/index_name/mail/1e50baf1dea339f871f9272508bc7615
curl http://127.0.0.1:9200/index_name/_doc/1e50baf1dea339f871f9272508bc7615（默认 type 为 _doc）
```

### PUT

修改参数（单个查询最大的桶数，默认10000）：

```bash
curl -X PUT http://127.0.0.1:9200/_cluster/settings?flat_settings -H 'content-Type:application/json' -d '{"persistent":{"search":{"max_buckets":"2147483647"}}}'
```

如果不加 `-H 'content-Type:application/json'` 参数，可能会报错：

> {"error":"Content-Type header [application/x-www-form-urlencoded] is not supported","status":406}

修改索引副本数量：

```bash
curl -X PUT http://127.0.0.1:9200/index_name/_settings -H 'content-Type:application/json' -d '{"number_of_replicas": 2}'
```

若报异常：



```
curl -X PUT 127.0.0.1:30103/_cluster/settings -H 'content-Type:application/json' -d '{
  "persistent" : {
    "indices.breaker.fielddata.limit" : "100%",
    "indices.breaker.total.limit" : "80%" 
  }
}'
```



### DELETE

删除某个索引：

```bash
curl -XDELETE 'http://127.0.0.1:9200/index_name'
```

