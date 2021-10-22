---
title: docker命令批量删除状态为Exited的容器
layout: info
commentable: true
date: 2021-10-18
mathjax: true
mermaid: true
tags: [Container,Docker]
categories: [Container,Docker]
description: 
---

docker启动的容器当中，经常有一些退出的容器，既然没有用了，就需要批量清理一下。

命令：

```
docker rm $(docker ps -q -f status=exited)
```

解释： 利用docker ps -f选项可以找到exited的容器 -q 只显示容器id 。

这样就可以批量删除了！

