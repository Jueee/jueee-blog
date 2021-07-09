---
title: 使用binlog2sql恢复MySQL数据
layout: info
commentable: true
date: 2021-06-08
mathjax: true
mermaid: true
tags: [Database,MySQL]
categories: [Database,MySQL]
description: 
---

### binlog2sql

从 MySQL binlog 解析出你要的 SQL。根据不同选项，你可以得到原始 SQL、回滚SQL、去除主键的 INSERT SQL等。

- [GitHub](https://github.com/danfengcao/binlog2sql)

<!--more-->

### 使用条件

#### 开启 bin-log

MySQL Server 必须开启 bin-log 配置。

```ini
[mysqld]
server_id = 1
log_bin = "C:/Program Files (x86)/MySQL/mysql-5.7.33-win32/mysql-bin.log"
max_binlog_size = 1G
binlog_format = row
binlog_row_image = full
```

查看 bin-log 类型：

```
show global variables like '%format%';
```

#### 安装Python依赖

安装 pymysql

```
pip3 install pymysql
```

安装 [mysql-replication](https://github.com/noplay/python-mysql-replication)

```
pip3 install mysql-replication
```

安装 [pymysql-utils](https://pypi.org/project/pymysql-utils/)

```
pip3 install --user pymysql==0.10.1
```

mysql-replication 模块依赖PyMySQL模块，并且在 PyMySQL 模块1.0.0之后，移除了【pymysql.util】

#### 异常处理

异常：

```
Traceback (most recent call last):
  File ".\binlog2sql.py", line 150, in <module>
    back_interval=args.back_interval, only_dml=args.only_dml, sql_type=args.sql_type)
  File ".\binlog2sql.py", line 48, in __init__
    with self.connection as cursor:
AttributeError: __enter__
```

需要将 binlog2sql.py 文件第 48 行，修改为：

```python
with self.connection.cursor() as cursor:
```

异常：

```
<pymysql.connections.Connection object at 0x03476BD0>
Traceback (most recent call last):
  File ".\binlog2sql.py", line 151, in <module>
    binlog2sql.process_binlog()
  File ".\binlog2sql.py", line 74, in process_binlog
    with temp_open(tmp_file, "w") as f_tmp, self.connection as cursor:
AttributeError: __enter__
```

需要将 binlog2sql.py 文件第 74 行，修改为：

```
with temp_open(tmp_file, "w") as f_tmp, self.connection.cursor() as cursor:
```

### 参数说明

**mysql连接配置**

-h host; -P port; -u user; -p password

**解析模式**

--stop-never 持续解析binlog。可选。默认False，同步至执行命令时最新的binlog位置。

-K, --no-primary-key 对INSERT语句去除主键。可选。默认False

-B, --flashback 生成回滚SQL，可解析大文件，不受内存限制。可选。默认False。与stop-never或no-primary-key不能同时添加。

--back-interval -B模式下，每打印一千行回滚SQL，加一句SLEEP多少秒，如不想加SLEEP，请设为0。可选。默认1.0。

**解析范围控制**

--start-file 起始解析文件，只需文件名，无需全路径 。必须。

--start-position/--start-pos 起始解析位置。可选。默认为start-file的起始位置。

--stop-file/--end-file 终止解析文件。可选。默认为start-file同一个文件。若解析模式为stop-never，此选项失效。

--stop-position/--end-pos 终止解析位置。可选。默认为stop-file的最末位置；若解析模式为stop-never，此选项失效。

--start-datetime 起始解析时间，格式'%Y-%m-%d %H:%M:%S'。可选。默认不过滤。

--stop-datetime 终止解析时间，格式'%Y-%m-%d %H:%M:%S'。可选。默认不过滤。

**对象过滤**

-d, --databases 只解析目标db的sql，多个库用空格隔开，如-d db1 db2。可选。默认为空。

-t, --tables 只解析目标table的sql，多张表用空格隔开，如-t tbl1 tbl2。可选。默认为空。

--only-dml 只解析dml，忽略ddl。可选。默认False。

--sql-type 只解析指定类型，支持INSERT, UPDATE, DELETE。多个类型用空格隔开，如--sql-type INSERT DELETE。可选。默认为增删改都解析。用了此参数但没填任何类型，则三者都不解析。

### 使用方式

使用示例：

```
python .\binlog2sql.py -hlocalhost -P3306 -uroot -p'jue' --start-file='mysql-bin.000001' --stop-file='mysql-bin.000003'
```

使用示例：

```
python .\binlog2sql.py -h'XX.XX.XX.XX' -P3306 -uXXX -pXXX -dXXX -tXXX --start-file='mysql-bin.335529'
```

### 异常处理

异常：

```
error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools"
```

访问 [下载](https://visualstudio.microsoft.com/zh-hans/visual-cpp-build-tools/)，安装 C++ 库文件。

异常：

```
	C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Tools\MSVC\14.29.30037\bin\HostX86\x86\cl.exe /c /nologo /Ox /W3 /GL /DNDEBUG /MT -Dversion_info=(2,0,3,'final',0) -D__version__=2.0.3 "-IC:\Program Files (x86)\MySQL\MySQL Connector C 6.1\include\mariadb" -Ic:\greensoftware\python\python37\include -Ic:\greensoftware\python\python37\include "-IC:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Tools\MSVC\14.29.30037\include" /TcMySQLdb/_mysql.c /Fobuild\temp.win32-3.7\Release\MySQLdb/_mysql.obj
    _mysql.c
    MySQLdb/_mysql.c(29): fatal error C1083: 无法打开包括文件: “mysql.h”: No such file or directory
```



```
fatal error C1083: 无法打开包括文件: “corecrt.h”: No such file or directory
```

勾选“Windows Universal CRT SDK”，安装它。

```
fatal error C1083: 无法打开包括文件: “windows.h”: No such file or directory
```

