---
title: 解决group_concat默认长度限制问题
layout: info
commentable: true
date: 2022-11-21
mathjax: true
mermaid: true
tags: [Database,MySQL]
categories: [Database,MySQL]
description: 
---

GROUP_CONCAT有个最大长度的限制，超过最大长度就会被截断掉

<!--more-->

### 获取长度

可以通过下面的语句获得长度：

```mysql
SELECT @@global.group_concat_max_len;
show variables like 'group_concat_max_len';
```

### 设置长度

使用以下语句设置：

```mysql
SET GLOBAL group_concat_max_len=102400;
SET SESSION group_concat_max_len=102400;
```

### 配置设置

在MySQL配置文件中 my.conf 或 my.ini 中添加:

```ini
[mysqld]
　　group_concat_max_len=102400
```

重启MySQL服务。
