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

### 使用 OpenVPN

```
openvpn  --config /etc/openvpn/config/vpn.ovpn --daemon --log-append /var/log/openvpn.log
```

