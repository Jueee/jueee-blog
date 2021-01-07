---
title: Docker 使用 Supervisor 来管理进程
layout: info
commentable: true
date: 2020-11-23
mathjax: true
mermaid: true
tags: [Docker,Supervisor]
categories: [Container,Docker]
description: 
---

**Docker** 容器在启动的时候开启单个进程。但我们经常需要在一个机器上开启多个服务，这可以有很多方法，最简单的就是把多个启动命令放到一个启动脚本里面，启动的时候直接启动这个脚本，另外就是安装进程管理工具。

本小节将使用进程管理工具 supervisor 来管理容器中的多个进程。使用Supervisor可以更好的控制、管理、重启我们希望运行的进程。

<!--more-->

### 配置方法

#### Dockerfile 配置

执行apt安装时注意加入`-y --no-install-recommends`，并且在安装完成后执行`rm -rf /var/lib/apt/lists/* && apt-get clean`命令，可以有效减小镜像的体积。

```dockerfile
COPY sources.list /etc/apt/
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    cron supervisor && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

COPY run-cron /etc/cron.d/run-cron
RUN chmod 0644 /etc/cron.d/run-cron
RUN crontab /etc/cron.d/run-cron

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]
```

其中，run-cron 文件内容如下：

```
PATH="/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
* * * * * echo `date` >> /tmp/crontab-date
* * * * * /java-app-dir/healthCheck.sh

```

这样安装完cron服务后，crontab服务并不会自启动，还需要 `/etc/init.d/cron start` 的启动命令。

```
# 保存环境变量，开启crontab服务
env >> /etc/default/locale
/etc/init.d/cron start
```

`/etc/init.d/cron start`用于启动crontab服务，但这样启动的crontab服务中配置的定时命令是没有Dockerfile中设置的环境变量的。

因此还需要在这之前执行`env >> /etc/default/locale`，这样有Dockerfile中通过`ENV`设置的环境变量在crontab中就可以正常读取了。

#### supervisor配置

supervisor配置文件内容

```ini
[supervisord]
nodaemon=true
[program:cron]
command=/etc/init.d/cron start
[program:javaapp]
command=/bin/bash -c "/java-app-dir/appCtrl.sh start && tail -f /dev/null"
```

配置文件包含目录和进程：

- 第一段 supervsord 配置软件本身，使用 nodaemon 参数来运行。
- 第二段包含要控制的 2 个服务。每一段包含一个服务的目录和启动这个服务的命令。

### 使用方法

创建镜像。

```shell
$ sudo docker build -t test/supervisord .
```

启动 supervisor 容器。

```shell
$ sudo docker run -t -i test/supervisords
2020-11-23 13:48:53,271 INFO Included extra file "/etc/supervisor/conf.d/supervisord.conf" during parsing
2020-11-23 13:48:53,282 INFO RPC interface 'supervisor' initialized
2020-11-23 13:48:53,282 CRIT Server 'unix_http_server' running without any HTTP authentication checking
2020-11-23 13:48:53,282 INFO supervisord started with pid 1
2020-11-23 13:48:54,284 INFO spawned: 'cron' with pid 8
2020-11-23 13:48:54,286 INFO spawned: 'javaapp' with pid 9
```

