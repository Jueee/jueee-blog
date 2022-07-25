---
title: Windows解决Typora提示过期的方案
layout: info
commentable: true
date: 2022-07-15
mathjax: true
mermaid: true
tags: [软件,Windows]
categories: [软件,Windows]
description: 
---

打开一直在用的 Markdown 编辑器 Typora，可是过期提示又来了。该怎么办呢？

![img](/images/2022/07/5e631a95a7a76b8085251b945bd35592.png)

<!--more-->

### 解决方案

根据大神的方案，结合我自己的实践，我把详细步骤一步步地贴出来，希望能够帮助一部分有这方面困惑的朋友，详细操作见下文。

其实操作起来很简单，主要是利用 Windows下的软件的 注册表权限，操作步骤如下：

1）Windows键+R，弹出命令行输入框，输入 regedit

![img](/images/2022/07/45e420f7164690470f4d5c94b132f095.png)

当提示 你要允许此应用对你的设备进行修改吗？ 时，选 是。

2）在注册表的输入框输入：计算机\HKEY_CURRENT_USER\SOFTWARE\Typora ，然后按回车；

![img](/images/2022/07/30185be8b5d3c04cf7f9483822971f73.png)

3）找到 typora 这一项，然后点击 右键，选择 权限；

![img](/images/2022/07/b1d4ccb0189d8ff2a150a61414588921.png)

4）在 权限 里面把各个用户的权限，全部选择 拒绝；有人说，仅关闭当前使用的用户即可，但我觉得保险起见，还是把所有用户都拒绝掉吧。【最后别忘了 应用 + 确认】

![image-20220725113941242](/images/2022/07/image-20220725113941242.png)

随后，可能会收到一个提示框，直接选 是 即可。

![img](/images/2022/07/f0be3404ec1ad205e2b92a50bbdb2538.png)

5）测试下能不能打开 typora：

<img src="/images/2022/07/b8d0fd0878a84fbeb78be028773d524c.png" alt="img" style="zoom:50%;" />
