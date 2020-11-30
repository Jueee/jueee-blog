---
title: Java获取Kafka指定topic的消息总量
layout: info
commentable: true
date: 2020-11-29
mathjax: true
mermaid: true
tags: [Java,JavaClass,Kafka]
categories: 
- [Java,JavaClass]
- [Kafka]
description: 
---

### Kafka Consumer API

Kafka提供了两套API给 Consumer

- The high-level Consumer API
- The SimpleConsumer API 

第一种高度抽象的Consumer API，它使用起来简单、方便，但是对于某些特殊的需求我们可能要用到第二种更底层的API。

<!--more-->

#### SimpleConsumer优势

那么第二种 `The SimpleConsumer API ` 能够帮助我们做哪些事情?

- 一个消息读取多次
- 在一个处理过程中只消费 Partition 其中的一部分消息
- 添加事务管理机制以保证消息被处理且仅被处理一次

#### SimpleConsumer弊端

使用SimpleConsumer有哪些弊端呢？

- 必须在程序中跟踪offset值
- 必须找出指定Topic Partition中的lead broker
- 必须处理broker的变动

#### SimpleConsumer步骤

使用SimpleConsumer的步骤

1. 从所有活跃的broker中找出哪个是指定Topic Partition中的 leader broker
2. 找出指定Topic Partition中的所有备份broker
3. 构造请求
4. 发送请求查询数据
5. 处理leader broker变更

### 命令行获取topic信息总量

```bash
$ bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list XXX1:9092 --topic topicName1 --time -1
topicName1:2:73454
topicName1:5:73006
topicName1:4:73511
topicName1:1:73493
topicName1:3:73019
topicName1:0:72983

$ bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list XXX1:9092 --topic topicName1 --time -2
topicName1:2:0
topicName1:5:0
topicName1:4:0
topicName1:1:0
topicName1:3:0
topicName1:0:0
```

**--time -1** 表示要获取指定topic所有分区当前的最大位移，**--time -2** 表示获取当前最早位移。

两个命令的输出结果相减便可得到所有分区当前的消息总数。

> 分区当前的消息总数 = [--time-1] - [--time-2]

相减是因为随着 kafka 的运行，topic 中有的消息可能会被删除，因此 **--time -1** 的结果其实表示的是历史上该topic生产的最大消息数，如果用户要统计当前的消息总数就必须减去 **--time -2** 的结果。

本例中没有任何消息被删除，故 **--time -2** 的结果全是0，表示最早位移都是0，消息总数等于历史上发送的消息总数。

### Java获取topic消息总量

#### high-level Consumer

The high-level Consumer API  获取Kafka指定topic的消息总量：

```java
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Properties;
import java.util.stream.Collectors;

import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.TopicPartition;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class KafkaOffsetTools {
	private final static Logger logger = LoggerFactory.getLogger(KafkaOffsetTools.class);

	public static final String KAFKA_BOOTSTRAP_SERVERS = "XXX1:9092,XXX2:9092,XXX3:9092";
	public static final List<String> TOPIC_LIST = Arrays.asList("topicName1","topicName2");
	
	public static void main(String[] args) {
		for(String topic: TOPIC_LIST) {
			long totolNum = totalMessageCount(topic, KAFKA_BOOTSTRAP_SERVERS);
			System.out.println(topic+":"+totolNum);
		}
	}
	
    public static long totalMessageCount(String topic, String brokerList) {
        Properties props = new Properties();
        props.put("bootstrap.servers", brokerList);
        props.put("group.id", "test-group");
        props.put("enable.auto.commit", "false");
        props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
        props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");

        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
            List<TopicPartition> tps = Optional.ofNullable(consumer.partitionsFor(topic))
                    .orElse(Collections.emptyList())
                    .stream()
                    .map(info -> new TopicPartition(info.topic(), info.partition()))
                    .collect(Collectors.toList());
            Map<TopicPartition, Long> beginOffsets = consumer.beginningOffsets(tps);
            Map<TopicPartition, Long> endOffsets = consumer.endOffsets(tps);
 
            return tps.stream().mapToLong(tp -> endOffsets.get(tp) - beginOffsets.get(tp)).sum();
        }
    }
}
```

输出结果：

```
topicName1:5301171
topicName2:439466
```

#### SimpleConsumer

The SimpleConsumer API  获取Kafka指定topic的消息总量：

```java
import java.util.Arrays;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.TreeMap;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import kafka.api.PartitionOffsetRequestInfo;
import kafka.common.TopicAndPartition;
import kafka.javaapi.OffsetRequest;
import kafka.javaapi.OffsetResponse;
import kafka.javaapi.PartitionMetadata;
import kafka.javaapi.TopicMetadata;
import kafka.javaapi.TopicMetadataRequest;
import kafka.javaapi.TopicMetadataResponse;
import kafka.javaapi.consumer.SimpleConsumer;

public class KafkaOffsetTools {
    
	private final static Logger logger = LoggerFactory.getLogger(KafkaOffsetTools.class);

	public static final String KAFKA_BOOTSTRAP_SERVERS = "XXX1:9092,XXX2:9092,XXX3:9092";
	public static final List<String> TOPIC_LIST = Arrays.asList("topicName1","topicName2");
	
	public static void main(String[] args) {
		String[] kafkaHosts = KAFKA_BOOTSTRAP_SERVERS.split(",");
		List<String> seeds = Arrays.asList(kafkaHosts);
		KafkaOffsetTools kot = new KafkaOffsetTools();
		Map<String, Integer> topicNumMap = new HashMap<String, Integer>();
		for (String topicName : TOPIC_LIST) {
			TreeMap<Integer, PartitionMetadata> metadatas = kot.findLeader(seeds, topicName);
			int logSize = 0;
			for (Entry<Integer, PartitionMetadata> entry : metadatas.entrySet()) {
				int partition = entry.getKey();
				String leadBroker = entry.getValue().leader().host();
				String clientName = "Client_" + topicName + "_" + partition;
				SimpleConsumer consumer = new SimpleConsumer(leadBroker, entry.getValue().leader().port(), 100000, 64 * 1024, clientName);
				long readOffset = getLastOffset(consumer, topicName, partition, kafka.api.OffsetRequest.LatestTime(), clientName);
				logSize += readOffset;
				if (consumer != null) {
					consumer.close();
				}
			}
			topicNumMap.put(topicName, logSize);
		}
		System.out.println(topicNumMap.toString());
	}

	private TreeMap<Integer, PartitionMetadata> findLeader(List<String> a_seedBrokers, String a_topic) {
		TreeMap<Integer, PartitionMetadata> map = new TreeMap<Integer, PartitionMetadata>();
		for (String seed : a_seedBrokers) {
			SimpleConsumer consumer = null;
			try {
				String[] hostAndPort = seed.split(":");
				consumer = new SimpleConsumer(hostAndPort[0], Integer.valueOf(hostAndPort[1]), 100000, 64 * 1024, "leaderLookup" + new Date().getTime());
				List<String> topics = Collections.singletonList(a_topic);
				TopicMetadataRequest req = new TopicMetadataRequest(topics);
				TopicMetadataResponse resp = consumer.send(req);

				List<TopicMetadata> metaData = resp.topicsMetadata();
				for (TopicMetadata item : metaData) {
					for (PartitionMetadata part : item.partitionsMetadata()) {
						map.put(part.partitionId(), part);
					}
				}
			} catch (Throwable e) {
				logger.error("Broker [" + seed + "] to find Leader for [" + a_topic + "] Reason: " + e.getMessage(), e);
			} finally {
				if (consumer != null) {
					consumer.close();
				}
			}
		}
		return map;
	}
	
	public static long getLastOffset(SimpleConsumer consumer, String topic, int partition, long whichTime,
			String clientName) {
		TopicAndPartition topicAndPartition = new TopicAndPartition(topic, partition);
		Map<TopicAndPartition, PartitionOffsetRequestInfo> requestInfo = new HashMap<TopicAndPartition, PartitionOffsetRequestInfo>();
		requestInfo.put(topicAndPartition, new PartitionOffsetRequestInfo(whichTime, 1));
		OffsetRequest request = new kafka.javaapi.OffsetRequest(requestInfo, kafka.api.OffsetRequest.CurrentVersion(), clientName);
		OffsetResponse response = consumer.getOffsetsBefore(request);

		if (response.hasError()) {
			logger.error("Error fetching data Offset Data the Broker. Reason: " + response.errorCode(topic, partition));
			return 0;
		}
		long[] offsets = response.offsets(topic, partition);
		return offsets[0];
	}
}
```

输出结果：

```
{topicName1=5301171, topicName2=439466}
```

