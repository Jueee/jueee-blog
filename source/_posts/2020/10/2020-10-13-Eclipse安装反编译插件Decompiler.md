---
title: Eclipse 安装反编译插件 Decompiler 
layout: info
commentable: true
date: 2020-10-13
mathjax: true
mermaid: true
tags: [软件,Eclipse,Java,IDE]
categories: [软件,IDE]
description: 
---

### Decompiler 插件介绍

增强的类反编译器将 JD，Jad，FernFlower，CFR，Procyon与Eclipse无缝集成，并允许Java开发人员直接调试类文件而无需源代码。

插件官网：http://marketplace.eclipse.org/content/enhanced-class-decompiler

<!--more-->

### Decompiler 插件安装

1. 打开：Help——Eclipse Marketplace

2. 搜索 jad、Decompiler 、或者反编译：

   ![image-20201021172812160](/images/2020/10/image-20201021172812160.png)

3. 点击 Installed，进行安装。

4. 安装完成后，重启 Eclipse。插件安装完成。

   ![image-20201021173703398](/images/2020/10/image-20201021173703398.png)

### Decompiler 插件配置

1. 设置*.class文件类型默认打开方式，如图所示：

   ![image-20201021173142275](/images/2020/10/image-20201021173142275.png)

2. 设置*.class without source文件类型打开方式，如图所示

   ![image-20201021173203007](/images/2020/10/image-20201021173203007.png)

3. 最后，点击 Apply and Close。就可以直接打开.class文件进行查看了。

4. 插件提供了系统菜单，工具栏，当打开了插件提供的类反编译查看器后，会激活菜单和工具栏选项，可以方便的进行首选项配置，切换反编译工具重新反编译，以及导出反编译结果。

   菜单：

   ![image-20201021174246707](/images/2020/10/image-20201021174246707.png)

   工具栏选项：

   ![image-20201021174505200](/images/2020/10/image-20201021174505200.png)







