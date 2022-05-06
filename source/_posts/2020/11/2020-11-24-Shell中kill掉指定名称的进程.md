---
title: Shell中kill掉指定名称的进程
layout: info
commentable: true
date: 2020-11-24
mathjax: true
mermaid: true
tags: [Linux,Shell]
categories: [OS,Shell]
description: 
---

在 Linux 开发中我们时常会遇到对于之前进程kill掉，然后再运行当前进程或程序的情况，此时我们是不知道需要kill的进程号的，那么就需要通过一个shell命令组合来实现这个需求。

<!--more-->

### 实现方法

如下命令可以实现：

```shell
ps a | grep -w nameprocess | grep -v grep| cut -c 1-6 | xargs kill -9
```

说明：

- 管道符“|”用来隔开两个命令，管道符左边命令的输出会作为管道符右边命令的输入。 
- “ps a”是查看所有进程的命令。这时检索出的进程将作为下一条命令“grep“的输入，注意要结束其它程序时，请将上面命令中的 nameprocess 替换成其它程序名，-w 'nameprocess' 强制 PATTERN 仅完全匹配字词。
- “grep -v grep”是在列出的进程中去除含有关键字“grep”的进程。
- “cut -c 1-6”是截取输入行的第1个字符到第6个字符，而这正好是进程号PID，或者根据自己实际的情况可以调整字符的截取位置。
- “xargs kill -9”中的xargs命令是用来把前面命令的输出结果（PID）作为“kill -9”命令的参数，并执行该命令。
- “kill -9”会强行杀掉指定进程，这样就成功清除了同名进程。

### 其他方法

```shell
ps axu|grep nameprocess | awk '{print "kill -9 "}'
```

