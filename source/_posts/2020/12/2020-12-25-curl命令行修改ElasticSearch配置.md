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
- [Linux,Shell]
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
curl http://127.0.0.1:9200/mdasmail_manti/_mapping?pretty
```

查询某个索引下某条记录的具体数据：

```bash
curl http://127.0.0.1:9200/mdasmail_manti/mail/1e50baf1dea339f871f9272508bc7615
```

### PUT

修改参数（单个查询最大的桶数，默认10000）：

```bash
curl -X PUT http://127.0.0.1:9200/_cluster/settings?flat_settings -H 'content-Type:application/json' -d '{"persistent":{"search":{"max_buckets":"2147483647"}}}'
```

如果不加 `-H 'content-Type:application/json'` 参数，可能会报错：

> {"error":"Content-Type header [application/x-www-form-urlencoded] is not supported","status":406}

### DELETE

删除某个索引：

```bash
curl -XDELETE 'http://127.0.0.1:9200/mdasmail_manti'
```

