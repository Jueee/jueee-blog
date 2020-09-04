---
title: Arthas之使用profiler做复杂链路分析
layout: info
commentable: true
date: 2020-09-02
mathjax: true
mermaid: true
tags: [Java,Java诊断,Arthas]
categories: [Java,Arthas]
description: 
---

### Arthas 的 profiler 命令

#### 命令说明

`profiler` 命令支持生成应用热点的火焰图。本质上是通过不断的采样，然后把收集到的采样结果生成火焰图。

> 文档：https://arthas.aliyun.com/doc/profiler.html

`profiler` 命令的实现依赖于开源 `async-profiler`：

> GitHub：https://github.com/jvm-profiling-tools/async-profiler

<!--more-->

#### 参数说明

| 参数名称    | 参数说明                                                     |
| ----------- | ------------------------------------------------------------ |
| *action*    | 要执行的操作                                                 |
| *actionArg* | 属性名模式                                                   |
| [i:]        | 采样间隔（单位：ns）（默认值：10'000'000，即10 ms）          |
| [f:]        | 将输出转储到指定路径                                         |
| [d:]        | 运行评测指定秒                                               |
| [e:]        | 要跟踪哪个事件（cpu, alloc, lock, cache-misses等），默认是cpu |

#### 注意事项

`profiler` 命令的使用，有以下注意事项：

1. Windows系统不支持 profiler 命令，只有  Linux/Mac 支持。

   > Current OS do not support AsyncProfiler, Only support Linux/Mac.

2. `$ /lib/x86_64-linux-gnu/libc.so.6 --version` 版本大于 2.14

   > /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.14' not found

### 使用 profiler 命令

#### 启动profiler

```powershell
$ profiler start
Started [cpu] profiling
```

> 默认情况下，生成的是cpu的火焰图，即event为`cpu`。可以用`--event`参数来指定。

#### 获取数量

获取已采集的sample的数量

```powershell
$ profiler getSamples
23
```

#### 查看状态

```powershell
$ profiler status
[cpu] profiling is running for 4 seconds
```

可以查看当前profiler在采样哪种`event`和采样时间。

#### 停止profiler

默认生成svg格式结果

```powershell
$ profiler stop
profiler output file: /tmp/demo/arthas-output/20191125-135546.svg
OK
```

默认情况下，生成的结果保存到应用的`工作目录`下的`arthas-output`目录。可以通过 `--file`参数来指定输出结果路径。比如：

```powershell
$ profiler stop --file /tmp/output.svg
profiler output file: /tmp/output.svg
OK
```

#### 生成html格式

默认情况下，结果文件是`svg`格式，如果想生成`html`格式，可以用`--format`参数指定：

```powershell
$ profiler stop --format html
profiler output file: /tmp/test/arthas-output/20191125-143329.html
OK
```

或者在`--file`参数里用文件名指名格式。比如`--file /tmp/result.html` 。

### 做复杂链路分析

#### 采样生成jfr文件

启动arthas之后，执行以下采样命令：

```
profiler start -f /home/admin/yourAppName/target/arthas-output/%t.jfr -d 180
```

%t 表示当前时间，-d 后面是采样秒数。