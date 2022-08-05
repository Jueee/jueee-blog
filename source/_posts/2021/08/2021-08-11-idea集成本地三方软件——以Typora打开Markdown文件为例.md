---
title: idea集成本地三方软件——以Typora打开Markdown文件为例
layout: info
commentable: true
date: 2021-08-11
mathjax: true
mermaid: true
tags: [Blog]
categories: Blog
description: 
---

### 官方教程

> https://www.jetbrains.com/help/idea/configuring-third-party-tools.html

### Idea配置

#### External Tools

需要先进入到Idea设置界面。

路径如下：【Settings】——【Tools】——【External Tools】，之后再点击 + 号（如图所示）

![image-20210811100557832](/images/2021/08/image-20210811100557832.png)

关于 External Tools 界面各参数含义，可以参看如下内容：

- Name: 在IntelliJ IDEA界面中显示的工具名称
- Group: 工具所属的组的名称。您可以选择一个现有组或新创建一个组
- Description: 对本工具的描述
- Program: 应用程序可执行文件的路径
- Arguments: 传递给可执行文件的参数
- Working directory: 执行工具的当前工作目录的路径。

#### Arguments参数

可以直接下拉选择。

**这里的参数,最好用英文格式的双引号""包括起来,否则Failed to load file**

![image-20210811101106765](/images/2021/08/image-20210811101106765.png)

上述内容填写安装之后，点击 OK 按钮。

#### 验证配置

上述操作执行完毕之后，便可在Idea中打开md文件进行一系列操作

> 在需要编辑的md文件上右键,选择External Tools下的Typora工具

![image-20210811101459966](/images/2021/08/image-20210811101459966.png)

###  快捷键设置

通过在需要编辑的md文件上右键,选择External Tools下的Typora工具, 有点麻烦, 我们可以添加个快捷键。

![image-20210811101627137](/images/2021/08/image-20210811101627137.png)

设置快捷键：

![image-20210811101752608](/images/2021/08/image-20210811101752608.png)

如果出现 **Failed to load file** 异常， 则需要配置中，在 Arguments中添加的参数, 用英文格式的双引号""包括起来。

### Mac 配置

配置 External Tools下的Typora工具：

<img src="/images/2021/08/image-20220805213111392.png" alt="image-20220805213111392" style="zoom:50%;" />

为 External Tools 下的 Typora工具增加快捷键。

<img src="/images/2021/08/image-20220805213232770.png" alt="image-20220805213232770" style="zoom:50%;" />