---
title: MySQL中DBlink的使用
layout: info
commentable: true
date: 2020-08-11
mathjax: true
mermaid: true
tags: [MySQL]
categories: [Database,MySQL]
description: 在实际工作中，我们可能会遇到需要操作其他数据库实例的部分表，但又不想系统连接多库。此时我们就需要用到数据表映射。如同Oracle中的DBlink一般，使用过Oracle DBlink数据库链接的人都知道可以跨实例来进行数据查询，同样的，Mysql自带的FEDERATED引擎完美的帮我们解决了该问题。
---

在实际工作中，我们可能会遇到需要操作其他数据库实例的部分表，但又不想系统连接多库。此时我们就需要用到数据表映射。

如同Oracle中的DBlink一般，使用过Oracle DBlink数据库链接的人都知道可以跨实例来进行数据查询，同样的，Mysql自带的 FEDERATED 引擎完美的帮我们解决了该问题。

### 检查引擎

查看target端是否安装了FEDERATED存储引擎：

```mysql
mysql> show engines ;
```

例如：

![1597126521400](/images/2020/08/1597126521400.png)

### 安装引擎

注意：如果没有安装**FEDERATED 引擎**，执行：

```mysql
install plugin federated soname 'ha_federated.so';
```

例如：

![1597126538702](/images/2020/08/1597126538702.png)

再次检查引擎：

```mysql
mysql> show engines ;
```

例如：

![1597126564647](/images/2020/08/1597126564647.png)

### 开启引擎

将 federated 添加到 my.cnf 重启数据库

```cnf
vi /etc/my.cnf
[mysqld]
federated
```

再次检查引擎，例如：

![1597126649766](/images/2020/08/1597126649766.png)

### 建表访问

使用CONNECTION创建FEDERATED引擎表通用模型：

```mysql
CREATE TABLE (......) 
ENGINE =FEDERATED CONNECTION='mysql://username:password@hostname:port/database/tablename'
```

注意 ENGINE=FEDERATED CONNECTION 后为源端地址 避免使用带@的密码

### 使用总结

基于MySQL5.7.23版本，笔者在源端及目标端实验了多种DDL及DML，现简单总结如下，有兴趣的同学可以试试看。

- 目标端建表结构可以与源端不一样 推荐与源端结构一致
- 源端DDL(CREATE、ALTER、DROP等语句)语句更改表结构 目标端不会变化
- 源端DML（SELECT、UPDATE、INSERT、DELETEt等语句）语句目标端查询会同步
- 源端drop表 目标端结构还在但无法查询
- 目标端不能执行DDL语句
- 目标端执行DML语句 源端数据也会变化
- 目标端truncate表 源端表数据也会被清空
- 目标端drop表对源端无影响

### 最佳实践

目前FEDERATED引擎使用范围还不多，若确实有跨实例访问的需求，建议做好规范，个人总结最佳实践如下：

1. 源端专门创建只读权限的用户来供目标端使用。
2. 目标端建议用CREATE SERVER方式创建FEDERATED表。
3. FEDERATED表不宜太多，迁移时要特别注意。
4. 目标端应该只做查询使用，禁止在目标端更改FEDERATED表。
5. 建议目标端表名及结构和源端保持一致。
6. 源端表结构变更后 目标端要及时删除重建。