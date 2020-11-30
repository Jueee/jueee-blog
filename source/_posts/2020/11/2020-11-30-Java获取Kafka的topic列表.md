---
title: Java获取Kafka的topic列表
layout: info
commentable: true
date: 2020-11-30
mathjax: true
mermaid: true
tags: [Kafka,Java,JavaClass]
categories: 
- [Java,JavaClass]
- [Kafka]
description: 
---

### 命令行获取

根据 zookeeper 地址获取 topic：

```bash
$ bin/kafka-topics.sh --list --zookeeper 127.0.0.1:2181
```

<!--more-->

### 引入依赖获取

#### 根据 kafka 地址

引入依赖

```xml
<dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka-clients</artifactId>
    <version>${kafka.version}</version>
</dependency>
```

根据 kafka 地址获取 topic 的 Java 方法

```java
Properties pro = new Properties();
pro.put("bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS);
ListTopicsResult result = KafkaAdminClient.create(pro).listTopics();
KafkaFuture<Set<String>> set = result.names();
Set<String> topicSet = set.get();
```

#### 根据 zookeeper 地址

引入依赖

```xml
<dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka_2.12</artifactId>
    <version>${kafka.version}</version>
</dependency>
```

根据 zookeeper 地址获取 topic 的 Java 方法

```java
ZkUtils zkUtils = ZkUtils.apply(KAFKA_ZOOKEEPER_SERVERS, 30000, 30000, JaasUtils.isZkSecurityEnabled());
Seq<String> topicSeq = zkUtils.getAllTopics();
List<String> allTopicList = JavaConversions.seqAsJavaList(topicSeq);
```

