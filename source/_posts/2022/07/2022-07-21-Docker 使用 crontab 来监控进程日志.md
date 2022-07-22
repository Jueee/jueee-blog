---
title: Docker 使用 crontab 来监控进程日志
layout: info
commentable: true
date: 2022-07-21
mathjax: true
mermaid: true
tags: [Docker,Supervisor]
categories: [Container,Docker]
description: 

---

对于 Docker 容器中的应用，我们希望通过监控日志的方式来检查运行状态。

如果日志一段时间不滚动，则进行应用的重启。

本文将使用进程管理工具 supervisor 来管理容器中的多个进程。使用Supervisor可以更好的控制、管理、重启我们希望运行的进程。

<!--more-->

### supervisor配置

 新增 supervisord.conf 文件，如下所示：

```conf
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

`/etc/init.d/cron start` 用于启动crontab服务，但这样启动的crontab服务中配置的定时命令是没有Dockerfile中设置的环境变量的。

因此还需要在这之前执行`env >> /etc/default/locale`，这样有Dockerfile中通过`ENV`设置的环境变量在crontab中就可以正常读取了。

### 报警文件配置

新增 alarm_log.sh 文件，如下所示：

```shell
#!/bin/bash

time=`tail -n 1000 ./approot/logs/app.log|grep 202|tail -n 1|cut -c 1-19`
timestamp=`date +%s -d"${time}"`
nowstamp=`date +%s`
alarmstamp=$[${nowstamp}-10*60]
echo `date` ${time} ${timestamp} ${nowstamp} ${alarmstamp}
if [[ "$alarmstamp" -gt "$timestamp" ]];then
echo "`date` restart "
cd /java-app-dir && bash appCtrl.sh restart
fi
```

### sources.list 文件

```livescript
deb http://repo.hz.netease.com/netease-stretch stretch main contrib non-free
deb-src http://repo.hz.netease.com/netease-stretch stretch main contrib non-free

deb http://debian.service.163.org/debian-current stretch-backports main contrib non-free
deb-src http://debian.service.163.org/debian-current stretch-backports main contrib non-free


deb http://debian.service.163.org/debian-current stretch main contrib non-free
deb-src http://debian.service.163.org/debian-current stretch main contrib non-free


deb http://debian.service.163.org/debian-security stretch/updates main contrib non-free
deb-src http://debian.service.163.org/debian-security stretch/updates main contrib non-free

## http://hwraid.le-vert.net/wiki/DebianPackages
deb http://repo.hz.netease.com/hwraid/stretch stretch main
```

### Dockerfile 配置

```dockerfile
FROM private-registry.yidun.internal/localmanti/yd-java-app:v1

MAINTAINER jueee

ENV XMX_CONFIG="4000"\
    XMS_CONFIG="4000"\
    MAX_PERM="256"\
    RUN_CMD="com.xxx.xxx.xxx.xxx"

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN env >> /etc/default/locale

COPY sources.list /etc/apt/

RUN apt-get update \
  && apt-get install -y --no-install-recommends cron supervisor\
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean \
  && echo "*/1 * * * * root  cd /java-app-dir && /bin/bash alarm_log.sh >> /java-app-dir/alarm_log.log" >> /etc/crontab

COPY alarm_log.sh /java-app-dir
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]
```

其中：

- `env >> /etc/default/locale` 是为了保存环境变量，从而方便 crontab 调用。
- 执行apt安装时注意加入`-y --no-install-recommends`，并且在安装完成后执行`rm -rf /var/lib/apt/lists/* && apt-get clean`命令，可以有效减小镜像的体积。

### 特殊处理

如果镜像重启的过程中，无法获取环境变量，导致重启失败，也需要通过 export 将环境变量取出来，然后请求的时候再带上。

如：

```
$ export
declare -x APPNAME_CONFIG="xxx-xxx"
declare -x FEATURE_MATCH_LIMIT="-1"
declare -x HOME="/root"
```

保存进 tmp_env 文件中。

重启请求时：

```
source /java-app-dir/tmp_env && cd /java-app-dir && bash appCtrl.sh restart
```
