---
title: Logstash多实例并行消费kafka
layout: info
commentable: true
date: 2021-12-24
mathjax: true
mermaid: true
tags: [软件,Linux,Logstash]
categories: 
- [Database,ElasticSearch]
description: 
---

### 消费原理

启动多个logstash并行消费kafka数据。

1. 设置相同 topic
2. 设置相同 groupid
3. 设置不同 clientid
4. input 的这个参数 consumer_threads => 10 多实列相加最好等于 topic分区数

如果一个logstash得参数大于topic，则topic数据都会被这个logstash消费掉。

### 消费设置

```java
input {
    kafka {
        id => "my_plugin_id"
            bootstrap_servers => "kafka.hostname:9092"
            topics => ["my-logger-channel"]
            group_id => "logstash"
            auto_offset_reset => "latest"
            codec => plain {
            charset => "UTF-8"
        }
    }
}
```

### docker-compose 配置

```yaml
version: '2'
services:
    logstash-run1:
        container_name: logstash-run1
        image: logstash:7.16.1
        restart: always
        logging:
            driver: "json-file"
            options:
                max-size: "300m"
        volumes:
            - ./config/:/usr/share/logstash/config/
            - ./patterns/:/usr/share/logstash/patterns/
            - /etc/localtime:/etc/localtime
            - /etc/timezone:/etc/timezone
        environment:
            - LS_HEAP_SIZE=5G
            - TZ="Asia/Shanghai"
    logstash-run2:
        container_name: logstash-run2
        image: logstash:7.16.1
        restart: always
        logging:
            driver: "json-file"
            options:
                max-size: "300m"
        volumes:
            - ./config/:/usr/share/logstash/config/
            - ./patterns/:/usr/share/logstash/patterns/
            - /etc/localtime:/etc/localtime
            - /etc/timezone:/etc/timezone
        environment:
            - LS_HEAP_SIZE=5G
            - TZ="Asia/Shanghai"
    logstash-run3:
        container_name: logstash-run3
        image: logstash:7.16.1
        restart: always
        logging:
            driver: "json-file"
            options:
                max-size: "300m"
        volumes:
            - ./config/:/usr/share/logstash/config/
            - ./patterns/:/usr/share/logstash/patterns/
            - /etc/localtime:/etc/localtime
            - /etc/timezone:/etc/timezone
        environment:
            - LS_HEAP_SIZE=5G
            - TZ="Asia/Shanghai"
```

