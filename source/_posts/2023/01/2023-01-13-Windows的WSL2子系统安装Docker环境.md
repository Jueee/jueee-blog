---
title: Windows的WSL2子系统安装Docker环境
layout: info
commentable: true
date: 2023-01-13
mathjax: true
mermaid: true
tags: [OS,Debian]
categories: [OS,Debian]
description: 
---

WSL 子系统安装好 Debian 后，需要配置 Docker 环境，下面介绍安装步骤。

<!--more-->

### 配置更新源

```bash
$ cat <<'EOF' > /etc/apt/sources.list
deb http://mirrors.163.com/debian/ bullseye main non-free contrib
deb-src http://mirrors.163.com/debian/ bullseye main non-free contrib
deb http://mirrors.163.com/debian-security/ bullseye-security main
deb-src http://mirrors.163.com/debian-security/ bullseye-security main
deb http://mirrors.163.com/debian/ bullseye-updates main non-free contrib
deb-src http://mirrors.163.com/debian/ bullseye-updates main non-free contrib
deb http://mirrors.163.com/debian/ bullseye-backports main non-free contrib
deb-src http://mirrors.163.com/debian/ bullseye-backports main non-free contrib
EOF

$ apt-get update
```

### 安装 Docker 环境

下载 docker deb 文件：

https://download.docker.com/linux/debian/dists/bullseye/pool/stable/amd64/

#### 安装

- containerd.io-与OS API进行交互的守护程序（在本例中为LXC-Linux Containers），从本质上将Docker与OS分离，还为非Docker容器管理器提供容器服务
- docker-ce-Docker守护程序，这是完成所有管理工作的部分，**在Linux上需要另外两个**
- docker-ce-cli-用于控制守护程序的CLI工具，如果要控制远程Docker守护程序，则可以单独安装它们

> $ sudo dpkg -i containerd.io_1.6.9-1_amd64.deb
>
> $ sudo dpkg -i docker-ce-cli_20.10.9_3-0_debian-bullseye_amd64.deb
>
> $ sudo dpkg -i docker-ce_20.10.9_3-0_debian-bullseye_amd64.deb

#### 日志

> /var/log# tail -n 100 docker.log

#### 依赖 iptables 包

依赖 iptables 包：

```
sudo apt-get install iptables
sudo apt --fix-broken install
```

#### WSL2 不支持 iptables-nft

```
time="2023-01-13T10:27:21.593809700+08:00" level=info msg="stopping healthcheck following graceful shutdown
failed to start daemon: Error initializing network controller: error obtaining controller instance: unable v1.8.7 (nf_tables):  RULE_APPEND failed (No such file or directory): rule in chain DOCKER-ISOLATION-STAGE-1
 (exit status 4))
```

原因是由于新的 Debian 系统使用了iptables-nft，而WSL2不支持导致的。

可以通过以下命令进行修改

```
$ sudo update-alternatives --config iptables
There are 2 choices for the alternative iptables (providing /usr/sbin/iptables).

  Selection    Path                       Priority   Status
------------------------------------------------------------
* 0            /usr/sbin/iptables-nft      20        auto mode
  1            /usr/sbin/iptables-legacy   10        manual mode
  2            /usr/sbin/iptables-nft      20        manual mode

Press <enter> to keep the current choice[*], or type selection number: 1
update-alternatives: using /usr/sbin/iptables-legacy to provide /usr/sbin/iptables (iptables) in manual mode
```

修改完成后重启Docker服务即可。 `$ sudo service docker start`

### 验证 docker 

```
$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

### 下载镜像

#### 异常处理

```
$ docker pull safe-box:1.0.2
Error response from daemon: Get "https://registry-1.docker.io/v2/": x509: certificate signed by unknown authority
```

可能你机器本身需要更新一下, 不认识RootCA清单，执行这一行：

```
sudo apt-get update && sudo apt-get install ca-certificates
```

然后重启Docker服务即可。 `$ sudo service docker start`