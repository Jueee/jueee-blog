---
title: ClickHouse数据库日常操作使用汇总
layout: info
commentable: true
date: 2023-10-13
mathjax: true
mermaid: true
tags: [Database,ClickHouse]
categories: [Database,ClickHouse]
description: 
---

### ClickHouse 系统操作

#### 查看系统进程

```sql
 select * from system.processes; 
```

#### kill 系统进程

```sql
KILL QUERY WHERE query_id = '';
```

