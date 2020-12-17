---
title: Zookeeper简要介绍及单机版安装
layout: info
commentable: true
date: 2020-12-16
mathjax: true
mermaid: true
tags: [Apache,Zookeeper]
categories: [Apache,Zookeeper]
description: 
---

### Zookeeper 介绍

ZooKeeper是Hadoop的正式子项目，它是一个针对大型分布式系统的可靠协调系统，提供的功能包括：配置维护、名字服务、分布式同步、组服务等。

ZooKeeper的目标就是封装好复杂易出错的关键服务，将简单易用的接口和性能高效、功能稳定的系统提供给用户。

- 官网：https://zookeeper.apache.org/index.html
- 下载：https://zookeeper.apache.org/releases.html
- GitHub：https://github.com/apache/zookeeper

<!--more-->

### Zookeeper 单机版安装

1. 下载

   ```bash
   wget http://mirror.bit.edu.cn/apache/zookeeper/zookeeper-3.4.14/zookeeper-3.4.14.tar.gz 
   ```

2. 解压

   ```bash
   tar -xvf zookeeper-3.4.14.tar.gz
   ```

3. 修改配置文件 `zookeeper-3.4.14/conf/zoo.cfg `

   ```bash
   tickTime=2000
   dataDir=/home/dir/zookeeper-3.4.14/zklog
   clientPort=2181
   initLimit=30
   syncLimit=15
   maxClientCnxns=1000
   ```

4. 启动服务端

   ```bash
   ~/zookeeper-3.4.14/bin$ ./zkServer.sh start
   ```

5. 客户端连接

   ```bash
   ~/zookeeper-3.4.14/bin$ ./zkCli.sh
   ```

   客户端远程连接

   ```bash
   ~/zookeeper-3.4.14/bin$ ./zkCli.sh -server 192.168.0.1:2181
   ```

### 服务端常用命令

- 启动 ZK 服务: sh bin/zkServer.sh start
- 查看 ZK 服务状态: sh bin/zkServer.sh status
- 停止 ZK 服务: sh bin/zkServer.sh stop
- 重启 ZK 服务: sh bin/zkServer.sh restart

### 客户端常用命令

使用 zkCli.sh -server **ip:port** 连接到 ZooKeeper 服务，连接成功后，系统会输 出 ZooKeeper 的相关环境以及配置信息。 

命令行工具的一些简单操作如下:

- 显示根目录下、文件：ls/ 使用ls命令来查看当前ZooKeeper中所包含的内容

  ```bash
  $ ls /dubbo/com.alibaba.dubbo.monitor.MonitorService
  [consumers, routers, providers, configurators]
  ```

- 显示根目录下、文件：ls2 / 查看当前节点数据并能看到更新次数等数据

  ```bash
  $ ls2 /dubbo/com.alibaba.dubbo.monitor.MonitorService
  [consumers, routers, providers, configurators]
  cZxid = 0x27f017fae11
  ctime = Wed Dec 16 14:03:48 CST 2020
  mZxid = 0x27f017fae11
  mtime = Wed Dec 16 14:03:48 CST 2020
  pZxid = 0x27f017fae23
  cversion = 4
  dataVersion = 0
  aclVersion = 0
  ephemeralOwner = 0x0
  dataLength = 12
  numChildren = 4
  ```

- 创建文件，并设置初始内容: create /zk “test” 创建一个新的 znode 节点“ zk ”以及与它关联的字符串 [-e] [-s] 【-e 零时节点】 【-s 顺序节点】

- 获取文件内容：get /zk 确认 znode 是否包含我们所创建的字符串 [watch【] watch 监听】

  ```bash
  $ get /dubbo/com.alibaba.dubbo.monitor.MonitorService/consumers
  10.110.20.22
  cZxid = 0x27f017fae1c
  ctime = Wed Dec 16 14:03:48 CST 2020
  mZxid = 0x27f017fae1c
  mtime = Wed Dec 16 14:03:48 CST 2020
  pZxid = 0x27f017fae1c
  cversion = 0
  dataVersion = 0
  aclVersion = 0
  ephemeralOwner = 0x0
  dataLength = 12
  numChildren = 0
  ```

  - cZxid：节点创建时的zxid
  - ctime：节点创建时间
  - mZxid：节点最近一次更新时的zxid
  - mtime：节点最近一次更新的时间
  - cversion：子节点数据更新次数
  - dataVersion：本节点数据更新次数
  - aclVersion：节点ACL(授权信息)的更新次数
  - ephemeralOwner：如果该节点为临时节点,ephemeralOwner值表示与该节点绑定的session id. 如果该节点不是临时节点,ephemeralOwner值为0
  - dataLength：节点数据长度，本例中为hello world的长度
  - numChildren：子节点个数

- 修改文件内容：set /zk “zkbak” 对 zk 所关联的字符串进行设置

- 删除文件：delete/zk 将刚才创建的znode删除，如果存在子节点删除失败

- 递归删除：rmr /zk 将刚才创建的znode删除，子节点同时删除

- 退出客户端：quit

  ```bash
  $ quit
  Quitting...
  2020-12-16 19:14:08,550 [myid:] - INFO  [main:ZooKeeper@684] - Session: 0x3766a4749cc00e8 closed
  2020-12-16 19:14:08,550 [myid:] - INFO  [main-EventThread:ClientCnxn$EventThread@512] - EventThread shut down
  ```

- 帮助命令：help

  ```bash
  $ help
  ZooKeeper -server host:port cmd args
          connect host:port
          get path [watch]
          ls path [watch]
          set path data [version]
          rmr path
          delquota [-n|-b] path
          quit
          printwatches on|off
          create [-s] [-e] path data acl
          stat path [watch]
          close
          ls2 path [watch]
          history
          listquota path
          setAcl path acl
          getAcl path
          sync path
          redo cmdno
          addauth scheme auth
          delete path [version]
          setquota -n|-b val path
  ```

  



