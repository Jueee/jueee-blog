---
title: k8s删除pod一直处于terminating状态
layout: info
commentable: true
date: 2021-02-20
mathjax: true
mermaid: true
tags: [k8s]
categories: 
- [Container,Kubernets]
description: 
---

若 k8s 删除 pod 一直处于 terminating 状态

可强制删除：

```
kubectl delete pod PODNAME --force --grace-period=0
```