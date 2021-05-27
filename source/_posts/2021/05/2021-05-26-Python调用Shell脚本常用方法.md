---
title: Python调用Shell脚本常用方法
layout: info
commentable: true
date: 2021-05-26
mathjax: true
mermaid: true
tags: [Python,Shell]
categories: 
- [Python]
- [Shell]
description: 
---

### 使用 os.system()

Python 示例：

```python
import os
val = os.system('ls -al')
print val
```

#### 返回的状态码

正常输出的情况下，sh 返回的状态码是 0

```powershell
$ python test1.py
total 12
drwxr-xr-x 2 jue root 4096 May 25 11:18 .
drwx------ 4 jue root 4096 May 25 11:18 ..
-rw-r--r-- 1 jue root   46 May 25 11:18 test1.py
0
```

没有找到时，sh 返回的状态码是1，而适用 Python 调用，返回的是：256

```python
import os
val = os.system('ls -al|grep jue')
print val
```

调用 Python

```bash
$ python test1.py
256
```

### 使用 os.popen()

### 使用 commands 模块

有三个方法可以使用：

1. commands.getstatusoutput(cmd)，其以字符串的形式返回的是输出结果和状态码，即（status,output）。
2. commands.getoutput(cmd)，返回cmd的输出结果。
3. commands.getstatus(file)，返回ls -l file的执行结果字符串，调用了getoutput，不建议使用此方法

### 使用 subprocess 模块

subprocess 模块允许创建很多子进程，创建的时候能指定子进程和子进程的输入、输出、错误输出管道，执行后能获取输出结果和执行状态。

1. subprocess.run()：python3.5中新增的函数， 执行指定的命令， 等待命令执行完成后返回一个包含执行结果的CompletedProcess类的实例。
2. subprocess.call()：执行指定的命令， 返回命令执行状态， 功能类似 os.system（cmd）。
3. subprocess.check_call()：python2.5中新增的函数, 执行指定的命令, 如果执行成功则返回状态码， 否则抛出异常。