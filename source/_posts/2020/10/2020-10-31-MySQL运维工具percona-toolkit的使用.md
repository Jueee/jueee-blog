---
title: MySQL运维工具percona-toolkit的使用
layout: info
commentable: true
date: 2020-10-31
mathjax: true
mermaid: true
tags: [MySQL]
categories: MySQL
description: 
---

percona-toolkit 是一组高级命令行工具的集合，可以查看当前服务的摘要信息，磁盘检测，分析慢查询日志，查找重复索引，实现表同步等等。

官网：https://www.percona.com/software/database-tools/percona-toolkit

<!--more-->

### 安装 percona-toolkit

#### 仓库安装

- Debian

  ```bash
  $ apt-cache search percona-toolkit
  percona-toolkit - Advanced MySQL and system command-line tools
  $ sudo apt-get install percona-toolkit
  ```

#### 下载安装

访问 [下载地址](https://www.percona.com/downloads/percona-toolkit/LATEST/)，根据系统版本选择对应的版本进行下载。

- Debian

  ```bash
  sudo dpkg -i percona-toolkit_3.2.1-1.buster_amd64.deb
  ```

### pt-query-digest

pt-query-digest主要用来分析mysql的慢日志，并格式化输出以便于查看和分析。

#### 报告分析

- **总体统计结果**
  - Overall：总共有多少条查询 
  - Time range：查询执行的时间范围 
  - unique：唯一查询数量，即对查询条件进行参数化以后，总共有多少个不同的查询 
  - total：总计 
  - min：最小 
  - max：最大 
  - avg：平均 95%：把所有值从小到大排列，位置位于95%的那个数，这个数一般最具有参考价值 
  - median：中位数，把所有值从小到大排列，位置位于中间那个数
- **查询分组统计结果**
  - Rank：所有语句的排名，默认按查询时间降序排列，通过--order-by指定 
  - Query ID：语句的ID，（去掉多余空格和文本字符，计算hash值） 
  - Response：总的响应时间 
  - time：该查询在本次分析中总的时间占比 
  - calls：执行次数，即本次分析总共有多少条这种类型的查询语句 
  - R/Call：平均每次执行的响应时间 
  - V/M：响应时间Variance-to-mean的比率 
  - Item：查询对象
- **每一种查询的详细统计结果**
  - ID：查询的ID号，和上图的Query ID对应 
  - Databases：数据库名 
  - Users：各个用户执行的次数（占比） 
  - Query_time distribution ：查询时间分布, 长短体现区间占比。
  - Tables：查询中涉及到的表 
  - Explain：SQL语句。

#### 使用示例

- 直接分析慢查询文件：

  ```bash
  $ pt-query-digest mysql-bin.288298.log > report1.log
  ```

- 解析MySQL 的 Binlog 日志：

  ```bash
  $ mysqlbinlog mysql-bin88.0001 > mysql-bin88.0001.sql
  $ pt-query-digest mysql-bin.288298.log > report1.log
  ```


### 参考资料

- https://www.cnblogs.com/javastack/p/12606106.html

