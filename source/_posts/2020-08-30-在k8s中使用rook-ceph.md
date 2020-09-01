---
title: 在k8s中使用rook-ceph
layout: info
commentable: true
date: 2020-08-30
mathjax: true
mermaid: true
tags: [k8s,Ceph]
categories: Ceph
description: 
---
### 相关链接

rook-ceph官方指导：

> https://rook.io/docs/rook/v1.1/ceph-examples.html 

github项目地址：

> https://github.com/rook/rook/tree/master/cluster/examples/kubernetes/ceph 

<!--more-->

### rook-ceph-tools使用

1. 执行toolbox.yaml，生成rook-ceph-tools-xxxx pod

2. 使用如下命令进入ceph的管理中：

   ```shell
   $ kubectl -n rook-ceph exec -it $(kubectl -n rook-ceph get pod -l "app=rook-ceph-tools" -o jsonpath='{.items[0].metadata.name}') bash
   ```

   ```shell
   $ kubectl exec -it rook-ceph-tools-9c9d7744b-2tpwn bash -n rook-ceph
   ```

3. ceph常用命令

   ```
   ceph -s 查看集群状态
   ceph osd status 查看osd状态
   ceph pg stat 查看pg状态
   ceph osd pool set pool pg_num 64 设置pg数量
   ceph osd pool set pool pgp_num 64 设置pgp数量，在集群规模较小，pg数量过少会导致监控警告，此两条命令需一起使用
   ```

### 在宿主机使用 ceph 命令行

1. 安装 `ceph-common`：`apt-get install ceph-common`。
2. 进入 `rook-ceph-tools-9c9d7744b-2tpwn` 容器，将 `/etc/ceph/ceph.conf` 和 `/etc/ceph/keyring` 拷贝到宿主机的 `/etc/ceph/` 文件夹下即可。

### 问题处理

```
(combined from similar events): MountVolume.SetUp failed for volume "mysqldata" : CephFS: mount failed: mount failed: exit status 32
```



https://pkgs.org/download/ceph-common

https://blog.51cto.com/leejia/2501080

