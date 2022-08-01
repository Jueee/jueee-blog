---
title: Mac上快速安装oh-my-zsh
layout: info
commentable: true
date: 2022-08-01
mathjax: true
mermaid: true
tags: [软件,MacOS]
categories: [软件,MacOS]
description:
---

### oh-my-zsh 介绍

- GitHub：[ohmyzsh-github](https://github.com/ohmyzsh/ohmyzsh)

<!--more-->

### zsh安装设置

mac自带了zsh，可以检测一下：

```shell
$ cat /etc/shells
# List of acceptable shells for chpass(1).
# Ftpd will not allow users to connect who are not using
# one of these shells.

/bin/bash
/bin/csh
/bin/dash
/bin/ksh
/bin/sh
/bin/tcsh
/bin/zsh
```

查看 zsh 版本：

```shell
$ zsh --version
zsh 5.8.1 (x86_64-apple-darwin21.0)
```

把zsh设置成默认shell

```bash
# 查看
$ echo $(which zsh)
/bin/zsh

# 设置
$ chsh -s $(which zsh)

# 查检-需要关闭终端重新打开后生效
$ echo $SHELL
/bin/zsh
```

### oh-my-zsh 安装

1. 下载仓库： 

   ```
   git clone https://github.com/ohmyzsh/ohmyzsh.git ~/.oh-my-zsh
   ```

2. 创建一个新的 zsh 配置文件。

   您可以通过复制我们为您包含的模板来创建新的zsh配置文件。

   ```
   cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
   ```

3. 更改默认 shell 的配置：

   ```
   chsh -s $(which zsh)
   ```

   您必须退出用户会话并重新登录才能看到此更改。

### 修改主题

主题列表：https://github.com/ohmyzsh/wiki/blob/main/Themes.md

默认显示：

##### <img src="/images/2022/08/image-20220801211650600.png" alt="image-20220801211650600" style="zoom:50%;" />

打开设置 `vi ~/.zshrc`

![image-20220801211632073](/images/2022/08/image-20220801211632073.png)

修改主题为 `crcandy`，并重启终端生效。

<img src="/images/2022/08/image-20220801213206293.png" alt="image-20220801213206293" style="zoom:50%;" />
