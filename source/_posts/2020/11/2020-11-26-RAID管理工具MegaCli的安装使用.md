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

```shell
wget --user=hetzner --password=download http://download.hetzner.de/tools/LSI/tools/MegaCLI/8.07.14_MegaCLI.zip
unzip 8.07.14_MegaCLI.zip -d megacli
cd megacli/Linux
sudo alien MegaCli-8.07.14-1.noarch.rpm
sudo dpkg -i megacli_8.07.14-2_all.deb
ln -s /opt/MegaRAID/MegaCli/MegaCli64 /usr/bin/megacli
```

#### 安装异常

问题：

```
$ megacli
megacli: error while loading shared libraries: libncurses.so.5: cannot open shared object file: No such file or directory
```



### 参考资料

- https://idc.wanyunshuju.com/cym/646.html
- https://gist.github.com/fxkraus/595ab82e07cd6f8e057d31bc0bc5e779
- https://blog.csdn.net/xinqidian_xiao/article/details/80940306