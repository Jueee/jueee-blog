---
title: Windows系统下安装Apache服务器
layout: info
commentable: true
date: 2020-10-15
mathjax: true
mermaid: true
tags: [软件,Apache]
categories: 
- [软件,Windows]
- [Apache]
description: 
---

### Apache & Tomcat

Apache与Tomcat都是Apache开源组织开发的用于处理HTTP服务的项目，两者都是免费的，都可以做为独立的Web服务器运行。

Apache是Web服务器而Tomcat是Java应用服务器。

<!--more-->

#### Apache

Apache：是C语言实现的，专门用来提供HTTP服务。

特性：简单、速度快、性能稳定、可配置（代理）

1. 主要用于解析静态文本，并发性能高，侧重于HTTP服务；
2. 支持静态页（HTML），不支持动态请求如：CGI、Servlet/JSP、PHP、ASP等；
3. 具有很强的可扩展性，可以通过插件支持PHP，还可以单向Apache连接Tomcat实现连通；
4. Apache是世界使用排名第一的Web服务器。

#### Tomcat

Tomcat：是Java开发的一个符合JavaEE的Servlet规范的JSP服务器（Servlet容器），是 Apache 的扩展。

特性：免费的Java应用服务器。

1. 主要用于解析JSP/Servlet，侧重于Servlet引擎；
2. 支持静态页，但效率没有Apache高；支持Servlet、JSP请求；
3. Tomcat本身也内置了一个HTTP服务器用于支持静态内容，可以通过Tomcat的配置管理工具实现与Apache整合。

#### Apache + Tomcat

Apache + Tomcat 两者整合后优点：
如果请求是静态网页则由Apache处理，并将结果返回；如果是动态请求，Apache会将解析工作转发给Tomcat处理，Tomcat处理后将结果通过Apache返回。这样可以达到分工合作，实现负载远衡，提高系统的性能。

### 下载Apache服务器

Apache HTTP Servcer下载地址：https://httpd.apache.org/

Windows 版本下载：https://httpd.apache.org/docs/current/platform/windows.html#down

### 配置Apache服务器

打开 Apache24\conf 目录下的 httpd.conf，修改配置信息。

#### 修改 ServerRoot 路径

```conf
Define SRVROOT "E:\software\php\Apache24"
ServerRoot "${SRVROOT}"
```

如果不修改会出现如下错误：

> httpd.exe: Syntax error on line 39 of E:/software/php/Apache24/conf/httpd.conf: ServerRoot must be a valid directory

#### 修改端口号

默认的是80端口，但是多数情况下，80端口被占用，所以需要修改80端口。如果确定80端口未被占用则可以不修改。

```conf
Listen 80
ServerName localhost:80
```

如果不修改可能会提示错误：

> (OS 10048)通常每个套接字地址(协议/网络地址/端口)只允许使用一次。: AH00072: make_sock: could not bind to address [::]:8081
>
> (OS 10048)通常每个套接字地址(协议/网络地址/端口)只允许使用一次。 : AH00072: make_sock: could not bind to address 0.0.0.0:8081
> AH00451: no listening sockets available, shutting down
>AH00015: Unable to open logs

#### 443 端口被占用

如果 443 端口被占用，会有如下报错信息：

> (OS 10048)通常每个套接字地址(协议/网络地址/端口)只允许使用一次。  : AH00072: make_sock: could not bind to address [::]:443
>
> (OS 10048)通常每个套接字地址(协议/网络地址/端口)只允许使用一次。  : AH00072: make_sock: could not bind to address 0.0.0.0:443 AH00451: no listening sockets available, shutting down

解决 443 端口被占用的问题：

在httpd.conf中, 找到加载ssl_module的那一行, 加#号注释掉就好了：

```conf
# LoadModule ssl_module modules/mod_ssl.so
```

### 安装Apache服务器

#### 常见的dos操作命令

1. 把apache24安装成系统服务：httpd -k install
2. 启动服务apcache24服务 ：httpd -k star
3. 停止服务apcache24服务 ：httpd -k stop
4. 重启服务apcache24服务 ：httpd -k restart
5. 卸载apcache24服务 ：httpd -k uninstall
6. 测试apache24配置语法 ：httpd -t
7. 版本信息 ：httpd -V
8. 查看cmd命令：httpd -h

#### 安装成系统服务

以管理员身份运行：`.\httpd.exe  -k install`

![1602828782266](/images/2020/10/1602828782266.png)

### 启动Apache服务器

#### 方法一

双击 `Apache24\bin\httpd.exe` 即可启动Apache服务器。

#### 方法二

打开系统服务窗口，找到Apache2.4，选择启动或停止。

![1602828954797](/images/2020/10/1602828954797.png)

#### 方法三

打开 Apache24\bin 找到 ApacheMonitor.exe 双击打开 Apache24 启停管理器。

![1602829021497](/images/2020/10/1602829021497.png)

#### 访问页面

然后打开浏览器在地址栏输入 http://localhost:80/ 就可以访问页面，页面如下：

![1602828320892](/images/2020/10/1602828320892.png)