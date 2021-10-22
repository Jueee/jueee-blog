---
title: MySQL清理binlog日志的方法
layout: info
commentable: true
date: 2021-10-11
mathjax: true
mermaid: true
tags: [Database,MySQL]
categories: [Database,MySQL]
description: 
---

MySQL中的binlog日志记录了数据库中数据的变动，便于对数据的基于时间点和基于位置的恢复，但是binlog也会日渐增大，占用很大的磁盘空间，因此，要对binlog使用正确安全的方法清理掉一部分没用的日志。

<!--more-->

### 自动清理

通过设置 binlog 过期的时间，使系统自动删除 binlog 文件。

查看 binlog 过期日期配置：

```mysql
mysql> show variables like 'expire_logs_days';
+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| expire_logs_days | 7     |
+------------------+-------+
1 row in set (0.00 sec)
```

设置 binlog 过期日期：

```mysql
mysql> set global expire_logs_days = 30;
```

在 my.ini 中设置过期时间：

```ini
[mysqld]

expire_logs_days = 7
```

### 手动清理

清理前的准备：

1. 查看主库和从库正在使用的binlog是哪个文件

   ```mysql
   mysql> show master status\G
   mysql> show slave status\G
   ```

2. 在删除binlog日志之前，首先对binlog日志备份，以防万一。

删除指定日期以前的日志索引中binlog日志文件：

```mysql
mysql> purge master logs before '2021-10-11 17:20:00';
```

删除指定日志文件的日志索引中binlog日志文件：

```mysql
mysql> purge master logs to 'mysql-bin.000022';
```

**注意**：

时间和文件名一定不可以写错，尤其是时间中的年和文件名中的序号，以防不小心将正在使用的 binlog 删除！

**切勿删除正在使用的 binlog！！！**

使用该语法，会将对应的文件和 mysql-bin.index 中的对应路径删除。

### 清理脚本

自动清理 binlog ，只保留最近 50 个：

```sh
#!/bin/sh
# incr backup of mysql
cd /mysqldata
# get the last binary log
LASTBIN=`tail -n 50 mysql-bin.index| head -n 1`
echo $LASTBIN
LASTBINFILE=`basename $LASTBIN`
echo $LASTBINFILE
# purge binary logs to the last binary log
/bin/mysql --defaults-file=/mysql/my1.cnf  -uroot  -e"purge binary logs to '${LASTBINFILE}'"
```

可以将该脚本配置进入 crontab。

### 注意

过期时间设置的要适当，对于主从复制等读取 binlog 的情况，要看从库的延迟决定过期时间，避免主库 binlog 还未传到从库便因过期而删除，导致主从不一致！！！