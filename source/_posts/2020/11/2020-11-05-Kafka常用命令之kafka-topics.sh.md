---
title: Kafka常用命令之kafka-topics.sh
layout: info
commentable: true
date: 2020-11-05
mathjax: true
mermaid: true
tags: [Apache,Kafka]
categories: [Apache,Kafka]
description: 
---

kafka-topics.sh 脚本主要负责 topic 相关的操作。它的具体实现是通过 kafka-run-class 来调用 `TopicCommand` 类，并根据参数执行指定的功能。

<!--more-->

### 场景再现

若程序报错：

>  [Producer clientId=producer-1] Error while fetching metadata with correlation id 312 : {logger-channel=UNKNOWN_TOPIC_OR_PARTITION}

可能原因：

topic不存在，切自动创建失败

需要设置：

```properties
auto.create.topics.enable=true
```

如果不方便修改配置，则需要手动创建 topic。

### 查看 topic

```bash
bin/kafka-topics.sh --list --zookeeper 127.0.0.1:2181/spacemanti
```

### 创建 topic 

```bash
bin/kafka-topics.sh --create --zookeeper 127.0.0.1:2181/spacemanti --config max.message.bytes=128000000 --config flush.messages=1 --replication-factor 1 --partitions 1 --topic logger-channel
```

### 查看 topic

```bash
bin/kafka-topics.sh --describe --zookeeper 127.0.0.1:2181/spacemanti  --topic manti-logger-channel                    Topic:manti-logger-channel      PartitionCount:1        ReplicationFactor:1     Configs:max.message.bytes=128000000,flush.messages=1
        Topic: manti-logger-channel     Partition: 0    Leader: 2       Replicas: 2     Isr: 2
```

* **PartitionCount**：partition 个数。
  
* **ReplicationFactor**：副本个数。
  
* **Partition**：partition 编号，从 0 开始递增。
  
* **Leader**：当前 partition 起作用的 breaker.id。
  
* **Replicas**: 当前副本数据所在的 breaker.id，是一个列表，排在最前面的其作用。
  
* **Isr**：当前 kakfa 集群中可用的 breaker.id 列表。

### 删除 topic

```bash
bin/kafka-topics.sh --describe --zookeeper 127.0.0.1:2181/spacemanti  --topic logger-channel
```

- 若 delete.topic.enable=true：直接彻底删除该 Topic。
- 若 delete.topic.enable=false：如果当前 Topic 没有使用过即没有传输过信息：可以彻底删除。
   如果当前 Topic 有使用过即有过传输过信息：并没有真正删除 Topic 只是把这个 Topic 标记为删除(marked for deletion)，重启 Kafka Server 后删除。

 **注**：delete.topic.enable=true 配置信息位于配置文件 config/server.properties 中(较新的版本中无显式配置，默认为 true)。

### 修改 Topic

- **增加分区数**

  ```shell
  bin/kafka-topics.sh --alter --bootstrap-server node1:9092,node2:9092,node3:9092 --topic topicName --partitions 3
  1
  ```

  修改分区数时，仅能增加分区个数。若是用其减少 partition 个数，则会报如下错误信息：

  ```
    org.apache.kafka.common.errors.InvalidPartitionsException: The number of partitions for a topic can only be increased. Topic hadoop currently has 3 partitions, 2 would not be an increase.
  1
  ```

  不能用来修改副本个数。(请使用 kafka-reassign-partitions.sh 脚本增加副本数)

- **增加配置**

  ```shell
  bin/kafka-topics.sh --alter --bootstrap-server node1:9092,node2:9092,node3:9092 --topic topicName --config flush.messages=1
  1
  ```

- **删除配置**

  ```shell
  bin/kafka-topics.sh --alter --bootstrap-server node1:9092,node2:9092,node3:9092 --topic topicName --delete-config flush.messages
  ```

### 配置属性

当如下所示的属性配置到 Topic 上时，将会覆盖 server.properties 上对应的属性。

| 属性名                    | 值类型 | 默认值              | 有效值                                | 服务器默认属性                  | 描述                                                         |
| ------------------------- | ------ | ------------------- | ------------------------------------- | ------------------------------- | ------------------------------------------------------------ |
| cleanup.policy            | list   | delete              | delete compact                        | log.cleanup.policy              | 过期或达到上限日志的清理策略。 delete：删除 compact：压缩    |
| compression.type          | string | producer            | uncompressed snappy lz4 gzip producer | compression.type                | 指定给该topic最终的压缩类型                                  |
| delete.retention.ms       | long   | 86400000            | [0,…]                                 | log.cleaner.delete.retention.ms | 压缩的日志保留的最长时间，也是客户端消费消息的最长时间。 与 log.retention.minutes 的区别在于：一个控制未压缩的数据，一个控制压缩后的数据。 |
| file.delete.delay.ms      | long   | 60000               | [0,…]                                 | log.segment.delete.delay.ms     | 从文件系统中删除前所等待的时间                               |
| flush.messages            | long   | 9223372036854775807 | [0,…]                                 | log.flush.interval.messages     | 在消息刷到磁盘之前，日志分区收集的消息数                     |
| flush.ms                  | long   | 9223372036854775807 | [0,…]                                 | log.flush.interval.ms           | 消息在刷到磁盘之前，保存在内存中的最长时间，单位是ms         |
| index.interval.bytes      | int    | 4096                | [0,…]                                 | log.index.interval.bytes        | 执行 fetch 操作后，扫描最近的 offset 运行空间的大小。 设置越大，代表扫描速度越快，但是也更耗内存。 （一般情况下不需要设置此参数） |
| message.max.bytes         | int    | 1000012             | [0,…]                                 | message.max.bytes               | log中能够容纳消息的最大字节数                                |
| min.cleanable.dirty.ratio | double | 0.5                 | [0,…,1]                               | log.cleaner.min.cleanable.ratio | 日志清理的频率控制，占该log的百分比。 越大意味着更高效的清理，同时会存在空间浪费问题 |
| retention.bytes           | long   | -1                  |                                       | log.retention.bytes             | topic每个分区的最大文件大小。 一个 topic 的大小限制 = 分区数 * log.retention.bytes。 -1 表示没有大小限制。 |
| retention.ms              | int    | 604800000           | [-1,…]                                | log.retention.minutes           | 日志文件保留的分钟数。 数据存储的最大时间超过这个时间会根据 log.cleanup.policy 设置的策略处理数据 |
| segment.bytes             | int    | 1073741824          | [14,…]                                | log.segment.bytes               | 每个 segment 的大小 (默认为1G)                               |
| segment.index.bytes       | int    | 10485760            | [0,…]                                 | log.index.size.max.bytes        | 对于segment日志的索引文件大小限制(默认为10M)                 |