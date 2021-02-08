---
title: Springboot集成Neo4j示例
layout: info
commentable: true
date: 2021-02-08
mathjax: true
mermaid: true
tags: [Java,Springboot,Database,Neo4j]
categories: 
- [Database,Neo4j]
- [Java,Springboot]
description: 
---

### 引入依赖

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-neo4j</artifactId>
</dependency>
```

<!--more-->

### 项目代码

本文完整项目代码位于：https://github.com/Jueee/blog-project/tree/main/neo4j-springboot

### 配置连接

```properties
spring.data.neo4j.uri=bolt://127.0.0.1:7687
spring.data.neo4j.username=neo4j
spring.data.neo4j.password=123456
```

### 建立NodeEntity

类似于MySQL中的 table 映射的对象类，mysql中叫做ORM，neo4j中叫做OGM [object graph mapping]

#### 节点的标签实体

```java
import lombok.Data;
import lombok.NoArgsConstructor;
import org.neo4j.ogm.annotation.GeneratedValue;
import org.neo4j.ogm.annotation.Id;
import org.neo4j.ogm.annotation.NodeEntity;
import org.neo4j.ogm.annotation.Property;

@NodeEntity(label = "Person")
@Data
@NoArgsConstructor
public class Person {

    @Id
    @GeneratedValue
    Long id;

    @Property(name = "name")
    private String name;
}
```

#### 关系实体

```java
import lombok.Data;
import lombok.NoArgsConstructor;
import org.neo4j.ogm.annotation.*;

@RelationshipEntity(type = "LOVES")
@Data
@NoArgsConstructor
public class Love {
    @Id
    @GeneratedValue
    private Long id;

    @StartNode
    private Person startNode;

    @EndNode
    private Person endNode;
}
```

### 接口 API

#### 编写Repository

##### 节点Repository

```java
import com.jueee.bean.Person;
import org.springframework.data.neo4j.repository.Neo4jRepository;

public interface PersonRepository extends Neo4jRepository<Person, Long> {

}
```

##### 关系Repository

```java
import com.jueee.bean.Love;
import org.springframework.data.neo4j.repository.Neo4jRepository;

public interface LoveRepository extends Neo4jRepository<Love,Long> {

}
```

#### 编写Service

```java
import com.jueee.bean.Love;
import com.jueee.bean.Person;
import com.jueee.dao.LoveRepository;
import com.jueee.dao.PersonRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class PersonService{

    @Autowired
    private PersonRepository personRepository;

    @Autowired
    private LoveRepository loveRepository;

    public Person addPerson(Person person){
        return personRepository.save(person);
    }

    public Person findOnePerson(long id) {
        return personRepository.findById(id).get();
    }

    public Love loves(Love love) {
        return loveRepository.save(love);
    }
}
```

#### 测试程序

```java
import com.jueee.bean.Love;
import com.jueee.bean.Person;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@Slf4j
@SpringBootTest
class PersonServiceTest {

    @Autowired
    PersonService personService;

    @Test
    public void test1(){
        Person test1 = new Person();
        test1.setName("test1");
        Person result1 = personService.addPerson(test1);
        log.info(result1.toString());

        Person test2 = new Person();
        test2.setName("test2");
        Person result2 = personService.addPerson(test2);
        log.info(result2.toString());

        Person person1 = personService.findOnePerson(result1.getId());
        Person person2 = personService.findOnePerson(result2.getId());
        Love love = new Love();
        love.setStartNode(person1);
        love.setEndNode(person2);
        Love result =  personService.loves(love);
        log.info(result.toString());
    }
}
```

#### 运行效果

日志：

```
Person(id=1263319, name=test1)
Person(id=1263329, name=test2)
Love(id=1650877, startNode=Person(id=1263319, name=test1), endNode=Person(id=1263329, name=test2))
```

查看关系：

![image-20210208135415452](/images/2021/02/image-20210208135415452.png)

### 自定义 cypherSQL

#### 查询对象

##### 编写Service

```java
import com.jueee.bean.Love;
import lombok.extern.slf4j.Slf4j;
import org.neo4j.ogm.session.Session;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
@Service
public class SessionService {

    @Autowired
    private Session session;

    public List<Love> test(){
        String searchSQL = "match p=(n:Person)-[t]->(m) where 1=1 return p limit 20";
        log.info("[searchSQL]"+searchSQL);
        long start = System.currentTimeMillis();
        List<Love> loveList = new ArrayList<>();
        Map<String, String> parameters = new HashMap<>();
        Iterable<Love> loves = session.query(Love.class, searchSQL, parameters);
        if (loves != null) {
            for (Love love : loves) {
                loveList.add(love);
            }
        }
        log.info("[UseTime]"+(System.currentTimeMillis()-start)+"ms"+"[Size]"+loveList.size());
        return loveList;
    }
}
```

##### 测试程序

```java
import com.jueee.bean.Love;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.neo4j.driver.types.Path;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

@Slf4j
@SpringBootTest
class SessionServiceTest {

    @Autowired
    SessionService sessionService;

    @Test
    public void test(){
        List<Love> pathList = sessionService.test();
        pathList.forEach(t->log.info(t.toString()));
    }
}
```

##### 运行结果

```
[searchSQL]match p=(n:Person)-[t]->(m) where 1=1 return p limit 20
[UseTime]1535ms[Size]2
Love(id=1650877, startNode=Person(id=1263319, name=test1), endNode=Person(id=1263329, name=test2))
Love(id=1651113, startNode=Person(id=1263485, name=test1), endNode=Person(id=1263486, name=test2))
```

#### 自定义统计 SQL

查询节点总数：

```java
public Long getNodeCount() {
    Long resultNum = 0L;
    try {
        StringBuffer cypher = new StringBuffer();
        Map<String, String> parameters = new HashMap<>();
        cypher.append("match (n:Person) return count(n)");
        Iterator<Map<String, Object>> mailSends = session.query(cypher.toString(), parameters).iterator();
        if (mailSends.hasNext()) {
            Map<String, Object> result = mailSends.next();
            resultNum = (Long)result.get("count(n)");
        }
    } catch (Exception e) {
        log.error(e.getMessage(),e);
    }
    return resultNum;
}
```

查询关系总数：

```java
public Long getRelationshipCount() {
    Long resultNum = 0L;
    try {
        StringBuffer cypher = new StringBuffer();
        Map<String, String> parameters = new HashMap<>();
        cypher.append("match p=(n:Person)-[]->(m:Person) return count(n)");
        log.info(cypher.toString());
        Iterator<Map<String, Object>> mailSends = session.query(cypher.toString(), parameters).iterator();
        if (mailSends.hasNext()) {
            Map<String, Object> result = mailSends.next();
            resultNum = (Long)result.get("count(n)");
        }
    } catch (Exception e) {
        log.error(e.getMessage(),e);
    }
    return resultNum;
}
```