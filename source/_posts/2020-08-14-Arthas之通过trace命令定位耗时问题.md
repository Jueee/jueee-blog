---
title: Arthas之通过trace命令定位耗时问题
layout: info
commentable: true
date: 2020-08-14
mathjax: true
mermaid: true
tags: [Java,Java诊断,Arthas]
categories: [Java,Arthas]
description: 通过Arthas中的trace命令，可以查看方法内部调用路径，并输出方法路径上的每个节点上耗时。
---

### trace（内部调用路径）

#### 方法介绍

通过Arthas中的trace命令，可以查看方法内部调用路径，并输出方法路径上的每个节点上耗时。

官方文档：

> [https://alibaba.github.io/arthas/trace.html](https://alibaba.github.io/arthas/trace.html)

#### 参数说明

使用 `thread --help` 获取 thread 命令的帮助信息：

![1597393992311](/images/2020/08/1597393992311.png)

主要参数说明如下：

| 参数名称            | 参数说明                             |
| ------------------- | ------------------------------------ |
| *class-pattern*     | 类名表达式匹配                       |
| *method-pattern*    | 方法名表达式匹配                     |
| *condition-express* | 条件表达式                           |
| [E]                 | 开启正则表达式匹配，默认为通配符匹配 |
| `[n:]`              | 命令执行次数                         |
| `#cost`             | 方法执行耗时                         |

#### 定位耗时问题

使用 **trace ** 命令开始检测耗时情况。

```
trace sample.demo.controller.UserController getUser
```

结果如下：

![1597402146114](/images/2020/08/1597402146114.png)

继续跟踪耗时高的方法，然后再次访问。

```
trace sample.demo.TraceService get
```

结果如下：

![1597402247630](/images/2020/08/1597402247630.png)

很清楚的看到是 `TraceService`的 `mysql`方法耗时是最高的。

### monitor（方法调用监控）

#### 方法介绍

monitor 命令可以对匹配 `class-pattern`／`method-pattern`的类、方法的调用进行监控。

官方文档：

> [https://alibaba.github.io/arthas/monitor.html](https://alibaba.github.io/arthas/monitor.html)

#### 参数说明

使用 `monitor --help` 获取 monitor 命令的帮助信息：

![1597402367532](/images/2020/08/1597402367532.png)

方法拥有一个命名参数 `[c:]`，意思是统计周期（cycle of output），拥有一个整型的参数值

| 参数名称         | 参数说明                             |
| ---------------- | ------------------------------------ |
| *class-pattern*  | 类名表达式匹配                       |
| *method-pattern* | 方法名表达式匹配                     |
| [E]              | 开启正则表达式匹配，默认为通配符匹配 |
| `[c:]`           | 统计周期，默认值为120秒              |

#### 监控的维度说明

| 监控项    | 说明                       |
| --------- | -------------------------- |
| timestamp | 时间戳                     |
| class     | Java类                     |
| method    | 方法（构造方法、普通方法） |
| total     | 调用次数                   |
| success   | 成功次数                   |
| fail      | 失败次数                   |
| rt        | 平均RT                     |
| fail-rate | 失败率                     |

#### 统计方法耗时

使用 **monitor** 命令监控统计方法的执行情况。

每10秒统计一次 `com.UserServiceImpl` 类的 `get` 方法执行情况。

```
monitor -c 10 sample.demo.controller.UserController getUser
```

![1597402331522](/images/2020/08/1597402331522.png)

### watch（观察方法信息）

#### 方法介绍

watch 让你能方便的观察到指定方法的调用情况。能观察到的范围为：`返回值`、`抛出异常`、`入参`，通过编写 `OGNL` 表达式进行对应变量的查看。

官方文档：

> [https://alibaba.github.io/arthas/watch.html](https://alibaba.github.io/arthas/watch.html)

#### 参数说明

使用 `watch --help` 获取 watch 命令的帮助信息：

![1597402622041](/images/2020/08/1597402622041.png)

watch 的参数比较多，主要是因为它能在 4 个不同的场景观察对象：

| 参数名称            | 参数说明                                           |
| ------------------- | -------------------------------------------------- |
| *class-pattern*     | 类名表达式匹配                                     |
| *method-pattern*    | 方法名表达式匹配                                   |
| *express*           | 观察表达式                                         |
| *condition-express* | 条件表达式                                         |
| [b]                 | 在**方法调用之前**观察                             |
| [e]                 | 在**方法异常之后**观察                             |
| [s]                 | 在**方法返回之后**观察                             |
| [f]                 | 在**方法结束之后**(正常返回和异常返回)观察【默认】 |
| [E]                 | 开启正则表达式匹配，默认为通配符匹配               |
| [x:]                | 指定输出结果的属性遍历深度，默认为 1               |

#### **特别说明**

- watch 命令定义了4个观察事件点，即 `-b` 方法调用前，`-e` 方法异常后，`-s` 方法返回后，`-f` 方法结束后
- 4个观察事件点 `-b`、`-e`、`-s` 默认关闭，`-f` 默认打开，当指定观察点被打开后，在相应事件点会对观察表达式进行求值并输出
- 这里要注意`方法入参`和`方法出参`的区别，有可能在中间被修改导致前后不一致，除了 `-b` 事件点 `params` 代表方法入参外，其余事件都代表方法出参
- 当使用 `-b` 时，由于观察事件点是在方法调用前，此时返回值或异常均不存在

#### 观察方法信息

##### 查看入参和出参
```
$ watch sample.demo.controller.UserController getUser '{params[0],returnObj}'
```

![1597402871452](/images/2020/08/1597402871452.png)

##### 查看入参和出参大小
```
$ watch sample.demo.controller.UserController getUser '{params[0],returnObj.size}'
```

![1597402936287](/images/2020/08/1597402936287.png)

##### 查看入参和出参String
```
$ watch sample.demo.controller.UserController getUser '{params[0],returnObj.toString()}'
```

![1597402988837](/images/2020/08/1597402988837.png)

##### 查看方法异常之后

```
$ watch sample.demo.controller.UserController getUser '{params[0],returnObj}' -e
```

![1597403442198](/images/2020/08/1597403442198.png)

### stack（方法调用路径）

#### 方法介绍

stack 输出当前方法被调用的调用路径。

官方文档：[https://alibaba.github.io/arthas/stack.html](https://alibaba.github.io/arthas/stack.html)

#### 参数说明

使用 `stack --help` 获取 stack 命令的帮助信息：

![1597403694320](/images/2020/08/1597403694320.png)

主要参数如下：

| 参数名称            | 参数说明                             |
| ------------------- | ------------------------------------ |
| *class-pattern*     | 类名表达式匹配                       |
| *method-pattern*    | 方法名表达式匹配                     |
| *condition-express* | 条件表达式                           |
| [E]                 | 开启正则表达式匹配，默认为通配符匹配 |
| `[n:]`              | 执行次数限制                         |

#### 方法调用路径

```
$ stack sample.demo.controller.UserController getUser
```

![1597403757289](/images/2020/08/1597403757289.png)

### tt（方法调用时空隧道）

#### 方法介绍

tt 方法执行数据的时空隧道，记录下指定方法每次调用的入参和返回信息，并能对这些不同的时间下调用进行观测。

官方文档：[https://alibaba.github.io/arthas/tt.html](https://alibaba.github.io/arthas/tt.html)

#### 参数说明

- `-t`

  tt 命令有很多个主参数，`-t` 就是其中之一。这个参数的表明希望记录下类 `*Test` 的 `print` 方法的每次执行情况。

- `-n 3`

  当你执行一个调用量不高的方法时可能你还能有足够的时间用 `CTRL+C` 中断 tt 命令记录的过程，但如果遇到调用量非常大的方法，瞬间就能将你的 JVM 内存撑爆。

  此时你可以通过 `-n` 参数指定你需要记录的次数，当达到记录次数时 Arthas 会主动中断tt命令的记录过程，避免人工操作无法停止的情况。

#### 返回结果说明

| 表格字段  | 字段解释                                                     |
| --------- | ------------------------------------------------------------ |
| INDEX     | 时间片段记录编号，每一个编号代表着一次调用，后续tt还有很多命令都是基于此编号指定记录操作，非常重要。 |
| TIMESTAMP | 方法执行的本机时间，记录了这个时间片段所发生的本机时间       |
| COST(ms)  | 方法执行的耗时                                               |
| IS-RET    | 方法是否以正常返回的形式结束                                 |
| IS-EXP    | 方法是否以抛异常的形式结束                                   |
| OBJECT    | 执行对象的`hashCode()`，注意，曾经有人误认为是对象在JVM中的内存地址，但很遗憾他不是。但他能帮助你简单的标记当前执行方法的类实体 |
| CLASS     | 执行的类名                                                   |
| METHOD    | 执行的方法名                                                 |

#### 方法调用时空隧道

##### 开始记录方法调用信息

```
$ tt -t sample.demo.controller.UserController getUser
```

![1597403958714](/images/2020/08/1597403958714.png)

##### 查看记录的方法调用信息

```
tt -l
```

![1597404208135](/images/2020/08/1597404208135.png)

##### 查看调用记录的详细信息

```
tt -i 1001
```

![1597404218381](/images/2020/08/1597404218381.png)

##### 重新发起调用

```
tt -i 1001 -p
```

![1597404320236](/images/2020/08/1597404320236.png)

