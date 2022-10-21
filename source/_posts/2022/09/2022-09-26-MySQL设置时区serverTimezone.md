---
title: MySQL设置时区serverTimezone
layout: info
commentable: true
date: 2022-09-26
mathjax: true
mermaid: true
tags: [Database,MySQL]
categories: [Database,MySQL]
description: 
---

### UTC

UTC，简称世界统一时间，跟北京时间相比，比北京早8个小时。

如果你设置serverTimezone=UTC，连接不报错，但是我们在用java代码插入到数据库时间的时候却出现了问题。

比如在java代码里面插入的时间为：2022-09-26 09:44:12

但是在数据库里面显示的时间却为：2022-09-26 01:44:12

有了8个小时的时差。

### 设置国内时间

东八区时间：

```
serverTimezone=GMT%2B8
```

上海时间：

```
serverTimezone=Asia/Shanghai
```

