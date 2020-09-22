---
title: kafka-manager的安装和使用
layout: info
commentable: true
date: 2020-08-14
mathjax: true
mermaid: true
tags: [Linux,软件,Kafka]
categories: [Linux,软件]
description: 
---

### kafka-manager地址

GitHub地址：

> [https://github.com/yahoo/CMAK](https://github.com/yahoo/CMAK)

下载地址：

> [https://github.com/yahoo/CMAK/releases](https://github.com/yahoo/CMAK/releases)

### kafka-manager简介

kafka-manager是目前最受欢迎的kafka集群管理工具，最早由雅虎开源，用户可以在Web界面执行一些简单的集群管理操作。具体支持以下内容：

- 管理多个集群
- 轻松检查群集状态（主题，消费者，偏移，代理，副本分发，分区分发）
- 运行首选副本选举
- 使用选项生成分区分配以选择要使用的代理
- 运行分区重新分配（基于生成的分配）
- 使用可选主题配置创建主题（0.8.1.1具有与0.8.2+不同的配置）
- 删除主题（仅支持0.8.2+并记住在代理配置中设置delete.topic.enable = true）
- 主题列表现在指示标记为删除的主题（仅支持0.8.2+）
- 批量生成多个主题的分区分配，并可选择要使用的代理
- 批量运行重新分配多个主题的分区
- 将分区添加到现有主题
- 更新现有主题的配置

### 安装kafka-manager

#### 普通安装

##### 下载

```
wget 'https://github.com/yahoo/CMAK/releases/download/3.0.0.5/cmak-3.0.0.5.zip'
unzip cmak-3.0.0.5.zip
cd cmak-3.0.0.5
```

##### 配置

修改  `conf/application.conf` 文件：

```conf
kafka-manager.zkhosts="127.0.0.1:2181"
kafka-manager.zkhosts=${?ZK_HOSTS}
cmak.zkhosts="127.0.0.1:2181"
cmak.zkhosts=${?ZK_HOSTS}
```

##### 启动

```
$ bin/cmak &
```

#### docker 安装

DockerHub：[https://hub.docker.com/r/sheepkiller/kafka-manager](https://hub.docker.com/r/sheepkiller/kafka-manager)

安装命令：

```shell
docker run -it \
	--name kafka-manager \
	-p 9000:9000 \
	-e ZK_HOSTS=127.0.0.1:2181 \
	-e KAFKA_MANAGER_AUTH_ENABLED=true \
	-e KAFKA_MANAGER_USERNAME=admin \
	-e KAFKA_MANAGER_PASSWORD=admin \
	-d sheepkiller/kafka-manager:latest
```

### 配置 kafka-manager

kafka-manager 默认的端口是9000。

1. 添加集群

   ![1597386588682](/images/2020/08/1597386588682.png)

2. 配置集群

   ![1597386711921](/images/2020/08/1597386711921.png)
   
3. 开启消费者查看

   ![1599558709720](/images/2020/08/1599558709720.png)

### 问题解决

#### 开启JMX

如果使用kafka-manager监控，需要开启JMX，则需要勾选：

![1597405340838](/images/2020/08/1597405340838.png)

否则会有以下报错：

```
2020-08-14 17:30:58,236 - [ERROR] k.m.j.KafkaJMX$ - Failed to connect to service:jmx:rmi:///jndi/rmi://dm161.bjth.163.org:-1/jmxrmi
java.lang.IllegalArgumentException: requirement failed: No jmx port but jmx polling enabled!
```

启动kafka服务时指定`JMX_PORT`值:

```
JMX_PORT=9999 nohup bin/kafka-server-start.sh config/server.properties &
```

#### /kafka-manager/mutex

CMAK添加集群的时候报错：

```
org.apache.zookeeper.KeeperException$UnimplementedException: KeeperErrorCode = Unimplemented for /kafka-manager/mutex
        at org.apache.zookeeper.KeeperException.create(KeeperException.java:106)
        at org.apache.zookeeper.KeeperException.create(KeeperException.java:54)
        at org.apache.zookeeper.ZooKeeper.create(ZooKeeper.java:1538)
        at org.apache.curator.utils.ZKPaths.mkdirs(ZKPaths.java:291)
        at org.apache.curator.framework.imps.CreateBuilderImpl$11.call(CreateBuilderImpl.java:746)
        at org.apache.curator.framework.imps.CreateBuilderImpl$11.call(CreateBuilderImpl.java:723)
        at org.apache.curator.RetryLoop.callWithRetry(RetryLoop.java:109)
        at org.apache.curator.framework.imps.CreateBuilderImpl.pathInForeground(CreateBuilderImpl.java:720)
        at org.apache.curator.framework.imps.CreateBuilderImpl.protectedPathInForeground(CreateBuilderImpl.java:484)
        at org.apache.curator.framework.imps.CreateBuilderImpl.forPath(CreateBuilderImpl.java:474)
```

解决：

```
root@zk-0:/opt/zookeeper/bin# ./zkCli.sh
[zk: localhost:2181(CONNECTED) 1] ls /kafka-manager
[configs, deleteClusters, clusters]
[zk: localhost:2181(CONNECTED) 2] create /kafka-manager/mutex ""
Created /kafka-manager/mutex
[zk: localhost:2181(CONNECTED) 3] create /kafka-manager/mutex/locks ""
Created /kafka-manager/mutex/locks
[zk: localhost:2181(CONNECTED) 4] create /kafka-manager/mutex/leases ""
Created /kafka-manager/mutex/leases
```

参考：https://github.com/yahoo/CMAK/issues/731