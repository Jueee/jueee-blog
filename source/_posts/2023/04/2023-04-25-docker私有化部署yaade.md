---
title: docker私有化部署yaade
layout: info
commentable: true
date: 2023-04-25
mathjax: true
mermaid: true
tags: [Blog]
categories: Blog
description: 
---

### yaade 

- GitHub：https://github.com/EsperoTech/yaade
- 文档：https://docs.yaade.io/getting-started.html

<!--more-->

### docker 部署

```
docker pull esperotech/yaade:latest
docker run -d --restart=always -p 9339:9339 -e YAADE_ADMIN_USERNAME=admin --name yaade esperotech/yaade:latest
```

#### 数据持久化

```
docker volume create yaade
docker run -d --restart=always -p 9339:9339 \
    -e YAADE_ADMIN_USERNAME=admin -v yaade:/app/data \
    --name yaade esperotech/yaade:latest
```



本地目录：

```
docker cp yaade:/app/data ./
docker run -d --restart=always -p 9339:9339 -e YAADE_ADMIN_USERNAME=admin -v /home/yaade/data:/app/data --name yaade esperotech/yaade:latest
```





<img src="assets/image-20230426154130050.png" alt="image-20230426154130050" style="zoom:50%;" />

#### 安装插件

插件地址：[Chrome插件](https://chrome.google.com/webstore/detail/yaade-extension/mddoackclclnbkmofficmmepfnadolfa/related)

<img src="assets/image-20230426154530201.png" alt="image-20230426154530201" style="zoom: 67%;" />

### 用户管理

#### 创建用户

新的用户，密码默认为 password：

![image-20230426155519337](assets/image-20230426155519337.png)

