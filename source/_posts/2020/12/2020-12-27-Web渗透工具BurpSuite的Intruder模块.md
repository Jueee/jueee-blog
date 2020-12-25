---
title: Web渗透工具BurpSuite的Intruder模块
layout: info
commentable: true
date: 2020-12-27
mathjax: true
mermaid: true
tags: [Blog]
categories: Blog
description: 
---

### Burp Intruder 介绍

Burp Intruder是一个强大的工具，用于自动对Web应用程序自定义的攻击，Burp Intruder 是高度可配置的，并被用来在广范围内进行自动化攻击。

可以使用 Burp Intruder 方便地执行许多任务，包括枚举标识符，获取有用数据，漏洞模糊测试。

合适的攻击类型取决于应用程序的情况，可能包括：缺陷测试：SQL 注入，跨站点脚本，缓冲区溢出，路径遍历；暴力攻击认证系统；枚举；操纵参数；拖出隐藏的内容和功能；会话令牌测序和会话劫持；数据挖掘；并发攻击；应用层的拒绝服务式攻击。

<!--more-->

### 模块说明

Burp Intruder主要有四个模块组成:

1. Target 用于配置目标服务器进行攻击的详细信息。
2. Positions  设置Payloads的插入点以及攻击类型（攻击模式）。
3. Payloads  设置payload，配置字典
4. Opetions  此选项卡包含了request headers，request engine，attack results ，grep match，grep_extrack，grep payloads和redirections。

可以发动攻击之前，在主要Intruder的UI上编辑这些选项，大部分设置也可以在攻击时对已在运行的窗口进行修改。

#### Target：目标选项

这个选项是用来配置目标服务器的细节，配置目标的host，port及协议（http/https）：

![image-20201225101813001](/images/2020/12/image-20201225101813001.png)

#### Positions：位置选项

这个选项是用来配置在攻击里产生的所有 HTTP 请求的模板。

![image-20201225102225581](/images/2020/12/image-20201225102225581.png)

Attack type 有四个攻击方式，下面说下每个的作用：

- sniper – 对变量依次进行暴力破解。
- battering ram – 对变量同时进行破解。
- pitchfork – 每一个变量标记对应一个字典，一一对应进行破解。
- cluster bomb – 每个变量对应一个字典，并且进行交叉式破解，尝试各种组合。适用于用户名+密码的破解。

可以使用选项上的按钮来控制位置上的标记：

- add § — 在当前光标位置插入一个位置标记。
- clear § — 删除整个模板或选中的部分模板里的位置标记。
- auto § — 这会对放置标记的位置做一个猜测，放哪里会有用，然后就把标记放到相应位置。这是一个为攻击常规漏洞(SQL 注入)快速标记出合适位置的有用的功能，然后人工标记是为自定义攻击的。
- refresh — 如果需要，可以刷新编辑器里有颜色的代码。
- clear — 删除整个编辑器内容。

#### Payloads：有效负荷选项

这个选项是用来配置一个或多个有效负荷的集合。如果定义了”cluster bomb”和”pitchfork”攻击类型，然后必须为每定义的有效负荷位置(最多8个)配置一个单独的有效负荷。使用”payload set”下拉菜单选择要配置的有效负荷。

##### Payload Sets

Payload数量类型设置

![image-20201225102526892](/images/2020/12/image-20201225102526892.png)

##### Payload Opetions

该选项会根据选项1中Payload type的设置而改变

![image-20201225102556360](/images/2020/12/image-20201225102556360.png)

##### Payload Processing 

对生成的Payload进行编码、加密、截取等操作

![image-20201225102628858](/images/2020/12/image-20201225102628858.png)

##### Payload Encoding 

可以配置哪些有效载荷中的字符应该是URL编码的HTTP请求中的安全传输。任何已配置的URL编码最后应用，任何有效载荷处理规则执行之后。 这是推荐使用此设置进行最终URL编码，而不是一个有效载荷处理规则，因为可以用来有效载荷的grep选项来检查响应为呼应有效载荷的最终URL编码应用之前。

![image-20201225102658729](/images/2020/12/image-20201225102658729.png)

#### Opetions 选项卡

此选项卡包含了request headers，request engine，attack results ，grep match，grep_extrack，grep payloads和redirections。

可以发动攻击之前，在主要Intruder的UI上编辑这些选项，大部分设置也可以在攻击时对已在运行的窗口进行修改。

##### Request Headers

这些设置控制在Intruder是否更新配置请求头。

![image-20201225103005795](/images/2020/12/image-20201225103005795.png)

- 如果选中‘update Content-Length header’框，Burp Intruder 会使用每个请求的 HTTP 主体长度的正确值，添加或更新这个请求里 HTTP 消息头的内容长度。这个功能对一些需要把可变长度的有效载荷插入到 HTTP 请求模板主体的攻击是很有必要的。这个 HTTP 规范和大多数 web 服务器一样，需要使用消息头内容长度来指定 HTTP 主体长度的正确值。如果没有指定正确值，目标服务器会返回一个错误，也可能返回一个未完成的请求，也可能无限期地等待接收请求里的进一步数据。
- 如果选中‘set Connection: close’框，则 Burp Intruder 会添加或更新 HTTP 消息头的连接来请求在每个请求后已关闭的连接。在多数情况下，这个选项会让攻击执行得更快。

##### Request Engine

设置发送请求的线程、超时重试等。

![image-20201225103151064](/images/2020/12/image-20201225103151064.png)

- Number of threads：线程，该选项控制攻击请求的并发数。
- Number of retries on network failure：网络故障的重试次数 – 如果出现连接错误或其他网络问题，Burp会放弃和移动之前重试的请求指定的次数。
- Pause before retry：重试前等待时间，当重试失败的请求，Burp会等待指定的时间（以毫秒为单位），然后重试。
- Throttle between requests：请求之间的等待时间，Burp可以在每次请求之前等待一个指定的延迟（以毫秒为单位） 。此选项很有用，以避免超载应用程序，或者是更隐蔽。
- Start time:开始时间，此选项允许您配置攻击立即启动，或在指定的延迟后，或开始处于暂停状态。

##### Attack Results

设置攻击结果的显示。

![image-20201225103310245](/images/2020/12/image-20201225103310245.png)

- Store requests/responses：存储请求/响应，这个选项确定攻击是否会保存单个请求和响应的内容
- Make unmodified baseline request：未修改的基本请求，如果选择此选项，那么除了配置的攻击请求，Burp会发出模板请求设置为基值，所有有效载荷的位置。此请求将在结果表显示为项目＃ 0 。使用此选项很有用，提供一个用来比较的攻击响应基地的响应。
- Use denial-of-service mode：使用拒绝服务的模式，如果选择此选项，那么攻击会发出请求，如正常，但不会等待处理从服务器收到任何答复。只要发出的每个请求， TCP连接将被关闭。这个功能可以被用来执行拒绝服务的应用层对脆弱的应用程序的攻击，通过重复发送该启动高负荷任务的服务器上，同时避免通过举办开放套接字等待服务器响应锁定了本地资源的请求。
- Store full payloads：保存完整的有效载荷。如果选择此选项，Burp将存储全部有效载荷值的结果。

##### Grep – Match

在响应中找出存在指定的内容的一项。

![image-20201225103454175](/images/2020/12/image-20201225103454175.png)

- Match：匹配类型，指定的表达式是否是简单的字符串或regular expressions(正则表达式)。
- Case sensitive match：区分大小写的匹配，指定检查表达式是否应区分大小写。
- Exclude HTTP headers：排除HTTP头，指定的HTTP响应头是否应被排除在检查。

##### Grep – Extract

通过正则提取返回信息中的内容。

点击ADD就弹出正则编辑窗口，如图我们选中我们需要获取的部分就可以自动生成正则表达式。点击OK就可以在列表中添加这条正则表达式。

![image-20201225103815261](/images/2020/12/image-20201225103815261.png)

##### Grep – Payloads

这些设置可以用于包含已提交的有效负载的反射的标志结果项目。如果启用了此选项，BurpSuite会添加包含一个复选框指示当前负载的值在每个响应发现新的结果列。

![image-20201225103910105](/images/2020/12/image-20201225103910105.png)

- Search responses for payload strings：在响应中搜索Payload。
- Case sensitive match：区分大小写，此指定是否对有效负载的检查区分大小写。
- Exclude HTTP headers：排除HTTP标头，不对HTTP响应头进行检查。
- Match against pre-URL-encoded payloads：对预URL编码的有效载荷匹配。

##### Redirections

重定向响应，控制Burp在进行攻击时如何处理重定向。 

![image-20201225104000361](/images/2020/12/image-20201225104000361.png)

- Follow redirections：跟随重定向
  Never：不跟随重定向（关闭跟随重定向）。
- On-site only：只会跟随重定向到同一个网页“网站” ，即使用相同的主机，端口和协议的是在原始请求使用的URL 。
- In-scope only：只跟随范围内，Intruder只会跟随重定向到目标范围之内的URL 。
- Always：总是跟随重定向，将遵循重定向到任何任何URL。（此选项可能会引导burp到其他网站）

#### 发起攻击

配置好相关的内容后就可以点击任意模块右上角的start attack或者菜单栏中的Intruder->start attack发起攻击请求。



