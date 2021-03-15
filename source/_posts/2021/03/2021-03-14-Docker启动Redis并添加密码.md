---
title: Docker启动Redis并添加密码
layout: info
commentable: true
date: 2021-03-14
mathjax: true
mermaid: true
tags: [Container,Docker,Kubernets,Redis]
categories: 
- [Container,Docker]
- [Database,Redis]
description: 
---

可以使用密码启动Redis服务器。使用的命令是：

```bash
redis-server --requirepass mypassword
```

本文介绍在容器中对 Redis 添加密码的方法。

<!--more-->

### Docker 设置密码

```bash
docker run --name myredis -p 6379:6379 -d redis --requirepass "mypassword"
```

### docker-compose 设置密码

```yaml
services:
  redis:
    container_name: 'myredis'
    image: 'redis'
    restart: always
    ports:
      - 6379:6379
    command: redis-server --requirepass mypassword
```

### Kubernets 设置密码

创建redis配置configmaps：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-conf
data:
  redis.conf: |
        bind 0.0.0.0
        port 6379
        requirepass mypassword
```

创建StatefulSet时启动参数配置：

```yaml
spec:
	containers:
	  - name: redis-server
		image: redis:latest
		imagePullPolicy: Always
		command:
		- redis-server
		args:
		- --requirepass
		- mypassword
```

### 密码访问 Redis

```
$ redis-cli
127.0.0.1:6379> RANDOMKEY
(error) NOAUTH Authentication required.
127.0.0.1:6379> auth mypassword
OK
127.0.0.1:6379> RANDOMKEY
(nil)
```

