---
title: SpringBoot集成Zookeeper
layout: info
commentable: true
date: 2020-12-19
mathjax: true
mermaid: true
tags: [Apache,Zookeeper,SpringBoot]
categories: 
- [Apache,Zookeeper]
- [Java,JavaJar]
- [Java,SpringBoot]
description: 
---

### 引入依赖

pom.xml 引入Zookeeper依赖

```xml
<dependency>
    <groupId>org.apache.zookeeper</groupId>
    <artifactId>zookeeper</artifactId>
    <version>3.4.14</version>
</dependency>
```

<!--more-->

### 添加配置

在 `application.properties` 文件中添加 zookeeper 配置：

```properties
zookeeper.address=127.0.0.1:2181
zookeeper.timeout=4000
```

### 连接配置类

新建ZookeeperConfig连接配置类

```java
import lombok.extern.slf4j.Slf4j;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.CountDownLatch;

@Slf4j
@Configuration
public class ZookeeperConfig {

    @Value("${zookeeper.address}")
    private String connectString;

    @Value("${zookeeper.timeout}")
    private int timeout;

    @Bean(name = "zkClient")
    public ZooKeeper zkClient(){
        ZooKeeper zooKeeper=null;
        try {
            final CountDownLatch countDownLatch = new CountDownLatch(1);
            // 连接成功后，会回调watcher监听，此连接操作是异步的，执行完new语句后，直接调用后续代码
            // 可指定多台服务地址 127.0.0.1:2181,127.0.0.1:2182,127.0.0.1:2183
            zooKeeper = new ZooKeeper(connectString, timeout, new Watcher() {
                @Override
                public void process(WatchedEvent event) {
                    if(Event.KeeperState.SyncConnected==event.getState()){
                        //如果收到了服务端的响应事件,连接成功
                        countDownLatch.countDown();
                    }
                }
            });
            countDownLatch.await();
            log.info("【初始化ZooKeeper连接状态....】={}",zooKeeper.getState()); // CONNECTED
        }catch (Exception e){
            log.error("初始化ZooKeeper连接异常....】={}",e);
        }
        return  zooKeeper;
    }
}
```

### 封装工具类

#### 获取子节点

获取当前节点的子节点(不包含孙子节点)

```java
public List<String> getChildren(String path) throws KeeperException, InterruptedException{
    List<String> list = zkClient.getChildren(path, false);
    return list;
}
```

#### 创建节点

创建持久化节点

```java
public boolean createNode(String path, String data){
    try {
        zkClient.create(path,data.getBytes(), ZooDefs.Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
        return true;
    } catch (Exception e) {
        log.error("【创建持久化节点异常】{},{},{}",path,data,e);
        return false;
    }
}
```

#### 修改节点

修改持久化节点

```java
public boolean updateNode(String path, String data){
    try {
        //zk的数据版本是从0开始计数的。如果客户端传入的是-1，则表示zk服务器需要基于最新的数据进行更新。
        //如果对zk的数据节点的更新操作没有原子性要求则可以使用-1.
        //version参数指定要更新的数据的版本, 如果version和真实的版本不同, 更新操作将失败. 指定version为-1则忽略版本检查
        zkClient.setData(path,data.getBytes(),-1);
        return true;
    } catch (Exception e) {
        log.error("【修改持久化节点异常】{},{},{}",path,data,e);
        return false;
    }
}
```

#### 获取节点值

获取指定节点的值

```java
public  String getData(String path, Watcher watcher){
    try {
        Stat stat=new Stat();
        byte[] bytes=zkClient.getData(path,watcher,stat);
        return  new String(bytes);
    }catch (Exception e){
        e.printStackTrace();
        return  null;
    }
}
```

#### 判断节点是否存在

判断指定节点是否存在

```java
// @param needWatch  指定是否复用zookeeper中默认的Watcher
public Stat exists(String path, boolean needWatch){
    try {
        return zkClient.exists(path,needWatch);
    } catch (Exception e) {
        log.error("【断指定节点是否存在异常】{},{}",path,e);
        return null;
    }
}

// 检测结点是否存在 并设置监听事件（三种监听类型： 创建，删除，更新）
// @param watcher  传入指定的监听类
public Stat exists(String path,Watcher watcher ){
    try {
        return zkClient.exists(path,watcher);
    } catch (Exception e) {
        log.error("【断指定节点是否存在异常】{},{}",path,e);
        return null;
    }
}
```

返回的 Stat 节点示例如下：

```java
log.info("[isExists]"+isExists.toString());
// [isExists]262,262,1608169108777,1608169108777,0,0,0,0,8,0,262
```

这几个数字对应的类型分别如下：

```java
public String toString() {
    try {
        ByteArrayOutputStream s = new ByteArrayOutputStream();
        CsvOutputArchive a_ = new CsvOutputArchive(s);
        a_.startRecord(this, "");
        a_.writeLong(this.czxid, "czxid"); // Zookeeper为节点分配的Id
        a_.writeLong(this.mzxid, "mzxid"); // 修改后的id
        a_.writeLong(this.ctime, "ctime"); // 节点创建时间
        a_.writeLong(this.mtime, "mtime"); // 修改时间
        a_.writeInt(this.version, "version"); // 节点的更新次数
        a_.writeInt(this.cversion, "cversion"); // 子节点的更新次数
        a_.writeInt(this.aversion, "aversion"); // 节点ACL(授权信息)的更新次数
        a_.writeLong(this.ephemeralOwner, "ephemeralOwner"); // 如果该节点为临时节点,ephemeralOwner值表示与该节点绑定的session id. 如果该节点不是临时节点,ephemeralOwner值为0
        a_.writeInt(this.dataLength, "dataLength"); // 数据长度
        a_.writeInt(this.numChildren, "numChildren"); // 子节点个数
        a_.writeLong(this.pzxid, "pzxid");
        a_.endRecord(this, "");
        return new String(s.toByteArray(), "UTF-8");
    } catch (Throwable var3) {
        var3.printStackTrace();
        return "ERROR";
    }
}
```

与 get 或 stat 命令行的返回结果一致：

```bash
$ get /test
testdata
cZxid = 0x106
ctime = Thu Dec 17 09:38:28 CST 2020
mZxid = 0x106
mtime = Thu Dec 17 09:38:28 CST 2020
pZxid = 0x106
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 8
numChildren = 0
$ stat /test
cZxid = 0x106
ctime = Thu Dec 17 09:38:28 CST 2020
mZxid = 0x106
mtime = Thu Dec 17 09:38:28 CST 2020
pZxid = 0x106
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x0
dataLength = 8
numChildren = 0
```

#### 删除节点

删除持久化节点

```java
public boolean deleteNode(String path){
    try {
        //version参数指定要更新的数据的版本, 如果version和真实的版本不同, 更新操作将失败. 指定version为-1则忽略版本检查
        zkClient.delete(path,-1);
        return true;
    } catch (Exception e) {
        log.error("【删除持久化节点异常】{},{}",path,e);
        return false;
    }
}
```

### 自定义监听

```java
import lombok.extern.slf4j.Slf4j;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;

@Slf4j
public class ZookeeperWatcher implements Watcher {
    @Override
    public void process(WatchedEvent event) {
        log.info("【Watcher监听事件】={}",event.getState());
        log.info("【监听路径为】={}",event.getPath());
        log.info("【监听的类型为】={}",event.getType()); //  三种监听类型： 创建，删除，更新
    }
}
```

删除节点时，打印结果为：

```
【监听的类型为】=NodeDeleted
【Watcher监听事件】=SyncConnected
【监听路径为】=/test
【监听的类型为】=NodeDeleted
```

event.getState() 的 返回类型见 [Watcher.KeeperState](https://github.com/apache/zookeeper/blob/master/zookeeper-server/src/main/java/org/apache/zookeeper/Watcher.java) 子类。

event.getType() 的 返回类型见 [Watcher.EventType](https://github.com/apache/zookeeper/blob/master/zookeeper-server/src/main/java/org/apache/zookeeper/Watcher.java) 子类。