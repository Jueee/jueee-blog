---
title: docker私有化部署Hoppscotch
layout: info
commentable: true
date: 2023-04-26
mathjax: true
mermaid: true
tags: [Blog]
categories: Blog
description: 
---

Hoppscotch 是一种可以通过 Web 服务的方式构建 API 访问的工具，使用 Node.js 开发，采用简约的 UI 设计，能实时发送和获取响应值，它的的前身是 Postwoman。

<!--more-->

### Hoppscotch 介绍

- 官网：https://hoppscotch.io/
- GitHub：https://github.com/hoppscotch/hoppscotch
- DockerHub：https://hub.docker.com/r/hoppscotch/hoppscotch
- 文档：https://docs.hoppscotch.io/

### docker 私有化部署

```
docker run --name hoppscotch -p 3000:3000 -d hoppscotch/hoppscotch:latest
```

访问服务：http://IP:3000/

### 搭建 hoppscotch 代理

访问 hoppscotch 的 web 页面配置代理，修改对应 ip。

```
docker run -d --name hoppscotch-proxy -p 9159:9159  hoppscotch/proxyscotch
```

![image-20230426152723014](assets/image-20230426152723014.png)

修改后，再次发送请求就可以了。

### 使用浏览器扩展

安装地址：[Chrome插件](https://chrome.google.com/webstore/detail/hoppscotch-browser-extens/amknoiejhlmhancpahfcfcfhllgkpbld/related)

#### 配置插件

插件安装完成后，点击插件图标，点击 Add，添加 origin 地址（部署的服务器地址），以支持跨站请求。

<img src="assets/image-20230426152136503.png" alt="image-20230426152136503" style="zoom: 67%;" />

在 web 页面开启使用浏览器扩展。

<img src="assets/image-20230426152244995.png" alt="image-20230426152244995" style="zoom: 67%;" />
