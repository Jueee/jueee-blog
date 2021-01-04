---
title: Zeppelin配置连接MySQL数据库
layout: info
commentable: true
date: 2020-12-30
mathjax: true
mermaid: true
tags: [Apache,Zeppelin,MySQL]
categories: 
- [Apache,Zeppelin]
- [Database,MySQL]
description: 
---

Zeppelin 原生支持JDBC链接。 但是默认的设置是指向PostgreSQL。

一种最简单的办法就是直接修改JDBC Interpreter里面的内容，指向你自己的MySQL实例即可。

本文介绍如何创建 MySQL Interpreter 并连接。

<!--more-->

### 访问 Zeppelin

搭建安装好 Zeppelin 后，访问 http://127.0.0.1:8080/#/ 。结果如下：

![image-20201230143530356](/images/2020/12/image-20201230143530356.png)

### 创建 MySQL Interpreters

1. 选择 Interpreters

   ![image-20201230143619751](/images/2020/12/image-20201230143619751.png)

2. 点击 Create 进行创建

   ![image-20201230143656818](/images/2020/12/image-20201230143656818.png)

3. 配置解析器名称，注意解析器所属组选择 “jdbc”

   ![image-20201230143831845](/images/2020/12/image-20201230143831845.png)

4. 配置 jdbc 连接属性

   ![image-20201230144116469](/images/2020/12/image-20201230144116469.png)

5. 设置依赖 MySQL 驱动，这里选择 `mysql:mysql-connector-java:8.0.22`。

   ![image-20201230144218765](/images/2020/12/image-20201230144218765.png)

6. 检查没有问题后，点击 Save 保存。

### 创建 MySQL NoteBook

1. 选择创建  NoteBook

   ![image-20201230144519005](/images/2020/12/image-20201230144519005.png)

2. 设置 NoteBook 名称，Interpreters 选择上面创建的 “mysql-Interpreters”。

   ![image-20201230144431472](/images/2020/12/image-20201230144431472.png)

3. 输入 SQL，并点击执行，即可查看 执行结果 table。

   ![image-20201230144757351](/images/2020/12/image-20201230144757351.png)

4. 选择 Bar Chart，并现在 keys 为 “statday”，values 为 “cnt”，即可查看相应的图表。

   ![image-20201230144858229](/images/2020/12/image-20201230144858229.png)

5. 饼图、折线图等，与柱状图类似。不赘述。