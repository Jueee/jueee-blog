---
title: Neo4j之Cypher相关SQL汇总
layout: info
commentable: true
date: 2020-10-24
mathjax: true
mermaid: true
tags: [Neo4j]
categories: Neo4j
description: 
---

### Cypher 语句

Cypher是图形数据库Neo4j的声明式查询语言。

Cypher语句规则和具备的能力：

- Cypher通过模式匹配图数据库中的节点和关系，来提取信息或者修改数据。
- Cypher语句中允许使用变量，用来表示命名、绑定元素和参数。
- Cypher语句可以对节点、关系、标签和属性进行创建、更新和删除操作。
- Cypher语句可以管理索引和约束。

<!--more-->

### Cypher 汇总

节点总数

```cypher
match (n) return count(n);
```

关系总数

```cypher
match p=(n)-[t]->(m) return count(n);
```

### Cypher 查询

#### 随机查询

```cypher
match p=(n:MAIL)-[t]->(m) return p limit 20
```

#### 条件查询

根据开始节点，筛选来往关系：

```cypher
MATCH p=(n:Mail{mail:'test@163.com'})-[send:Send*1..1]->(m:Mail) RETURN p;

MATCH p=(n:Mail)-[send:Send*1..1]->(m:Mail) where n.mail='test@126.com' RETURN p;
```

#### 来往次数查询

根据来往次数，筛选来往关系：

```cypher
MATCH (a:MAIL)-[r:SEND]->(b:MAIL) WITH a, b, TAIL (COLLECT (r)) as rr WHERE size(rr)>3 RETURN a,b,rr;
```

#### 多层级查询

根据条件，关联 3 级：

```cypher
MATCH p=(a: MAIL{mail:'test@163.com'})-[rels*1..3]-(b) return p limit 100
```

#### 来往关系

```cypher
MATCH (p1:MAIL{mail:'test1@163.com'}),(p2:MAIL{mail:'test2@163.com'}),
      p=shortestpath((p1)-[rels*..10]-(p2))  
where all(t IN rels where t.date>='2020-10-17 00:00:00' and t.date <='2020-10-17 23:59:59') return p 
```

#### 过滤路径

普通过滤：

```cypher
match p=(n:MAIL)-[t]->(m) 
where t.date>='2020-10-23 00:00:00' and t.date <='2020-10-23 23:59:59'
return p limit 20
```

根据条件，关联 3 级并过滤路径：

```cypher
MATCH p=(a: MAIL{mail:'test@163.com'})-[rels*1..3]-(b) 
where all(t IN rels where t.date>='2020-10-23' and t.date <='2020-10-24') 
return p limit 100
```

{% note warning %}

**需采用 where all(t IN rels where ...) 的方式，否则会报错：** 

`Type mismatch: expected Any, Map, Node, Relationship, Point, Duration, Date, Time, LocalTime, LocalDateTime or DateTime but was List<Relationship>`

{% endnote %}

### Cypher 删除

#### 删除所有

删除所有节点或关系的标签或属性：

```cypher
MATCH (a)-[rel]-(b) DELETE a,b,rel;
MATCH (a: Mail_test)-[rel]-(b:Mail_test) DELETE a,b,rel;
```

删除所有节点：

```cypher
MATCH (e) DELETE e;
MATCH (e: Mail_test) DELETE e;
```

### 参考资料

- https://www.jianshu.com/p/2bb98c81d8ee

