---
title: Linux安装使用iostat命令
layout: info
commentable: true
date: 2020-12-16
mathjax: true
mermaid: true
tags: [OS,Linux]
categories: 
- [OS,Linux]
categories: 
description: 
---

### iostat 介绍

**iostat命令** 被用于监视系统输入输出设备和CPU的使用情况。

它的特点是汇报磁盘活动统计情况，同时也会汇报出CPU使用情况。

同vmstat一样，iostat也有一个弱点，就是它不能对某个进程进行深入分析，仅对系统的整体情况进行分析。

<!--more-->

### 安装 iostat

centos 安装：

```bash
yum install sysstat
```

Debian 安装：

```bash
apt-get install sysstat
```

包下载：

- Debian 8：https://packages.debian.org/jessie/sysstat
- Debian 9：https://packages.debian.org/stretch/sysstat
- Debian 10：https://packages.debian.org/buster/sysstat

### 使用 iostat

选项

- -c：仅显示CPU使用情况；
- -d：仅显示设备利用率；
- -k：显示状态以千字节每秒为单位，而不使用块每秒；
- -m：显示状态以兆字节每秒为单位；
- -p：仅显示块设备和所有被使用的其他分区的状态；
- -t：显示每个报告产生时的时间；
- -V：显示版号并退出；
- -x：显示扩展状态。

参数：

- 间隔时间：每次报告的间隔时间（秒）；
- 次数：显示报告的次数。

### 使用示例

#### -d 参数

参数 -d 表示，显示设备（磁盘）使用状态。

```
$ iostat -d 10
Linux 4.9.0-8-amd64 (mant)      2020年12月16日  _x86_64_        (4 CPU)

Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
sda               1.55        16.98        28.18    8690027   14417430
sdb              10.62        21.86       192.73   11187053   98614636
```

输出信息的含义：

- tps：该设备每秒的传输次数。"一次传输"意思是"一次I/O请求"。多个逻辑请求可能会被合并为"一次I/O请求"。"一次传输"请求的大小是未知的。
- kB_read/s：每秒从设备读取的数据量；
- kB_wrtn/s：每秒向设备写入的数据量；
- kB_read：读取的总数据量；
- kB_wrtn：写入的总数量数据量。

这些单位都为Kilobytes。

#### -c 参数

-c 参数显示CPU使用情况：

```bash
$ iostat -c
Linux 4.9.0-8-amd64 (mant)      2020年12月16日  _x86_64_        (4 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
          58.94    0.00    2.70    1.26    0.00   37.10
```

输出信息的含义：

- %user：CPU处在用户模式下的时间百分比。
- %nice：CPU处在带NICE值的用户模式下的时间百分比。
- %system：CPU处在系统模式下的时间百分比。
- %iowait：CPU等待输入输出完成时间的百分比。
- %steal：管理程序维护另一个虚拟处理器时，虚拟CPU的无意识等待时间百分比。
- %idle：CPU空闲时间百分比。

**备注：**如果%iowait的值过高，表示硬盘存在I/O瓶颈，%idle值高，表示CPU较空闲，如果%idle值高但系统响应慢时，有可能是CPU等待分配内存，此时应加大内存容量。%idle值如果持续低于10，那么系统的CPU处理能力相对较低，表明系统中最需要解决的资源是CPU。

#### -x 参数

每隔三秒查看一次完整信息：

```bash
$ iostat -x 3
Linux 4.9.0-8-amd64 (mant)      2020年12月16日  _x86_64_        (4 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
          58.88    0.00    2.71    1.26    0.00   37.16

Device:         rrqm/s   wrqm/s     r/s     w/s    rkB/s    wkB/s avgrq-sz avgqu-sz   await r_await w_await  svctm  %util
sda               1.48     5.77    1.07    0.47    17.03    28.25    58.50     0.00    1.86    0.99    3.83   0.92   0.14
sdb               0.08    15.77    0.68    9.95    21.93   193.02    40.43     0.27   25.60   36.17   24.88   6.47   6.88
```

输出信息的含义：

- rrqm/s：每秒这个设备相关的读取请求有多少被Merge了（当系统调用需要读取数据的时候，VFS将请求发到各个FS，如果FS发现不同的读取请求读取的是相同Block的数据，FS会将这个请求合并Merge）；
- wrqm/s：每秒这个设备相关的写入请求有多少被Merge了。
- r/s：每秒读取的扇区数；
- w/s：每秒写入的扇区数。
- rKB/s：每秒发送到设备的读取请求数。
- wKB/s：每秒向设备发出的写请求数。
- avgrq-sz 平均请求扇区的大小
- avgqu-sz 是平均请求队列的长度。毫无疑问，队列长度越短越好。    
- await：  每一个IO请求的处理的平均时间（单位是微秒毫秒）。这里可以理解为IO的响应时间，一般地系统IO响应时间应该低于5ms，如果大于10ms就比较大了。这个时间包括了队列时间和服务时间，也就是说，一般情况下，await大于svctm，它们的差值越小，则说明队列时间越短，反之差值越大，队列时间越长，说明系统出了问题。
- svctm    表示平均每次设备I/O操作的服务时间（以毫秒为单位）。如果svctm的值与await很接近，表示几乎没有I/O等待，磁盘性能很好，如果await的值远高于svctm的值，则表示I/O队列等待太长，         系统上运行的应用程序将变慢。
- %util： 在统计时间内所有处理IO时间，除以总共统计时间。例如，如果统计间隔1秒，该设备有0.8秒在处理IO，而0.2秒闲置，那么该设备的%util = 0.8/1 = 80%，所以该参数暗示了设备的繁忙程度。一般地，如果该参数是100%表示设备已经接近满负荷运行了（当然如果是多磁盘，即使%util是100%，因为磁盘的并发能力，所以磁盘使用未必就到了瓶颈）。