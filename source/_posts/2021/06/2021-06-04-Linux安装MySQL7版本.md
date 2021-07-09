---
title: Linux安装MySQL7版本
layout: info
commentable: true
date: 2021-06-04
mathjax: true
mermaid: true
tags: [Database,MySQL]
categories: [Database,MySQL]
description: 
---

### 安装步骤

#### 查看服务器版本

系统版本：

```
$ lsb_release -cr
Release:        9.12
Codename:       stretch
```

内核版本：

```
$ uname -r
4.9.0-12-amd64
```

#### 下载 MySQL

根据服务器版本，下载 MySQL 安装包。

下载地址：https://downloads.mysql.com/archives/community/

#### 安装 MySQL

以下载的 `mysql-server_5.7.18-1debian9_amd64.deb-bundle.tar` 为例进行说明。

解压 tar：

```bash
$ gzip mysql-server_5.7.18-1debian9_amd64.deb-bundle.tar
```

解压 tar.gz：

```bash
$ tar -zxvf mysql-server_5.7.18-1debian9_amd64.deb-bundle.tar.gz
```

安装 deb 包：

```bash
$ dpkg -i *.deb
```

#### 初始化 MySQL

```bash
$ /usr/sbin/mysqld --defaults-file=/home/ddb/mysql/my3306.cnf --user=ddb --initialize
```

#### 启动 MySQL

```bash
$ mysqld_safe --defaults-file=/home/ddb/mysql/my3306.cnf &
```

#### 查看 root 密码

查看 MySQL 数据目录下的 `mysqld.log` 日志文件，如下图所示红框的地方即为 root 的初始密码。

![image-20210604114352669](/images/2021/06/image-20210604114352669.png)

#### 访问 root

```bash
$ mysql  --defaults-file=/home/ddb/mysql/my4336.cnf -uroot -p
Enter password:

mysql> show databases;
ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.
```

此时，必须修改 root 密码。

#### 修改 root 密码

```mysql
SET PASSWORD = PASSWORD('newpassword');
ALTER USER 'root'@'localhost' PASSWORD EXPIRE NEVER;
FLUSH PRIVILEGES;
```

### 问题处理

#### 安装 deb 异常

安装 deb 包时出现如下异常：

```
dpkg: dependency problems prevent configuration of mysql-community-server:
 mysql-community-server depends on libaio1 (>= 0.3.93); however:
  Package libaio1 is not installed.
 mysql-community-server depends on libmecab2; however:
  Package libmecab2 is not installed.
 mysql-community-server depends on libnuma1 (>= 2.0.11); however:
  Package libnuma1 is not installed.
```

解决方式：

```bash
$ apt-get install libaio1 libmecab2 libnuma1
```

#### 初始化异常

```
2021-06-04T11:13:04.485999+08:00 0 [Warning] TIMESTAMP with implicit DEFAULT value is deprecated. Please use --explicit_defaults_for_timestamp server option (see documentation for more details).
2021-06-04T11:13:04.487043+08:00 0 [ERROR] --initialize specified but the data directory has files in it. Aborting.
2021-06-04T11:13:04.487070+08:00 0 [ERROR] Aborting
```

这是由于初始化数据目录不为空，清空数据目录下的所有文件即可。