---
title: OpenOffice简要介绍和安装说明
layout: info
commentable: true
date: 2020-12-21
mathjax: true
mermaid: true
tags: [Apache,OpenOffice]
categories: [Apache,OpenOffice]
description: 
---

### OpenOffice 介绍

**OpenOffice.org** 是一套跨平台的办公室软件套件，能在 Windows、Linux、MacOS X (X11)、和 Solaris 等操作系统上执行。它与各个主要的办公室软件套件兼容。

OpenOffice.org 的主要模块有：

- Writer(文本文档)
- Calc(电子表格)
- Impress(演示文稿)
- Math(公式计算)
- Draw(画图)
- Base(数据库)

<!--more-->

### OpenOffice 相关链接

- 官网：https://openoffice.apache.org/、http://www.openoffice.org/
- 下载：http://www.openoffice.org/download/
- GitHub：https://github.com/apache/openoffice

### 安装 OpenOffice

#### Debian 安装

1. 下载 OpenOffice 软件包

   下载地址：http://www.openoffice.org/zh-cn/download/

   版本：deb 64 选择 `Linux 64-bit (x86-64) (DEB)`

2. 解压软件包

   ```bash
   tar -zxvf Apache_OpenOffice_4.1.7_Linux_x86-64_install-deb_zh-CN.tar.gz
   ```

3. 安装 OpenOffice

   ```bash
   cd zh-CN/DEBS
   sudo dpkg -i *.deb
   cd desktop-integration
   sudo dpkg -i *.deb
   ```

4. 启动 OpenOffice

   ```bash
   sudo soffice --headless --accept="socket,host=127.0.0.1,port=8100;urp;" --nofirststartwizard &
   ```

#### Windows 安装

1. 下载 `Apache_OpenOffice_4.1.8_Win_x86_install_zh-CN.exe`
2. 双击进行安装。
3. 安装后，在 `C:\Program Files (x86)\OpenOffice 4` 目录下。

#### 异常处理

运行程序报错：

```bash
$ soffice --headless --accept="socket,host=127.0.0.1,port=8100;urp;" --nofirststartwizard
X11 connection rejected because of wrong authentication.
X11 connection rejected because of wrong authentication.
/opt/openoffice4/program/soffice.bin X11 error: Can't open display:
   Set DISPLAY environment variable, use -display option
   or check permissions of your X-Server
   (See "man X" resp. "man xhost" for details)
```

需安装 X11：

```bash
apt-get install xvfb
apt-get install x11-xserver-utils
apt-get install tightvncserver tightvnc-java
```



