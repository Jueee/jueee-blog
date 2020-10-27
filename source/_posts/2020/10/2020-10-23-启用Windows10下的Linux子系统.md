---
title: 启用Windows10下的Linux子系统
layout: info
commentable: true
date: 2020-10-23
mathjax: true
mermaid: true
tags: [Windows,软件,Linux]
categories: 
- [软件,Windows]
- [Linux]
description: 
---

### WSL 介绍

Windows Subsystem for Linux（简称WSL）是一个在Windows 10上能够运行原生Linux二进制可执行文件（ELF格式）的兼容层。

官网：https://docs.microsoft.com/zh-cn/windows/wsl/

<!--more-->

### 启用 WSL

需要先启用“适用于 Linux 的 Windows 子系统”可选功能，然后才能在 Windows 上安装 Linux 分发。

以管理员身份打开 PowerShell 并运行：

```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

如下图所示：

![image-20201022164416572](/images/2020/10/image-20201022164416572.png)

然后，**重新启动计算机**。

### 安装 Linux

打开 [Microsoft Store](https://aka.ms/wslstore)，并选择你偏好的 Linux 分发版。

单击以下链接会打开每个分发版的 Microsoft Store 页面：

- [Ubuntu 16.04 LTS](https://www.microsoft.com/store/apps/9pjn388hp8c9)
- [Ubuntu 18.04 LTS](https://www.microsoft.com/store/apps/9N9TNGVNDL3Q)
- [Ubuntu 20.04 LTS](https://www.microsoft.com/store/apps/9n6svws3rx71)
- [openSUSE Leap 15.1](https://www.microsoft.com/store/apps/9NJFZK00FGKV)
- [SUSE Linux Enterprise Server 12 SP5](https://www.microsoft.com/store/apps/9MZ3D1TRP8T1)
- [SUSE Linux Enterprise Server 15 SP1](https://www.microsoft.com/store/apps/9PN498VPMF3Z)
- [Kali Linux](https://www.microsoft.com/store/apps/9PKR34TNCV07)
- [Debian GNU/Linux](https://www.microsoft.com/store/apps/9MSVKQC78PK6)
- [Fedora Remix for WSL](https://www.microsoft.com/store/apps/9n6gdm4k2hnc)
- [Pengwin](https://www.microsoft.com/store/apps/9NV1GV1PXZ6P)
- [Pengwin Enterprise](https://www.microsoft.com/store/apps/9N8LP0X93VCP)
- [Alpine WSL](https://www.microsoft.com/store/apps/9p804crf0395)

在分发版的页面中，选择“获取”。

### 设置新分发

首次启动新安装的 Linux 分发版时，将打开一个控制台窗口，系统会要求你等待一分钟或两分钟，以便文件解压缩并存储到电脑上。 

未来的所有启动时间应不到一秒。

然后，需要[为新的 Linux 分发版创建用户帐户和密码](https://docs.microsoft.com/zh-cn/windows/wsl/user-support)。

![image-20201022171700195](/images/2020/10/image-20201022171700195.png)

- 此**用户名**和**密码**特定于安装的每个单独的 Linux 分发版，与 Windows 用户名无关。
- 创建**用户名**和**密码**后，该帐户将是分发版的默认用户，并将在启动时自动登录。
- 此帐户将被视为 Linux 管理员，能够运行 `sudo` (Super User Do) 管理命令。
- 在适用于 Linux 的 Windows 子系统上运行的每个 Linux 分发版都有其自身的 Linux 用户帐户和密码。 每当添加分发版、重新安装或重置时，都必须配置一个 Linux 用户帐户。

### 查看版本信息

Debian查看版本当前操作系统发行版信息：

```bash
$ cat /etc/os-release
PRETTY_NAME="Debian GNU/Linux 10 (buster)"
NAME="Debian GNU/Linux"
VERSION_ID="10"
VERSION="10 (buster)"
VERSION_CODENAME=buster
ID=debian
HOME_URL="https://www.debian.org/"
SUPPORT_URL="https://www.debian.org/support"
BUG_REPORT_URL="https://bugs.debian.org/"
```

Debian查看当前操作系统版本信息

```bash
$ cat /proc/version
Linux version 4.4.0-19041-Microsoft (Microsoft@Microsoft.com) (gcc version 5.4.0 (GCC) ) #1-Microsoft Fri Dec 06 14:06:00 PST 2019
```

Debian查看版本当前操作系统内核信息

```bash
$ uname -r
4.4.0-19041-Microsoft
```

### 卸载 WSL

#### 方法一

在powershell中输入下面的代码

```
wslconfig /l  #显示出你安装的列表。
wslconfig /u debian #debian为上述列表中的名字   注销子系统
```

#### 方法二

打开开始菜单，右键卸载掉。

![image-20201023142313438](/images/2020/10/image-20201023142313438.png)

### 更新和升级包

大多数分发版随附了一个空的的包目录或最简单的包目录。

强烈建议定期更新包目录并使用分发版的首选包管理器升级已安装的包。 

对于 Debian/Ubuntu，请使用 apt，修改 `/etc/apt/sources.list`：

```bash
deb http://mirrors.163.com/debian/ buster main contrib non-free
# deb-src http://mirrors.163.com/debian/ buster main contrib non-free
deb http://mirrors.163.com/debian/ buster-updates main contrib non-free
# deb-src http://mirrors.163.com/debian/ buster-updates main contrib non-free
deb http://mirrors.163.com/debian/ buster-backports main contrib non-free
# deb-src http://mirrors.163.com/debian/ buster-backports main contrib non-free
deb http://mirrors.163.com/debian-security buster/updates main contrib non-free
# deb-src http://mirrors.163.com/debian-security buster/updates main contrib non-free
```

更新

```bash
sudo apt update && sudo apt upgrade
```

### 开启 ssh 连接

1. 卸载 ssh server

   ```bash
   sudo apt-get remove openssh-server
   ```

2. 安装 ssh server

   ```bash
   sudo apt-get install openssh-server
   ```

3. 按需修改 ssh server 配置 

   ```bash
   sudo vim /etc/ssh/sshd_config
   ```

   可能需要修改以下几项：

   ```
   Port 2222  #默认的是22，但是windows有自己的ssh服务，也是监听的22端口，所以这里要改一下
   UsePrivilegeSeparation no
   PasswordAuthentication yes
   AllowUsers youusername # 这里改成你登陆WSL用的
   ```

4. 启动 ssh server

   ```bash
   sudo service ssh --full-restart
   ```

现在就可以用 xshell 等软件登陆 Debian on windows 了，IP 是 127.0.0.1。

但是要注意，cmd 的窗口还不能关掉。关掉后 sshd 服务也会关掉，连接就断开了。

### 问题解决

如果提示下面报错，很可能是进行设置后，没有重启电脑。

![image-20201022170346394](/images/2020/10/image-20201022170346394.png)

### 参考资料

- https://docs.microsoft.com/zh-cn/windows/wsl/install-win10