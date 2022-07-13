---
title: MAC的Chrome提示您的连接不是私密连接
layout: info
commentable: true
date: 2022-07-05
mathjax: true
mermaid: true
tags: [OS，Mac]
categories: [OS，Mac]
description: 
---

### 问题描述

Mac 版本的Chrome访问未认证的https链接时，会提示您的连接不是私密连接。

<!--more-->

![image-20220705164011373](/images/2022/07/image-20220705164011373.png)

### 短期方案

1. 浏览器停留在当前页面。
2. 在键盘直接敲击 “**thisisunsafe**”，不用管在哪里显示，就默默的打出“**thisisunsafe**”就好了。
3. 输入完成后，页面直接就会刷新了，就可以正常访问了。

### 长期方案

输入 thisisunsafe（刷新页面后，手动输入 thisisunsafe 后即可）是短期方案。

但是每次总输入这么一长串，比较麻烦，搜了一下没找到方案，遂记录一下。

mac 下打开 /Applications/Google Chrome.app/Contents/MacOS 后，看到了有一个Google Chrome的二进制文件，类似下图：

![image-20220705164755237](/images/2022/07/image-20220705164755237.png)

#### 修改方案

替换掉这个Google Chrome的二进制文件，然后生成一个bash文件，依旧启动之前的二进制文件，并添加参数--ignore-certificate-errors 即可。

#### 操作命令

操作如下三条命令：

- mv Google Chrome Google.real 

  把原先的二进制文件重命名

- vi Google Chrome 

  新建Google Chrome，输入

  ```
  /Applications/Google\ Chrome.app/Contents/MacOS/Google.real --ignore-certificate-errors
  ```

- chmod 777 Google Chrome

重启chrome即可。

当然windows下直接右键修改快捷方式，添加--ignore-certificate-errors即可。
