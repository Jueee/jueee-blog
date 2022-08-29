---
title: 自动删除 ElasticSearch 索引
layout: info
commentable: true
date: 2020-09-07
mathjax: true
mermaid: true
tags: [ElasticSearch,Shell]
categories: 
- [Database,ElasticSearch]
- [OS,Shell]
description: 
---

索引文件保留在服务器中，大大减小服务器的性能，占用硬盘空间，
因此使用脚本自动删除 elk 中的历史索引以释放空间。

### 清理索引命令行

查看所有的索引文件：

> curl -XGET http://localhost:9200/_cat/indices?v

删除索引文件以释放空间：

> curl -XDELETE http://localhost:9200/filebeat-2016.12.28

<!--more-->

### 清理索引脚本

新增 Shell 脚本：

```powershell
#!/bin/bash
# auto delete 7 day ago elasticsearch index

eshost='127.0.0.1:9200'

dtime=`date -d "7 day ago" +%Y-%m-%d`
dtime_stamp=`date -d "$dtime" +%s`

echo `date` 'start clean ' $dtime >> clean-log.log

indexs=`curl -s 'http://'$eshost'/_cat/indices' | awk '$3~/^logstash/{print $3}'`

for line in $indexs;do
  index=$line
  itime=`echo $line | awk -F - '{print $3}' | tr '.' '-'`
  itime_stamp=`date -d "$itime" +%s`

  if [ $itime_stamp -lt $dtime_stamp ];then
    echo $index >> clean-log.log
    curl -X DELETE "http://$eshost/$index" > /dev/null 2>&1
  fi
done
```

其中：

- `echo $line | awk -F - '{print $3}'`  中的 `-` 表示索引中的日期分隔符，根据需要，可以换成 `awk -F _ '{print $3}'` 等
- `'{print $3}'` 中的 `3` 表示日期所处的位置，可以根据需要更改。

### 配置自动任务

每天2点定时删除es中指定日期的数据，配置 crontab：

```powershell
0 2 * * * sh /home/dir/auto-clean-log.sh >> /home/dir/clean-log.log 2>&1
```

### 容器中获取 es 地址

对于 docker 搭建的 es 环境，可以通过如下参数获取 es 的 IP：

```
esip=`docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" elasticsearch.manti-infra.svc`
eshost="$esip:9200"
```

对于 k8s 搭建的 es 环境，可以通过如下参数获取 es 的 IP：

```powershell
esip=`kubectl describe svc elasticsearch  -n manti-infra | grep IP | awk '{print $2}'`
eshost="$esip:9200"
```

