---
title: Java使用neo4j-java-driver操作Neo4j
layout: info
commentable: true
date: 2021-02-09
mathjax: true
mermaid: true
tags: [Java,Database,Neo4j]
categories: 
- [Database,Neo4j]
- [Java,JavaJar]
description: 
---

### 引入依赖

```xml
<!-- https://mvnrepository.com/artifact/org.neo4j.driver/neo4j-java-driver -->
<dependency>
   <groupId>org.neo4j.driver</groupId>
   <artifactId>neo4j-java-driver</artifactId>
   <version>4.2.0</version>
</dependency>
```

<!--more-->

### 项目代码

本文完整项目代码位于：https://github.com/Jueee/blog-project/tree/main/neo4j-driver-session

### 使用步骤

每个Neo4j驱动程序都有一个用于创建驱动程序的数据库对象。

一般按照以下操作步骤：

1. 向数据库对象请求一个新的驱动程序；
2. 向驱动程序对象请求一个新会话；
3. 请求会话对象创建事务；
4. 使用事务对象运行语句。它返回一个表示结果的对象；
5. 处理结果；
6. 关闭会话。

示例：

```java
Driver driver = GraphDatabase.driver("bolt://127.0.0.1:7687", AuthTokens.basic("neo4j", "password"));
Session session = driver.session();
final Result result = session.run("MATCH (a:Person) RETURN a.name AS name");
while (result.hasNext()) {
    Record record = result.next();
    System.out.println(record.get("name").asString());
}
session.close();
driver.close();
```

### 生成 Driver Session

#### Java 引入

```java
Driver driver = GraphDatabase.driver("bolt://127.0.0.1:7687", AuthTokens.basic("neo4j", "password"));
SessionConfig sessionConfig = SessionConfig.defaultConfig();
Session session = driver.session(sessionConfig);
```

#### SpringBoot 引入

##### 配置文件

```properties
neo4j.uri=bolt://127.0.0.1:7687
neo4j.username=neo4j
neo4j.password=password
```

##### 配置类

```java
import org.neo4j.driver.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class Neo4jConfig {

    @Value("${neo4j.uri}")
    private String neo4jUri;

    @Value("${neo4j.username}")
    private String neo4jUsername;

    @Value("${neo4j.password}")
    private String neo4jPassword;

    @Bean
    public Session getSession(){
        Driver driver = GraphDatabase.driver(neo4jUri, AuthTokens.basic(neo4jUsername, neo4jPassword));
        SessionConfig sessionConfig = SessionConfig.defaultConfig();
        return driver.session(sessionConfig);
    }
}
```

##### 引入 Session

```java
@Autowired
private Session session;
```

### 执行SQL

```java
public List<Path> randomPerson(){
    String searchSQL = "match p=(n:Person)-[t]->(m) where 1=1 return p limit 20";
    log.info("[searchSQL]"+searchSQL);
    long start = System.currentTimeMillis();
    List<Path> pathList = new ArrayList<>();
    Result result = session.run(searchSQL);
    while ( result.hasNext() ) {
        Record record = result.next();
        Value value = record.get(0);
        pathList.add(value.asPath());
    }
    log.info("[UseTime]"+(System.currentTimeMillis()-start)+"ms"+"[Size]"+pathList.size());
    return pathList;
}
```

### 执行统计

#### 汇总节点数量

```java
public Long getNodeCount() {
    Long resultNum = 0L;
    try {
        String searchSQL = "match (n:Person) return count(n)";
        Result result = session.run(searchSQL);
        while ( result.hasNext() ) {
            Record record = result.next();
            Value value = record.get(0);
            resultNum = value.asLong();
        }
    } catch (Exception e) {
        log.error(e.getMessage(),e);
    }
    return resultNum;
}
```

#### 汇总关系数量

```java
public Long getRelationshipCount() {
    Long resultNum = 0L;
    try {
        String searchSQL = "match p=(n:Person)-[]->(m:Person) return count(n)";
        Result result = session.run(searchSQL);
        while ( result.hasNext() ) {
            Record record = result.next();
            Value value = record.get(0);
            resultNum = value.asLong();
        }
    } catch (Exception e) {
        log.error(e.getMessage(),e);
    }
    return resultNum;
}
```