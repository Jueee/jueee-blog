---
title: Windows系统下的MySQL版本升级
layout: info
commentable: true
date: 2021-03-10
mathjax: true
mermaid: true
tags: [Windows,Database,MySQL]
categories: [Database,MySQL]
description: 
---

最近因原先的 MySQL 版本过低，所以希望将Windows下的MySQL5.5升级为MySQL5.7。记录一下升级过程。

<!--more-->

### 下载MySQL

- MySQL下载地址：https://dev.mysql.com/downloads/mysql/
- MySQL 5.7.33.0：https://dev.mysql.com/downloads/file/?id=500616

### 移除旧版本 MySQL

管理员身份运行，先停止 MySQL 服务，然后移除 MySQL。

```powershell
C:\WINDOWS\system32>cd C:\Program Files (x86)\MySQL\MySQL Server 5.5\bin

C:\Program Files (x86)\MySQL\MySQL Server 5.5\bin>mysqld --remove MySQL
Failed to remove the service because the service is running
Stop the service and try again

C:\Program Files (x86)\MySQL\MySQL Server 5.5\bin>net stop MySQL
MySQL 服务正在停止.
MySQL 服务已成功停止。

C:\Program Files (x86)\MySQL\MySQL Server 5.5\bin>mysqld --remove MySQL
Service successfully removed.
```

如果报错 `The service doesn't exist!`，则需要在任务管理器 -> 服务中，查找一下具体的MySQL服务名

### 备份数据

1. 将旧版本的data文件和 my.ini 文件复制至5.7路径下。
2. 重命名旧版本安装目录，避免混淆。
3. 查看并修改 my.ini 文件中的路径配置。

my.ini 配置后如下：

```ini
#Path to installation directory. All paths are usually resolved relative to this.
basedir="C:/Program Files (x86)/MySQL/mysql-5.7.33-win32/"
#Path to the database root
datadir="C:/ProgramData/MySQL/mysql-5.7.33-win32/Data/"
```

### 添加新MySQL

```bash
mysqld.exe --install MySQL
```

启动MySQL：

```bash
net start MySQL
```

![image-20210310150046355](/images/2021/03/image-20210310150046355.png)

### 问题解决

```bash
mysqld --console
```

打印如下：

```
[ERROR] unknown variable 'table_cache=256'
[ERROR] Aborting
```

去除 my.ini 文件中的 table_cache 属性配置。

```
[ERROR] unknown variable 'innodb_additional_mem_pool_size=2M'
[ERROR] Aborting
```

去除 my.ini 文件中的 innodb_additional_mem_pool_size 属性配置。

### 升级 MySQL

```bash
mysql_upgrade -uroot -p
```

![image-20210310145814403](/images/2021/03/image-20210310145814403.png)

重新启动 MySQL 服务：

![image-20210310145649486](/images/2021/03/image-20210310145649486.png)

至此，MySQL升级就算完成了。

验证 MySQL 新版本：

![image-20210310151140637](/images/2021/03/image-20210310151140637.png)