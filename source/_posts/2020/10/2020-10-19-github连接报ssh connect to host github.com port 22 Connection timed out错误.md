---
title: github连接报“ssh connect to host github.com port 22 Connection timed out”错误
layout: info
commentable: true
date: 2020-10-19
mathjax: true
mermaid: true
tags: [Git,GitHub]
categories: Git
description: 
---



Git 在提交 代码时，报错：

```
ssh: connect to host github.com port 22: Connection timed out
fatal: Could not read from remote repository.
```

<!--more-->

在连接 github 时，执行”ssh -T git@github.com” 命令时，出现：

```
$ ssh -T git@github.com
ssh: connect to host github.com port 22: Connection timed out
```

在存放公钥私钥(id_rsa和id_rsa.pub)的同级文件夹中，新建config文本，内容如下：

```
Host github.com
User hellojue@foxmail.com
Hostname ssh.github.com
PreferredAuthentications publickey
IdentityFile ~/.ssh/id_rsa
Port 443
```

其中User为登录github的账号名称。

再次执行”ssh -T git@github.com”时，这时验证就可以通过。

```
$ ssh -T git@github.com
Hi Jueee! You've successfully authenticated, but GitHub does not provide shell access.
```

