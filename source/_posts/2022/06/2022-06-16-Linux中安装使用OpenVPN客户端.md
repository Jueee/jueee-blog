---
title: Linux中安装使用OpenVPN客户端
layout: info
commentable: true
date: 2022-06-16
mathjax: true
mermaid: true
tags: [软件,Linux]
categories: [软件,Linux]
description: 
---

### 安装 OpenVPN

```
apt-get install openvpn -y
```

<!--more-->

### 使用 OpenVPN

```
#! /bin/bash

sudo openvpn  --config /etc/openvpn/config/vpn.ovpn --daemon --log-append /var/log/openvpn.log
```

### 异常处理

如果出现报错：

```
Thu Aug 18 17:46:48 2022 ERROR: Cannot ioctl TUNSETIFF tun: Operation not permitted (errno=1)
Thu Aug 18 17:46:48 2022 Exiting due to fatal error
```

其实只要使用  sudo openvpn client.ovpn 就可以了。

### 下载地址

https://build.openvpn.net/downloads/releases/
