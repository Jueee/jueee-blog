---
title: 安装搭建Elasticsearch
layout: info
commentable: true
date: 2020-09-06
mathjax: true
mermaid: true
tags: [Elasticsearch]
categories: 
- [Database,Elasticsearch]
description: 
---

### Elasticsearch

Elasticsearch 是一个分布式的开源搜索和分析引擎，适用于所有类型的数据，包括文本、数字、地理空间、结构化和非结构化数据。

<!--more-->

### 下载Elasticsearch

> https://www.elastic.co/cn/downloads/elasticsearch

### 安装Elasticsearch

```
$ wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.4.2-linux-x86_64.tar.gz
$ tar -xvf elasticsearch-7.4.2-linux-x86_64.tar
```

### 配置Elasticsearch

配置文件：

```
~/elasticsearch-7.4.2/config$ cat elasticsearch.yml
```

#### 日志路径

```yaml
path.logs: /mnt/data/elasticsearch/logs
```

#### 数据存储

```yaml
path.data: /mnt/data/elasticsearch/data
```

#### 远程访问

```yaml
network.host: 0.0.0.0
```

### 启动Elasticsearch

```
$ ./elasticsearch -d
```

如果你想把 Elasticsearch 作为一个守护进程在后台运行，那么可以在后面添加参数 -d 。

### 启动异常处理

#### vm.max_map_count

异常：

```
max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
```

修改/etc/sysctl.conf，增加如下配置：

```
vm.max_map_count=262144
```

保存后执行 `sysctl -p` 生效

查看结果：

```
$ sysctl -a|grep vm.max_map_count
vm.max_map_count=262144
```

#### default discovery settings are unsuitable

异常：

```
the default discovery settings are unsuitable for production use; at least one of [discovery.seed_hosts, discovery.seed_providers, cluster.initial_master_nodes] must be configured
```

##### 方案一：cluster.initial_master_nodes

配置 cluster.initial_master_nodes 为当前 node，默认为注释，放开注释就行了：

```yaml
cluster.initial_master_nodes: ["node-1", "node-2"]
```

##### 方案二：discovery.seed_hosts

配置 discovery.seed_hosts 为机器名或者 IP 信息：

```yaml
discovery.seed_hosts: elasticsearch.hostname.svc
```

#### system call filters failed to install

异常：

```
system call filters failed to install; check the logs and fix your configuration or disable system call filters at your own risk
```

这是在因为 Centos6 不支持 SecComp，而 ES5.2.0 默认 bootstrap.system_call_filter 为true进行检测，所以导致检测失败，失败后直接导致ES不能启动。

解决：
在elasticsearch.yml 中配置 bootstrap.system_call_filter 为 false，注意要在Memory下面：

```yaml
bootstrap.memory_lock: false
bootstrap.system_call_filter: false
```

### 中文 ik 分词

#### 下载分词

> https://github.com/medcl/elasticsearch-analysis-ik/releases

#### 安装分词

```
ADD elasticsearch-analysis-ik-$VERSION.zip /tmp/
RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install -b file:///tmp/elasticsearch-analysis-ik-$VERSION.zip
```

### 查看配置

- 查看es配置：http://127.0.0.1:9200/ 

- 查看es集群状态：http://127.0.0.1:9200/_cat/health?v
- 集群节点健康查看：http://127.0.0.1:9200/_cat/nodes?v 
- 列出集群索引
  ：http://127.0.0.1:9200/_cat/indices?v  
- 查询集群数据
  ：http://127.0.0.1:9200/mail_indexname/mail/1e50baf1dea339f871f9272508bc7615

