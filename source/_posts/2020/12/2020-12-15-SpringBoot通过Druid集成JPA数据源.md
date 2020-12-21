---
title: SpringBoot通过Druid集成JPA数据源
layout: info
commentable: true
date: 2020-12-15
mathjax: true
mermaid: true
tags: [Java,JavaJar,Alibaba,Druid,JPA]
categories: 
- [Java,JavaJar]
- [Java,SpringBoot]
description: 
---

### JPA 介绍

JPA顾名思义就是Java Persistence API的意思，是JDK 5.0注解或XML描述对象－关系表的映射关系，并将运行期的实体对象持久化到数据库中。

JPA 具有如下优势：

1. **标准化**

   JPA 是 JCP 组织发布的 Java EE 标准之一，因此任何声称符合 JPA 标准的框架都遵循同样的架构，提供相同的访问API，这保证了基于JPA开发的企业应用能够经过少量的修改就能够在不同的JPA框架下运行。

2. **容器级特性的支持**

   JPA框架中支持大数据集、事务、并发等容器级事务，这使得 JPA 超越了简单持久化框架的局限，在企业应用发挥更大的作用。

3. **简单方便**

   JPA的主要目标之一就是提供更加简单的编程模型：在JPA框架下创建实体和创建Java 类一样简单，没有任何的约束和限制，只需要使用 javax.persistence.Entity进行注释，JPA的框架和接口也都非常简单，没有太多特别的规则和设计模式的要求，开发者可以很容易的掌握。JPA基于非侵入式原则设计，因此可以很容易的和其它框架或者容器集成。

4. **查询能力**

   JPA的查询语言是面向对象而非面向数据库的，它以面向对象的自然语法构造查询语句，可以看成是Hibernate HQL的等价物。JPA定义了独特的JPQL（Java Persistence Query Language），JPQL是EJB QL的一种扩展，它是针对实体的一种查询语言，操作对象是实体，而不是关系数据库的表，而且能够支持批量更新和修改、JOIN、GROUP BY、HAVING 等通常只有 SQL 才能够提供的高级查询特性，甚至还能够支持子查询。

5. **高级特性**

   JPA 中能够支持面向对象的高级特性，如类之间的继承、多态和类之间的复杂关系，这样的支持能够让开发者最大限度的使用面向对象的模型设计企业应用，而不需要自行处理这些特性在关系数据库的持久化。

<!--more-->

### maven 配置

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>com.alibaba</groupId>
        <artifactId>druid-spring-boot-starter</artifactId>
        <version>1.2.4</version>
    </dependency>
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <optional>true</optional>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

### 配置单数据源

1. 配置文件

   ```properties
   spring.datasource.driverClassName=com.mysql.cj.jdbc.Driver
   spring.datasource.url=jdbc:mysql://localhost:3306/test?serverTimezone=UTC
   spring.datasource.username=xxx
   spring.datasource.password=xxx
   ```

2. Bean

   ```java
   import lombok.Data;
   
   import javax.persistence.Entity;
   import javax.persistence.GeneratedValue;
   import javax.persistence.GenerationType;
   import javax.persistence.Id;
   import java.util.Date;
   
   @Entity
   @Data
   public class User {
       @Id
       @GeneratedValue(strategy = GenerationType.IDENTITY)
       private Long id;
   
       private String username;
   
       private String nickname;
   }
   ```

3. Mapper

   ```java
   import com.jueee.druid.bean.User;
   import org.springframework.data.jpa.repository.JpaRepository;
   import org.springframework.data.jpa.repository.Query;
   import org.springframework.data.repository.query.Param;
   
   public interface UserMapper extends JpaRepository<User,Integer> {
       @Query(value = "SELECT t FROM User t WHERE username = :username")
       User findUserByName(@Param("username") String username);
   }
   ```

4. Service

   ```java
   import com.jueee.druid.bean.User;
   import com.jueee.druid.mapper.UserMapper;
   import org.springframework.beans.factory.annotation.Autowired;
   import org.springframework.stereotype.Service;
   
   import java.util.List;
   
   @Service
   public class UserService {
       @Autowired
       private UserMapper userMapper;
   
       public User findUserByName(String name) {
           return userMapper.findUserByName(name);
       }
   
       public List<User> findAll() {
           return userMapper.findAll();
       }
   }
   ```

5. 测试类

   ```java
   import com.jueee.druid.bean.User;
   import lombok.extern.slf4j.Slf4j;
   import org.junit.jupiter.api.Test;
   import org.springframework.beans.factory.annotation.Autowired;
   import org.springframework.boot.test.context.SpringBootTest;
   
   import java.util.List;
   
   @Slf4j
   @SpringBootTest
   public class UserServiceTest {
   
       @Autowired
       private UserService userService;
   
       @Test
       public void findUserByName(){
           User user = userService.findUserByName("admin");
           log.info(user.getUsername()+"-"+user.getNickname()); // admin-小章鱼
       }
   
       @Test
       public void findAll(){
           List<User> list = userService.findAll();
           list.forEach(t -> log.info(t.getUsername()));	// admin
       }
   }
   ```

### 配置多数据源

**注意点**：

- @Primary注解的使用
- 目录结构中，JPA目录和实体类目录建议根据多数据源的配置进行分层，因为在多数据源配置中存在相关配置

相关配置如下：

1. 配置文件

   ```properties
   spring.datasource.first.driverClassName=com.mysql.cj.jdbc.Driver
   spring.datasource.first.url=jdbc:mysql://127.0.0.1:3306/vuedb?serverTimezone=UTC
   spring.datasource.first.username=xxx
   spring.datasource.first.password=xxx
   
   spring.datasource.second.driverClassName=com.mysql.cj.jdbc.Driver
   spring.datasource.second.url=jdbc:mysql://127.0.0.1:3306/test?serverTimezone=UTC
   spring.datasource.second.username=xxx
   spring.datasource.second.password=xxx
   ```

2. 多数据源配置：

   ```java
   import com.alibaba.druid.spring.boot.autoconfigure.DruidDataSourceBuilder;
   import org.springframework.boot.context.properties.ConfigurationProperties;
   import org.springframework.context.annotation.Bean;
   import org.springframework.context.annotation.Configuration;
   import org.springframework.context.annotation.Primary;
   
   import javax.sql.DataSource;
   
   @Configuration
   public class DruidDataSourceConfig {
   
       @Primary
       @ConfigurationProperties(prefix = "spring.datasource.first")
       @Bean(name = "firstDataSource")
       public DataSource firstDataSource() {
           return DruidDataSourceBuilder.create().build();
       }
   
       @ConfigurationProperties(prefix = "spring.datasource.second")
       @Bean(name = "secondDataSource")
       public DataSource secondDataSource() {
           return DruidDataSourceBuilder.create().build();
       }
   }
   ```

   {% note warning %}

   多数据源配置时，一定要区分主数据源和其他数据源。所以在主数据源初始化时一定要加上注解@Peimary，其余数据源初始化不可以使用这个注解，否则报错。

   {% endnote %}

3. 对应不同的数据源，需要匹配不同的JPA

   主数据源primary JPA配置如下：

   ```java
   import org.springframework.beans.factory.annotation.Autowired;
   import org.springframework.beans.factory.annotation.Qualifier;
   import org.springframework.boot.autoconfigure.orm.jpa.HibernateProperties;
   import org.springframework.boot.autoconfigure.orm.jpa.HibernateSettings;
   import org.springframework.boot.autoconfigure.orm.jpa.JpaProperties;
   import org.springframework.boot.orm.jpa.EntityManagerFactoryBuilder;
   import org.springframework.context.annotation.Bean;
   import org.springframework.context.annotation.Configuration;
   import org.springframework.context.annotation.Primary;
   import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
   import org.springframework.orm.jpa.JpaTransactionManager;
   import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
   import org.springframework.transaction.PlatformTransactionManager;
   import org.springframework.transaction.annotation.EnableTransactionManagement;
   
   import javax.persistence.EntityManager;
   import javax.sql.DataSource;
   import java.util.Map;
   
   @Configuration
   @EnableTransactionManagement
   @EnableJpaRepositories(
           entityManagerFactoryRef = "entityManagerFactoryFirst",
           transactionManagerRef = "transactionManagerFirst",
           basePackages = {"com.jueee.druid.mapper.first"}) //设置Repository所在位置
   public class JpaConfigFirst {
       @Autowired
       private JpaProperties jpaProperties;
       @Autowired
       private HibernateProperties hibernateProperties;
   
       @Autowired
       @Qualifier("firstDataSource")
       private DataSource firstDataSource;
   
   
   
       @Primary
       @Bean(name = "entityManagerFirst")
       public EntityManager entityManager(EntityManagerFactoryBuilder builder) {
           return entityManagerFactoryFirst(builder).getObject().createEntityManager();
       }
   
       @Primary
       @Bean(name = "entityManagerFactoryFirst")
       public LocalContainerEntityManagerFactoryBean entityManagerFactoryFirst(EntityManagerFactoryBuilder builder) {
           return builder
                   .dataSource(firstDataSource)// 设置数据源
                   .properties(jpaProperties.getProperties())// 设置jpa配置
                   .properties(getVendorProperties())// 设置hibernate配置
                   .packages("com.jueee.druid.bean.first") //设置实体类所在位置
                   .persistenceUnit("firstPersistenceUnit")// 设置持久化单元名，用于@PersistenceContext注解获取EntityManager时指定数据源
                   .build();
       }
   
       private Map getVendorProperties() {
           return hibernateProperties.determineHibernateProperties(jpaProperties.getProperties(), new HibernateSettings());
       }
   
       @Primary
       @Bean(name = "transactionManagerFirst")
       public PlatformTransactionManager transactionManagerFirst(EntityManagerFactoryBuilder builder) {
           return new JpaTransactionManager(entityManagerFactoryFirst(builder).getObject());
       }
   }
   ```

   {% note warning %}

   主数据源JPA配置中，相对应的注入bean一定要加上注解@Primary，否则报错！

   {% endnote %}

   第二数据源JPA配置如下：

   ```java
   import org.springframework.beans.factory.annotation.Autowired;
   import org.springframework.beans.factory.annotation.Qualifier;
   import org.springframework.boot.autoconfigure.orm.jpa.HibernateProperties;
   import org.springframework.boot.autoconfigure.orm.jpa.HibernateSettings;
   import org.springframework.boot.autoconfigure.orm.jpa.JpaProperties;
   import org.springframework.boot.orm.jpa.EntityManagerFactoryBuilder;
   import org.springframework.context.annotation.Bean;
   import org.springframework.context.annotation.Configuration;
   import org.springframework.context.annotation.Primary;
   import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
   import org.springframework.orm.jpa.JpaTransactionManager;
   import org.springframework.orm.jpa.LocalContainerEntityManagerFactoryBean;
   import org.springframework.transaction.PlatformTransactionManager;
   import org.springframework.transaction.annotation.EnableTransactionManagement;
   
   import javax.persistence.EntityManager;
   import javax.sql.DataSource;
   import java.util.Map;
   
   @Configuration
   @EnableTransactionManagement
   @EnableJpaRepositories(
           entityManagerFactoryRef = "entityManagerFactorySecond",
           transactionManagerRef = "transactionManagerSecond",
           basePackages = {"com.jueee.druid.mapper.second"}) //设置Repository所在位置
   public class JpaConfigSecond {
       @Autowired
       private JpaProperties jpaProperties;
       @Autowired
       private HibernateProperties hibernateProperties;
   
       @Autowired
       @Qualifier("secondDataSource")
       private DataSource secondDataSource;
   
   
   
       @Primary
       @Bean(name = "entityManagerSecond")
       public EntityManager entityManager(EntityManagerFactoryBuilder builder) {
           return entityManagerFactorySecond(builder).getObject().createEntityManager();
       }
   
       @Primary
       @Bean(name = "entityManagerFactorySecond")
       public LocalContainerEntityManagerFactoryBean entityManagerFactorySecond(EntityManagerFactoryBuilder builder) {
           return builder
                   .dataSource(secondDataSource)// 设置数据源
                   .properties(jpaProperties.getProperties())// 设置jpa配置
                   .properties(getVendorProperties())// 设置hibernate配置
                   .packages("com.jueee.druid.bean.second") //设置实体类所在位置
                   .persistenceUnit("secondPersistenceUnit")// 设置持久化单元名，用于@PersistenceContext注解获取EntityManager时指定数据源
                   .build();
       }
   
       private Map getVendorProperties() {
           return hibernateProperties.determineHibernateProperties(jpaProperties.getProperties(), new HibernateSettings());
       }
   
       @Primary
       @Bean(name = "transactionManagerSecond")
       public PlatformTransactionManager transactionManagerSecond(EntityManagerFactoryBuilder builder) {
           return new JpaTransactionManager(entityManagerFactorySecond(builder).getObject());
       }
   }
   ```

4. Bean

   `com.jueee.druid.bean.first.User` 类：

   ```java
   import lombok.Data;
   
   import javax.persistence.Entity;
   import javax.persistence.GeneratedValue;
   import javax.persistence.GenerationType;
   import javax.persistence.Id;
   import java.util.Date;
   
   @Entity
   @Data
   public class User {
       @Id
       @GeneratedValue(strategy = GenerationType.IDENTITY)
       private Long id;
   
       private String username;
   
       private String nickname;
   }
   ```

   `com.jueee.druid.bean.second.Book`类：

   ```java
   import lombok.Data;
   
   import javax.persistence.Entity;
   import javax.persistence.GeneratedValue;
   import javax.persistence.GenerationType;
   import javax.persistence.Id;
   
   @Entity
   @Data
   public class Book {
       @Id
       @GeneratedValue(strategy = GenerationType.IDENTITY)
       private Long id;
   
       private String author;
   
       private String description;
   
       private String title;
   }
   ```

5. Mapper

   `com.jueee.druid.mapper.first`类：

   ```java
   import com.jueee.druid.bean.first.User;
   import org.springframework.data.jpa.repository.JpaRepository;
   import org.springframework.data.jpa.repository.Query;
   import org.springframework.data.repository.query.Param;
   
   public interface UserMapper extends JpaRepository<User,Integer> {
       @Query(value = "SELECT t FROM User t WHERE username = :username")
       User findUserByName(@Param("username") String username);
   }
   ```

   `com.jueee.druid.mapper.second`类：

   ```java
   import com.jueee.druid.bean.second.Book;
   import org.springframework.data.jpa.repository.JpaRepository;
   import org.springframework.data.jpa.repository.Query;
   import org.springframework.data.repository.query.Param;
   
   public interface BookMapper extends JpaRepository<Book,Integer> {
       @Query(value = "SELECT t FROM Book t WHERE title = :title")
       Book findUserByTitle(@Param("title") String title);
   }
   ```

6. Service 和 Test 与单数据源一致，不再赘述。

