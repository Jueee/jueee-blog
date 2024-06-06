---
title: 页面跳转报错This request has been blocked； the content must be served over HTTPS
layout: info
commentable: true
date: 2023-05-10
mathjax: true
mermaid: true
tags: [HTML]
categories: HTML
description: 
---

JS 报错：
**This request has been blocked; the content must be served over HTTPS**

<!--more-->

### 详细报错

详细报错内容如下：

```
Mixed Content: The page at 'https://xxx/mainfrane' was loaded over HTTPS, but requested an insecure forn action 'http://xxx/student/exan'. This request has been blocked; the content must be served over HTTPS.
```

![image-20230510183758642](assets/image-20230510183758642.png)

### 报错原因

http、https混合导致的

网站用的是 https 要跳转到 http 请求，被阻止了。

### 解决方法

1.页面中都是用 https ，或者都使用 http

2.在 <head> 标签中添加以下代码

```
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests"/>
```

意思是自动将http的不安全请求升级为https。
