---
title: Zookeeper客户端错误：Packet len* is out of range!
layout: info
commentable: true
date: 2020-12-17
mathjax: true
mermaid: true
tags: [Apache,Zookeeper]
categories: [Apache,Zookeeper]
description: 
---

### 出现问题

zookeeper 客户端出现异常：

```
2020-12-16 14:47:52,219 [main-SendThread(127.0.0.1:2181)] WARN  org.apache.zookeeper.ClientCnxn$SendThread (ClientCnxn.java:1161) - Session 0x1766a4799830001 for server localhost/127.0.0.1:2181, unexpected error, closing socket connection and attempting reconnect
java.io.IOException: Packet len5605464 is out of range!
        at org.apache.zookeeper.ClientCnxn$SendThread.readLength(ClientCnxn.java:710)
        at org.apache.zookeeper.ClientCnxn$SendThread.doIO(ClientCnxn.java:869)
        at org.apache.zookeeper.ClientCnxn$SendThread.run(ClientCnxn.java:1130)
```

<!--more-->

### 分析问题

根据错误提示，`java.io.IOException: Packet len8854970 is out of range!`，out of range就是超过了某个限制，查看源码。

根据相应的关键词，找到报错的类：[ClientCnxnSocket.java](https://github.com/apache/zookeeper/blob/master/zookeeper-server/src/main/java/org/apache/zookeeper/ClientCnxnSocket.java)

对应方法如下：

```java
private int packetLen = ZKClientConfig.CLIENT_MAX_PACKET_LENGTH_DEFAULT;

protected void initProperties() throws IOException {
    try {
        packetLen = clientConfig.getInt(
            ZKConfig.JUTE_MAXBUFFER,
            ZKClientConfig.CLIENT_MAX_PACKET_LENGTH_DEFAULT);
        LOG.info("{} value is {} Bytes", ZKConfig.JUTE_MAXBUFFER, packetLen);
    } catch (NumberFormatException e) {
        String msg = MessageFormat.format(
            "Configured value {0} for property {1} can not be parsed to int",
            clientConfig.getProperty(ZKConfig.JUTE_MAXBUFFER),
            ZKConfig.JUTE_MAXBUFFER);
        LOG.error(msg);
        throw new IOException(msg);
    }
}

void readLength() throws IOException {
    int len = incomingBuffer.getInt();
    if (len < 0 || len >= packetLen) {
        throw new IOException("Packet len " + len + " is out of range!");
    }
    incomingBuffer = ByteBuffer.allocate(len);
}
```

其中，[ZKConfig.JUTE_MAXBUFFER](https://github.com/apache/zookeeper/blob/master/zookeeper-server/src/main/java/org/apache/zookeeper/common/ZKConfig.java#L45) 的定义如下

```java
public static final String JUTE_MAXBUFFER = "jute.maxbuffer";
```

默认值 [ZKClientConfig.CLIENT_MAX_PACKET_LENGTH_DEFAULT](https://github.com/apache/zookeeper/blob/master/zookeeper-server/src/main/java/org/apache/zookeeper/client/ZKClientConfig.java#L60) 为：

```java
public static final int CLIENT_MAX_PACKET_LENGTH_DEFAULT = 0xfffff; /* 1 MB */
```

从代码就能够很容易的看出，这个错误是因为`len`小于0或大于`packetLen`，根据代码逻辑，`len`不小于0，那就是大于`packetLen`。

而 `packetLen`的值是`jute.maxbuffer`系统变量定义或默认的 4096 * 1024（4M）。

16进制的 `0xfffff` 为 10 进制的 `1048575`，即 1M。

源码的大体逻辑就是，创建与zookeeper连接之后，要对某个节点进行读写操作，为了提高吞吐量，先判断下该节点数据量大小是否超过设置的`jute.maxbuffer`，如果是，就抛出异常。

### 解决问题

根据上面的纠错，答案就很明显了。只有两种方案：

- 把待操作节点的大小减下来，小于默认的4M
- 把默认的`jute.maxbuffer`大小提高

对于第一种方式，需要根据自身具体情况具体操作。这里没有什么有效建议。

对于第二种方式，server 和 client 根据情况进行修改，解决方案如下：

#### 服务端

zkServer修改配置文件，增加内存配置 `jute.maxbuffer`，重启zk使配置生效。

```shell
vim zoo.cfg
jute.maxbuffer=0x400000 #增加此配置到 4M 内存
```

#### 客户端

client 端启动的时候增加参数

```shell
JAVA_OPTS=" -Djute.maxbuffer=0x400000 "
```