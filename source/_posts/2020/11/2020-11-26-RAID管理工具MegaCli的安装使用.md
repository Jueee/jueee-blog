---
title: RAID管理工具MegaCli的安装使用
layout: info
commentable: true
date: 2020-11-26
mathjax: true
mermaid: true
tags: [Linux,软件,RAID]
categories: [Linux,软件]
description: 
---

### MegaCli 介绍

MegaCli 是一款管理维护硬件RAID软件，可以通过它来了解当前raid卡的所有信息，包括 raid卡的型号，raid的阵列类型，raid 上各磁盘状态，等等。

<!--more-->

### MegaCli 安装

#### 下载安装

方案一

```bash
apt-get install alien
wget --user=hetzner --password=download http://download.hetzner.de/tools/LSI/tools/MegaCLI/8.07.14_MegaCLI.zip
unzip 8.07.14_MegaCLI.zip -d megacli
cd megacli/Linux
sudo alien MegaCli-8.07.14-1.noarch.rpm
sudo dpkg -i megacli_8.07.14-2_all.deb
ln -s /opt/MegaRAID/MegaCli/MegaCli64 /usr/bin/megacli
```

方案二

```bash
apt-get -y install  rpm2cpio libsysfs2 libsysfs-dev unzip
unzip 8.00.48_Linux_MegaCLI.zip
unzip MegaCliLin.zip
rpm2cpio Lib_Utils-1.00-09.noarch.rpm | cpio -idmv
rpm2cpio MegaCli-8.00.48-1.i386.rpm | cpio -idmv
ln -s opt/MegaRAID/MegaCli/MegaCli64 /usr/bin/megacli64
ln -s opt/MegaRAID/MegaCli/MegaCli /usr/bin/megacli
```

#### 验证安装

```bash
$  megacli -v
      MegaCLI SAS RAID Management Tool  Ver 8.07.14 Dec 16, 2013
    (c)Copyright 2013, LSI Corporation, All Rights Reserved.
Exit Code: 0x00
```

#### 安装异常

问题：

```bash
$ megacli
megacli: error while loading shared libraries: libncurses.so.5: cannot open shared object file: No such file or directory
```

解决

```bash
$ apt-get install libncurses5
```

### 命令汇总

- 查看raid卡日志

  megacli -FwTermLog -Dsply -aALL

- 显示适配器个数

  megacli -adpCount

- 显示适配器时间

  megacli -AdpGetTime –aALL

- 显示所有适配器信息

  megacli -AdpAllInfo -aAll

- 显示所有逻辑磁盘组信息

  megacli -LDInfo -LALL -aAll

- 查raid卡信息(生产商、电池信息及所支持的raid级别)

  megacli -AdpAllInfo -aALL |grep -E "Product Name|BBU|Memory Size|RAID Level Supported"

- 查看虚拟化(vd)和物理盘(pd)的信息，比如查看物理硬盘数，是否有硬盘offline或者degraded

  megacli -AdpAllInfo -aALL |grep -E "Device Present" -A9

- 查看硬盘是否online

  megacli -PDList -aALL |grep "Firmware state"

- 查看硬盘是否存在物理错误(error不为0，可能会有硬盘故障即将发生)

  megacli -PDList -aALL |grep -i error

- 查看电池信息(电池类型、电池状态、充电状态、温度等)

  megacli -AdpBbuCmd -aAll

- raid卡个数

  megacli –adpCount

- 检测磁盘 ID 注意, 该ID 值用于标注磁盘

  megacli -PDlist -aALL | grep "ID" | uniq

- 显示所有逻辑磁盘组信息(做了几组raid，raid cache的默认和当前策略，做好raid后的虚拟盘容量)

  megacli -LDInfo -LALL -aAll

- 显示所有物理盘(物理磁盘个数、大小、是否存在error)

  megacli -PDList -aAll

- 显示所有物理盘物理错误

  megacli -PDList -aAll |grep -i error

- 查看充电状态

  megacli -AdpBbuCmd -GetBbuStatus -aALL |grep 'Charger Status'

- 显示BBU状态信息，比如电池是否,如果issohgood为Yes为正常，No为异常
      

  megacli -AdpBbuCmd -GetBbuStatus -aALL|grep -i issohgood

- 显示BBU状态信息

  megacli -AdpBbuCmd -GetBbuStatus -aALL

- 显示BBU容量信息

  megacli -AdpBbuCmd -GetBbuCapacityInfo -aALL

- 显示BBU设计参数

  megacli -AdpBbuCmd -GetBbuDesignInfo -aALL

- 显示当前BBU属性

  megacli -AdpBbuCmd -GetBbuProperties -aALL

- 显示Raid卡型号，cache大小、Raid设置，cache策略、Disk相关信息

  megacli -cfgdsply -aALL |egrep "PDs|VDs|Product Name|Memory|BBU:"

- 查看磁盘缓存策略(查看vd的)

  megacli -LDGetProp -Cache -LALL -aALL

- 查看磁盘缓存策略(查看pd的)

  megacli -LDGetProp -DskCache -LALL -aALL

- 查看物理磁盘重建进度

  megacli -PDRbld -ShowProg -PhysDrv [1:5] -a0

- 以动态可视化文字界面显示

  megacli -PDRbld -ProgDsply -PhysDrv [1:5] -a0

- 关闭缓存

  megacli -LDSetProp -DisDskCache -L0 -a0

- 显示Rebuid进度

  megacli -PDRbld -ShowProg -physdrv[20:2] -aALL

- 查看E S

  megacli -PDList -aAll -NoLog | grep -Ei "(enclosure|slot)"

- 查看所有硬盘的状态

  megacli -PDList -aAll -NoLog

- 查看所有Virtual Disk的状态

  megacli -LdPdInfo -aAll -NoLog

- 在线做Raid

  megacli -CfgLdAdd -r0[0:11] WB NORA Direct CachedBadBBU -strpsz64 -a0 -NoLog

  megacli -CfgLdAdd -r5 [12:2,12:3,12:4,12:5,12:6,12:7] WB Direct -a0

- 点亮指定硬盘(定位)

  megacli -PdLocate -start -physdrv[252:2] -a0

- 清除Foreign状态

  megacli -CfgForeign -Clear -a0

- 查看RAID阵列中掉线的盘

  megacli -pdgetmissing -a0

- 替换坏掉的模块

  megacli -pdreplacemissing -physdrv[12:10] -Array5 -row0 -a0

- 手动开启rebuid

  megacli -pdrbld -start -physdrv[12:10] -a0

- 查看Megacli的log

  megacli -FwTermLog dsply -a0 > adp2.log

- 设置HotSpare

  megacli -pdhsp -set [-Dedicated [-Array2]] [-EnclAffinity] [-nonRevertible] -PhysDrv[4:11] -a0

  megacli -pdhsp -set [-EnclAffinity] [-nonRevertible] -PhysDrv[32：1}] -a0

- 关闭Rebuild

  megacli -AdpAutoRbld -Dsbl -a0

- 设置rebuild的速率

  megacli -AdpSetProp RebuildRate -30 -a0

- 创建一个 raid5 阵列，由物理盘 2,3 4 构成，该阵列的热备盘是物理盘 5

  megacli-CfgLdA d -r5 [1:2,1:3,1:4] WB Direct -Hsp[1:5] -a0

- 创建阵列，不指定热备

  megacli-CfgLdA d -r5 [1:2,1:3,1:4] WB Direct -a0

- 删除阵列

  megacli-CfgLdDel -L1 -a0

- 在线添加磁盘

  megacli-LDRecon -Star - 5 Ad -PhysDrv[1:4] -L1 -a0

- 阵列创建完后，会有一个初始化同步块的过程，可以看 其进度。

  megacli-LDInit -ShowProg -LA L -aAL

- 以动态可视化文字界面显示

  megacli-LDInit -ProgDsply -LA L -aAL

- 查看阵列后台初始化进度

  megacli-LDBI -ShowProg -LA L -aAL

- 或者以动态可视化文字界面显示

  megacli-LDBI -ProgDsply -LA L -aAL

- 指定第 5 块盘作为全局热备

  megacli-PDHSP -Set [-EnclAf in ty] [-no Rev rtible] -PhysDrv[1:5] -a0

- 指定为某个阵列的专用热备

  megacli-PDHSP -Set [-Dedicated [-Ar ay1] [-EnclAf in ty] [-no Rev rtible] -PhysDrv[1:5] -a0

- 删除全局热备

  megacli-PDHSP -Rmv -PhysDrv[1:5] -a0

- 将某块物理盘下线/上线

  megacli -PDOffline -PhysDrv [1:4] -a0

  megacli -PDOnline -PhysDrv [1:4] -a0

- 查看物理磁盘重建进度

  megacli-PDRbld -ShowProg -PhysDrv [1:5] -a0

- 或者以动态可视化文字界面显示

  megacli -PDRbld -ProgDsply -PhysDrv [1:5] -a0

- 查看做 raid 的情况

  megacli -LDInfo -Lal -aAL | grep -E "RAID Lev l|Strip Size|NumberOf Drives|Span Depth|^Size"

- 取 Enclosure Device ID

  uiqnum=` megacli -PDlist -aAL | grep "ID" | uniq |awk -F: '{print $2}' | awk '{print $1}'`

- 取 Slot Number

  disknum=`megacli -PDList -aAL | grep -E "DISK GROUP|Slot Number|postion:|Firmware sta e:" | grep Slot | awk -F[: ] '{print $NF}'`

- 算出总数

  diskto al=`megacli -PDList -aAL | grep -E "DISK GROUP|Slot Number|postion:|Firmware sta e:" | grep Slot | awk -F[: ] '{print $NF}' | wc -l`
  ar ay=($disknum)

- 查看当前raid缓存状态，raid缓存状态设置为wb的话要注意电池放电事宜，设置电池放电模式为自动学习模式

  megacli   -ldgetprop  -dskcache -lall  -aall

- raid 电池设置相关

  - 查看电池状态信息(Display BBU Status Information)

    megacli -AdpBbuCmd -GetBbuStatus -aN|-a0,1,2|-aALL

    megacli -AdpBbuCmd -GetBbuStatus -aALL

  - 查看电池容量（Display BBU Capacity Information）

    megacli -AdpBbuCmd -GetBbuCapacityInfo -aN|-a0,1,2|-aALL

    megacli -AdpBbuCmd -GetBbuCapacityInfo –aALL

  - 查看电池设计参数(Display BBU Design Parameters)

    megacli -AdpBbuCmd -GetBbuDesignInfo -aN|-a0,1,2|-aALL

    megacli -AdpBbuCmd -GetBbuDesignInfo –aALL

  - 查看电池属性（Display Current BBU Properties）

    megacli -AdpBbuCmd -GetBbuProperties -aN|-a0,1,2|-aALL

    megacli -AdpBbuCmd -GetBbuProperties –aALL

  - 设置电池为学习模式为循环模式（Start BBU Learning Cycle）

    megacli -AdpBbuCmd -BbuLearn -aN|-a0,1,2|-aALL

- 查询raid级别，磁盘数量，容量，条带大小。

  megacli -cfgdsply -aALL |grep Policy

- 查询控制器cache策略

  megacli -LDSetProp WB -L0 -a0

- 设置write back功能

  megacli -LDSetProp CachedBadBBU -L0 -a0

- 设置即使电池坏了还是保持WB功能

  megacli -AdpBbuCmd -BbuLearn a0

- 手动充电

  megacli -FwTermLog -Dsply -aALL

- 显示适配器个数： 

  megacli -adpCount

- 显示所有适配器信息： 

  megacli -AdpAllInfo -aAll

- 显示所有逻辑磁盘组信息： 

  megacli -LDInfo -LALL -aAll

- 显示所有的物理信息： 

  megacli -PDList -aAll
  Media

- 查看充电状态： 

  megacli -AdpBbuCmd -GetBbuStatus -aALL

- 显示BBU(后备电池)状态信息： 

  megacli -AdpBbuCmd -GetBbuStatus -aALL

- 显示BBU容量信息： 

  megacli -AdpBbuCmd -GetBbuCapacityInfo -aALL

- 显示BBU设计参数： 

  megacli -AdpBbuCmd -GetBbuDesignInfo -aALL

- 显示当前BBU属性： 

  megacli -AdpBbuCmd -GetBbuProperties -aALL

- 显示Raid卡型号，Raid设置，Disk相关信息： 

  megacli -cfgdsply -aALL

- 查看Cache 策略设置： 

  megacli -cfgdsply -aALL |grep -i Policy

- 查看充电进度百分比： 

  megacli -AdpBbuCmd -GetBbuStatus -aALL

### 参考资料

- https://idc.wanyunshuju.com/cym/646.html
- https://gist.github.com/fxkraus/595ab82e07cd6f8e057d31bc0bc5e779
- https://blog.csdn.net/xinqidian_xiao/article/details/80940306