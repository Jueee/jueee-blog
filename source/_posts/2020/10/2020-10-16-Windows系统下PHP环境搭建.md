---
title: Windows系统下PHP环境搭建
layout: info
commentable: true
date: 2020-10-16
mathjax: true
mermaid: true
tags: [PHP,软件]
categories: 
- [软件,Windows]
- [PHP]
description: 
---

### 下载 PHP

下载地址：http://php.net/downloads.php

Windows下载：https://windows.php.net/download/

版本选择：

- 如果是与 Apache 搭配，建议选择 Thread Safe 版本（有 php7apache2_4.dll）。
- 如果是与 CGI 或者 FAST-CGI 搭配，建议选择 Non Thread Safe 版本。

<!--more-->

### 安装Apache 服务器

PHP环境搭建的前提是 Apache HTTP Server （Apache 服务器）已经安装部署成功，并可以正常访问到服务器的主页面。

Apache HTTP Server 的安装部署可以点击“ [Windows系统下安装Apache服务器](https://jueee.github.io/2020/10/2020-10-15-Windows系统下安装Apache服务器)” 查看具体操作。

### 配置 PHP

将 PHP 的根目录下的 php.ini-development 或者 php.ini-production复制一份并改名为 php.ini，作为PHP的配置文件。

#### 修改扩展文件的路径

```ini
; extension_dir = "ext" 
```

取消注释，或者改为： 

```ini
extension_dir = "${phphome}\ext"
```

注意：如果是与 Apache 搭配，建议将扩展文件路径改为绝对路径，因为有可能加载不了。

#### 设置默认的时区

```ini
[Date]
; https://www.php.net/manual/zh/timezones.php 选择时区列表网址
date.timezone = Asia/Shanghai
```

#### 设置 ssl

```ini
[openssl]
openssl.cafile= cacert.pem
```

### 修改 Apache服务器

修改 Apache24\conf\ 目录下的 httpd.conf 配置 Apache ，让 Apache 和 PHP 协同工作。

#### DocumentRoot 设置

修改前：默认的是 Apache24 下的 htdocs 目录：

![1602831496444](/images/2020/10/1602831496444.png)

修改后：指定到自定义的路径，但是要记住这个路径。

```
DocumentRoot "E:/software/php/php-page"
<Directory "E:/software/php/php-page">
```

#### 默认索引

修改默认的索引，以支持 PHP 。

修改前：

```conf
<IfModule dir_module>
    DirectoryIndex index.html
</IfModule>
```

修改后：

```conf
<IfModule dir_module>
    DirectoryIndex index.html  index.php index.htm
</IfModule>
```

#### 开启 rewrite 功能

将下面这行代码前面的 # 去掉：

```conf
LoadModule rewrite_module modules/mod_rewrite.so
```

#### 加载 PHP 模块

如果是 PHP 7，则相应的更改，示例如下（**注意绝对路径**）：

```
#php7
LoadModule php7_module E:/software/php/php-7.4.11/php7apache2_4.dll
<IfModule php7_module> 
    PHPIniDir "D:/soft/php-7.x.x/" 
    AddType application/x-httpd-php .php
    AddType application/x-httpd-php-source .phps
</IfModule>
```

#### dll 复制

如果安装的PHP x64位版本，Apache也需要是x64位版本的。

然后还要将php目录下的libeay32.dll、ssleay32.dll、libssh2.dll以及ext目录下的php_curl.dll等四个文件，都复制放到System32目录下。否则curl扩展无法使用。

参考链接：http://my.oschina.net/lsfop/blog/496181 。

### 启动运行测试

在 `E:\software\php\php-page` 目录下，创建 index.php 文件，文本内容如下：

```php
<?php
echo phpinfo();
?>
```

打开浏览地址栏输入： localhost:80/index.php 或者 127.0.0.1:80/index.php ,就可以打开 PHP 页面。

![1602831917955](/images/2020/10/1602831917955.png)