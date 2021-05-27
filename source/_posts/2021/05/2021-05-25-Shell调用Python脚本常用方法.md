---
title: Shell调用Python脚本常用方法
layout: info
commentable: true
date: 2021-05-25
mathjax: true
mermaid: true
tags: [Python,Shell]
categories: 
- [Python]
- [Shell]
description: 
---

### 普通调用

#### Python脚本示例

```python
# -*- coding: utf-8 -*-
import datetime

if __name__=='__main__':
    today = datetime.datetime.today()
    yesterday = today - datetime.timedelta(days=1)
    keyWord = yesterday.strftime( '%Y-%m-%d' )
    print(keyWord +" 测试！")
```

#### Shell 脚本示例

```bash
#! /bin/bash


thispath=$(cd "$(dirname "$0")"; pwd)

pyfile="$thispath/test.py"
result=`python $pyfile`
echo $result >> $thispath/out.log
```

#### 调用结果

```bash
$ ./runAlarm.sh
2021-05-24 测试！
```

### 带参数调用

#### Python 脚本示例

```python
# -*- coding: utf-8 -*-
import sys

if __name__=='__main__':
    print("param one:"+sys.argv[1])
    print("param two:"+sys.argv[2])
```

运行脚本：

```bash
$ python test0.py  a b
param one:a
param two:b
```

#### Shell 脚本示例

```shell
#! /bin/bash

thispath=$(cd "$(dirname "$0")"; pwd)

pyfile="$thispath/test0.py"
result=`python $pyfile ttt ccc`
echo $result
```

运行结果：

```
param one:ttt param two:ccc
```

向 Shell 脚本传递参数：

```shell
#! /bin/bash

thispath=$(cd "$(dirname "$0")"; pwd)

pyfile="$thispath/test0.py"
result=`python $pyfile $1 $2`
echo $result
```

运行结果：

```
$ bash test0.sh aaa bbb
param one:aaa param two:bbb
```

