---
title: Java消费Kafka配置信息总结
layout: info
commentable: true
date: 2022-08-21
mathjax: true
mermaid: true
tags: [Apache,Kafka]
categories: [Apache,Kafka]
description: 
---

Java消费Kafka配置信息总结。

配置文档：https://kafka.apache.org/documentation/#newconsumerconfigs

<!--more-->

### 长轮询poll消息

代码中设置了长轮询的时间是 1000 毫秒：

```java
ConsumerRecords<String,String> records =  consumer.poll(Duration.ofMillis(1000));
```

【注意】

- poll() 方法里传的参数是时间（ms）。
- Kafka 轮询一次就相当于拉取（poll）一定时间段broker中可消费的数据，  在这个指定时间段里拉取，时间到了就立刻返回数据。 
- poll（5000）：  即在5s中内拉去的数据返回到消费者端。

### 消费者拉取最大条数

默认情况下，消费者一次最大会拉去的消息条数设置如下：

```java
// max.poll.records
props.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 500);
```

【注意】必须为整型，不能为字符串。

对于如下消费循环：

```java
while (true){
    ConsumerRecords<String,String> records =  consumer.poll(Duration.ofMillis(1000));
    for (ConsumerRecord<String, String> record : records) {
        System.out.printf("收到消息：partition = %d,offset = %d,key = %s ,value = %s%n",
                record.partition(),record.offset(),record.key(),record.value());
    }
}
```

- 如果一次poll到500条消息，就直接执行for循环
- 如果一次没有poll到500条，且时间在1秒内，那么长轮询继续poll，要么到500条，要么到1s

### 消费者拉取最大字节

服务器将返回的每个分区的最大数据量：

```java
// max.partition.fetch.bytes
props.put(ConsumerConfig.MAX_PARTITION_FETCH_BYTES_CONFIG, 1 * 1024 * 1024);
```

设置 max.partition.fetch.bytes 时的另一个重要考虑因素是消费者处理数据所花费的时间。

消费者必须足够频繁地调用 poll() 以避免会话超时和随后的重新平衡。

如果单次 poll() 返回的数据量很大，消费者处理的时间可能会更长，这意味着它不会及时到达轮询循环的下一次迭代，以避免会话超时。

### 消费者心跳检查

如果两次poll的时间超过了30s的时间间隔，kafka会认为消费者消费能力过弱，将其踢出消费者组，将分区分配给其他消费者 rebalance

```java
// heartbeat.interval.ms
// consumer给broker发送心跳的间隔时间
props.put(ConsumerConfig.HEARTBEAT_INTERVAL_MS_CONFIG, 30 * 1000);
```

### 消费者健康状态检查

消费者每隔1s向kafka集群发送心跳，集群发现如果有超过10s没有续约的消费者，将被踢出消费组，出发消费组的rebalance机制，将该分区交给消费组里其他消费者进行消费

```java
// heartbeat.interval.ms
// consumer给broker发送心跳的间隔时间
props.put(ConsumerConfig.HEARTBEAT_INTERVAL_MS_CONFIG, 1000);
// session.timeout.ms
// kafka如果超过10秒没有收到消费这的心跳，会把消费者踢出消费者组，进行rebalance,把分区分配给其他消费者
props.put(ConsumerConfig.SESSION_TIMEOUT_MS_CONFIG, 10 * 1000);
```

其中，`session.timeout.ms` 的设置必须介于 `group.min.session.timeout.ms` 和 `group.max.session.timeout.ms` 之间。

- group.min.session.timeout.ms：6000 (6 seconds)：消费者允许的最小会话超时。

  更短的超时导致更快的故障检测，代价是更频繁的消费者心跳

- group.max.session.timeout.ms：1800000 (30 minutes)：注册消费者允许的最大会话超时。

  更长的超时时间让消费者有更多的时间来处理心跳之间的消息，但代价是检测故障的时间更长。

### 请求时间

配置控制客户端等待请求响应的最长时间。

如果在超时之前没有收到响应，客户端将在必要时重新发送请求，或者如果重试次数用尽，则请求失败。

request.timeout.ms 应该大于 session.timeout.ms 和 fetch.max.wait.ms。

### 指定条件消费

#### 指定分区消费

```JAVA
consumer.assign(Arrays.asList(new TopicPartition(TOPIC_NAME,0)));
```

#### 消息回溯消费

从topic offset的0号位置开始消费

```JAVA
consumer.assign(Arrays.asList(new TopicPartition(TOPIC_NAME,0)));
consumer.seekToBeginning(Arrays.asList(new TopicPartition(TOPIC_NAME,0)));
```

#### 指定offset消费

```JAVA
consumer.assign(Arrays.asList(new TopicPartition(TOPIC_NAME,0)));
consumer.seek(new TopicPartition(TOPIC_NAME,0),10);
```

#### 从指定时间点开始消费

```JAVA
//从指定时间点开始消费
//1. 拿到主题下所有的分区
List<PartitionInfo> partitionInfos = consumer.partitionsFor(TOPIC_NAME);
//2. 拿到1小时前的时间
long fetchDateTime = new Date().getTime()- 1000 * 60 * 60;
HashMap<TopicPartition, Long> map = new HashMap<>();
for (PartitionInfo partitionInfo : partitionInfos) {
    map.put(new TopicPartition(TOPIC_NAME, partitionInfo.partition()),fetchDateTime);
}
//3. consumer.offsetsForTimes 根据时间拿到偏移量
Map<TopicPartition, OffsetAndTimestamp> parmap = consumer.offsetsForTimes(map);
for (Map.Entry<TopicPartition, OffsetAndTimestamp> entry : parmap.entrySet()) {
    //先拿到分区
    TopicPartition key = entry.getKey();
    OffsetAndTimestamp value = entry.getValue();
    if(key ==null || value == null) continue;
    long offset = value.offset();
    System.out.println("partition-"+key.partition() + "|offset-"+offset);
    //根据消费里的timestamp确定offset
    if(value != null){
        consumer.assign(Arrays.asList(key));
        consumer.seek(key,offset);
    }
}
```

### 新消费组的消费偏移量

```JAVA
/**
 * 当消费主题的是一个新的消费组，或者指定offset的消费方式，offset不存在
 * latest(默认)：只消费自己启动后发送到主题的消息
 * earliest: 第一次从头开始消费，以后按照消费offset记录继续消费，这个需要区别于consumer.seekToBeginning(每次从头开始消费)
 */
// auto.offset.reset
props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
```

