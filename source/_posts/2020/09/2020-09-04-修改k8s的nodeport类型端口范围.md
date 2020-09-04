---
title: 修改k8s的nodeport类型端口范围
layout: info
commentable: true
date: 2020-09-04
mathjax: true
mermaid: true
tags: [k8s]
categories: k8s
description: 
---

### 出现问题

在 Kubernetes(k8s) 创建 service 使用nodePort 暴露 外部端口8192时报错：

> The Service "web-admin" is invalid: spec.ports[0].nodePort: Invalid value: 8192: provided port is not in the valid range. The range of valid ports is 30000-32767

<!--more-->

### 解决方案

编辑 `kube-apiserver.yaml`文件

```
vim /etc/kubernetes/manifests/kube-apiserver.yaml
```

找到 `--service-cluster-ip-range` 这一行，在这一行的下一行增加 如下内容

```
- --service-node-port-range=1-65535
```

最后修改效果如下：

![1599200375796](/images/2020/09/1599200375796.png)

最后 重启 kubelet

```powershell
systemctl daemon-reload
systemctl restart kubelet
```