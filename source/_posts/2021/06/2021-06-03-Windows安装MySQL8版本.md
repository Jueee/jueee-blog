---
title: Windows安装MySQL8版本
layout: info
commentable: true
date: 2021-06-03
mathjax: true
mermaid: true
tags: [Database,MySQL]
categories: [Database,MySQL]
description: 
---

之前本地只安装了 MySQL 7 的版本，现在需要再安装一个 MySQL 8 版本。并同时运行两个MySQL 实例。

<!--more-->

### 安装 MySQL 8

#### 下载安装包

首先去官网下载安装包。

下载地址：https://dev.mysql.com/downloads/mysql/

#### 初始化配置文件

在 MySQL 8 安装目录下，新增 my.ini 文件。

```ini
[mysqld]
# 设置3308端口
port=3308
# 设置mysql的安装目录
basedir="C:/Program Files (x86)/MySQL/mysql-8.0.25-winx64/"
# 设置mysql数据库的数据的存放目录
datadir="C:/ProgramData/MySQL/mysql-8.0.25-winx64/data/"
# 允许最大连接数
max_connections=200
# 允许连接失败的次数。这是为了防止有人从该主机试图攻击数据库系统
max_connect_errors=10
# 服务端使用的字符集默认为utf8mb4
character-set-server=utf8mb4
# 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB
[mysql]
# 设置mysql客户端默认字符集
default-character-set=utf8
[client]
# 设置mysql客户端连接服务端时默认使用的端口
port=3308
default-character-set=utf8mb4
```



#### 初始化 MySQL 8

```
$ mysqld.exe --initialize --user=mysql --console
2021-06-03T07:33:21.066330Z 0 [System] [MY-013169] [Server] C:\Program Files (x86)\MySQL\mysql-8.0.25-winx64\bin\mysqld.exe (mysqld 8.0.25) initializing of server in progress as process 24512
2021-06-03T07:33:21.077089Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
2021-06-03T07:33:22.039158Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
2021-06-03T07:33:24.440831Z 6 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: Gy8=d#vCL>uy
```

#### 注册服务

```
$ mysqld --install mysql8 --defaults-file="C:\Program Files (x86)\MySQL\mysql-8.0.25-winx64\my.ini" mysql8
```

#### 修改注册表

注册表位置：计算机\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\mysql8

![image-20210603154340439](/images/2021/06/image-20210603154340439.png)

#### 启动服务

```
$ net start mysql8
mysql8 服务正在启动 .
mysql8 服务已经启动成功。
```

#### 登录 MySQL

这时提示需要密码，然后就是用你上面初始化 MySQL 最后的密码登录

```
$ mysql -u root -p
Enter password: ************
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.25
```

#### 修改密码

```
mysql> ALTER USER root@localhost IDENTIFIED  BY 'password';
Query OK, 0 rows affected (0.01 sec)
```

#### 修改身份验证机制

MySQL 8.0 默认使用 caching_sha2_password 身份验证机制，可能使一些客户端访问异常，建议修改身份验证机制为原先的 mysql_native_password。

```
mysql> alter user 'root'@'localhost' identified by 'password' password expire never;
Query OK, 0 rows affected (0.01 sec)

mysql> alter user 'root'@'localhost' identified with mysql_native_password by 'password';
Query OK, 0 rows affected (0.01 sec)

mysql> flush privileges;
Query OK, 0 rows affected (0.00 sec)
```

#### 访问 MySQL

```
mysql> select version();
+-----------+
| version() |
+-----------+
| 8.0.25    |
+-----------+
1 row in set (0.00 sec)
```

### 遇到的问题

#### 删除 data 文件夹

初始化 MySQL 时出现如下异常：

```
$ mysqld.exe --initialize --user=mysql --console
2021-06-03T07:22:20.315062Z 0 [System] [MY-013169] [Server] C:\Program Files (x86)\MySQL\mysql-8.0.25-winx64\bin\mysqld.exe (mysqld 8.0.25) initializing of server in progress as process 28252
2021-06-03T07:22:20.317336Z 0 [ERROR] [MY-010457] [Server] --initialize specified but the data directory has files in it. Aborting.
2021-06-03T07:22:20.317345Z 0 [ERROR] [MY-013236] [Server] The designated data directory C:\ProgramData\MySQL\mysql-8.0.25-winx64\data\ is unusable. You can remove all files that the server added to it.
2021-06-03T07:22:20.317909Z 0 [ERROR] [MY-010119] [Server] Aborting
2021-06-03T07:22:20.318138Z 0 [System] [MY-010910] [Server] C:\Program Files (x86)\MySQL\mysql-8.0.25-winx64\bin\mysqld.exe: Shutdown complete (mysqld 8.0.25)  MySQL Community Server - GPL.
```

my.ini 配置文件有问题，在查询日志并解决后，删除 data 目录下的所有文件，再次初始化即可。

#### 服务启动异常

使用 net 启动服务时，发现异常：

```
$ net start mysql8
mysql8 服务正在启动 .
mysql8 服务无法启动。

服务没有报告任何错误。

请键入 NET HELPMSG 3534 以获得更多的帮助。
```

很可能是注册表中的 ImagePath 路径有问题，按照安装说明中进行修改即可。

#### 客户端连接异常

客户端连接 MySQL 8 出现异常：

```
Unable to load authentication plugin 'caching_sha2_password'.
```

这是 MySQL 8.0版本才出现的问题，原因是 MySQL 8.0 默认使用 caching_sha2_password 身份验证机制 —— 从原来的 mysql_native_password 更改为 caching_sha2_password。

解决办法：

可以更换版本但是感觉治标不治本，建议修改身份验证机制

1. 登陆 MySQL ，输入：mysql -uroot -p   接着输入密码

2. 登陆mysql成功之后输入：

   ```sql
   alter user 'root'@'localhost' identified by 'password' password expire never;
   alter user 'root'@'localhost' identified with mysql_native_password by 'password'
   flush privileges;
   ```

   其中 password 为 MySQL 的密码。

再次使用客户端连接，即可正常。

