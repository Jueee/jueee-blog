---
title: 在eclipse中安装lombok.jar
layout: info
commentable: true
date: 2020-09-21
mathjax: true
mermaid: true
tags: [eclipse,IDE,软件]
categories: [软件,IDE]
description: 
---

### 下载

**下载lombok.jar（一定要最新版）**

下载地址：https://projectlombok.org/download

<!--more-->

### 安装

1. **复制lombok.jar到eclipse.ini所在目录**

2. **安装lombok.jar**：shift+右键唤出命令窗口，运行**java -jar lombok.jar**  或者 直接双击lombok.jar（后者操作更简单）

   ![image-20200921103421844](assets/image-20200921103421844.png)

3. 选择 eclipse.exe：
   ![image-20200921103504337](assets/image-20200921103504337.png)

4. 确认 eclipse.exe：![image-20200921103526313](assets/image-20200921103526313.png)

5. 快速安装：
   ![image-20200921103543338](assets/image-20200921103543338.png)

6. 操作完成后发现eclipse.ini多了一行配置：
   ![image-20200921103619161](assets/image-20200921103619161.png)

### **安装成功后操作** 

重启eclipse并刷新项目，之前报错的set() get()等方法不再报错。

### **注意事项**

lombok.jar一定要从官网下载最新，否则安装后get() set()等方法仍会报错。