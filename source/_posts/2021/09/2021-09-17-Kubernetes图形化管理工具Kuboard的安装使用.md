---
title: Kubernetes图形化管理工具Kuboard的安装使用
layout: info
commentable: true
date: 2021-09-17
mathjax: true
mermaid: true
tags: [Container,Kubernetes]
categories: [Container,Kubernetes]
description: 
---

### Kuboard 简介

Kuboard，是一款免费的 Kubernetes 图形化管理工具，Kuboard 力图帮助用户快速在 Kubernetes 上落地微服务，Kubernetes 容器编排已越来越被大家关注，然而使用 Kubernetes 的门槛却依然很高，主要体现在这几个方面：

- 集群的安装复杂，出错概率大
- Kubernetes相较于容器化，引入了许多新的概念，学习难度高
- 需要手工编写 YAML 文件，难以在多环境下管理
- 缺少好的实战案例可以参考

#### Kuboard 特点

- 无需编写YAML
- 纯图形化环境
- 多环境管理

#### 相关文档

- 官网：https://www.kuboard.cn/
- 安装文档：https://www.kuboard.cn/install/v3/install.html

### 安装工程

在线安装：

```
kubectl apply -f https://addons.kuboard.cn/kuboard/kuboard-v3.yaml
```

### 访问 Kuboard

- 在浏览器中打开链接 `http://your-node-ip-address:30080`
- 输入初始用户名和密码，并登录
  - 用户名： `admin`
  - 密码： `Kuboard123`