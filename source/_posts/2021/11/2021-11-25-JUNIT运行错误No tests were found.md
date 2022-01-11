---

title: JUNIT运行错误No tests were found
layout: info
commentable: true
date: 2021-11-25
mathjax: true
mermaid: true
tags: [Java]
categories: Java
description: 
---

### 问题描述

![image-20211125145714774](/images/2021/11/image-20211125145714774.png)

### 问题分析

1. 进行单元测试的方法不能有返回值，否则会报 No test were found
2. 进行单元测试的方法不能私有化
3. Junit 版本问题

### 解决方案

1. 去掉单元测试的方法的返回值。
2. 如果单元测试方法前有 `private` 等修饰符，需要去掉。

如下图所示：

![image-20211125145846332](/images/2021/11/image-20211125145846332.png)

