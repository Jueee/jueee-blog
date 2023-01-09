---
title: curl命令行查询ElasticSearch数据
layout: info
commentable: true
date: 2022-12-13
mathjax: true
mermaid: true
tags: [Database,ElasticSearch,curl]
categories: 
- [Database,ElasticSearch]
- [OS,Shell]
description: 
---

ES的查询有query、URL两种方式，而URL是比较简洁的一种，本文主要以实例探讨和总结URL的查询方式。

<!--more-->

### 查询语法

```bash
curl [ -s][ -g][ -X<REST Verb>][ -H 'Content-Type: application/json'] '<Node>:<Port>/<Index>[/Type][/ID]/_search?pretty&q=<search string>'
　　注意要用''包起来，否则后面的&会被识别为“后台执行”，即&后面的内容被忽略
　　-s 不输出查询的时间那些东西
　　-g 做转义用　　
　　<REST Verb>：REST风格的语法谓词，GET/POST/PUT
　　<Node>:节点ip，默认使用localhost
　　<port>:节点端口号，默认80，ES默认使用9200
　　<Index>:索引名，支持通配符，power_json*
　　<Type>:索引类型，由于一个index只有一个type，可不输入
　　<ID>:操作对象的ID号，可不输入
　　q  ：前面加&，后跟查询语句
```

#### 常用参数

```
q---查询字符串
sort---排序执行。可以是fieldName或 fieldName:asc/ 的形式fieldName:desc。fieldName可以是文档中的实际字段，也可以是特殊_score名称，表示基于分数的排序。可以有几个sort参数（顺序很重要）。
from---从命中的索引开始返回。默认为0。
size---要返回的点击次数。默认为10。
_source_include---查询包含某些source字段的文档。
_source_exclude---查询不包含某些source字段的文档。
timeout---搜索超时，将搜索请求限制在指定的时间值内执行，并使用在到期时累积的点击数进行保释。默认为无超时。
default_field---默认为index.query.default_field，即未指定字段前缀时返回所有字段，索引设置为*
default_operator---默认查询运算符，未指定时默认为OR。
analyzer---用于分析查询字符串的分析器名称。
_source---设置为false禁用_source字段检索。
analyze_wildcard---是否应分析通配符和前缀查询,默认为false
status:active---where the status field contains active
　　　　　　　 ---（status相当于fieldname,active相当于值----->TESTID：39232032303039,由于=被用在了前面“q=”,所以这里用“：”代替了“=”）
title:(quick OR brown)---where the title field contains quick or brown. If you omit the OR operator the default operator will be used
author:"John Smith"---where the author field contains the exact phrase "john smith"
_exists_:title---where the field title has any non-null value
date:[2012-01-01 TO 2012-12-31]---All days in 2012
count:[10 TO *]---Numbers from 10 upwards
count:>=10---Numbers from 10 upwards
```

### 查看具体数据

查询某个索引下某条记录的具体数据：

```bash
curl 'localhost:9200/index_name/mail/aaa'
curl 'localhost:9200/index_name/_doc/aaa'（默认 type 为 _doc）
```

### 根据条件查询

```bash
curl 'localhost:9200/index_name/_search?pretty&q=msgid:aaa'	//查指定的字段值
curl 'localhost:9200/index_name/_search?pretty&q=msgid:aaa&size=3' //查指定的字段值，并只显示3个
curl 'localhost:9200/index_name/_search?pretty&q=msgid:aaa&from=2&size=3' //从第3个开始只显示3个，即3/4/5
curl 'localhost:9200/index_name/_search?pretty&q=msgid:aaa&sort=TIME:desc' //按时间排序，desc降序，默认为升序
curl 'localhost:9200/index_name/_search?pretty&analyze_wildcard&q=msgid:aaa'　　 //模糊查询
curl 'localhost:9200/index_name/_search?pretty&q=VAL:<200'　　//比较大小
curl 'localhost:9200/index_name/_search?pretty&_source=false'　　//是否显示
curl 'localhost:9200/index_name/_search?pretty&_source_includes=TIME,VAL'　　//设置包含的字段
curl -g 'localhost:9200/index_name/_search?pretty&q=(SOLAR:1%20AND%20CENTRAL:1)'　　//组合查询，要加 -g
curl -g 'localhost:9200/index_name/_search?pretty&q=TIME:[2019-05%20TO%202019-06]'　//范围查询，要加 -g
```

### 查询多个index数据

```bash
curl 'http://127.0.0.1:9200/index_name1,index_name2,index_name3/_search?pretty&q=msgid:1e50baf1dea339f871f9272508bc7615'
```

### JSON参数复杂查询

```bash
curl 'http://127.0.0.1:9200/index_name/_search' {"query":{"bool":{"must":[{"match":{"uid":"aaa"}},{"match":{"msgid":"bbb"}}]}}}
```

