---
title: SpringBoot通过Druid集成MyBatis-Plus框架
layout: info
commentable: true
date: 2020-12-23
mathjax: true
mermaid: true
tags: [Java,JavaJar,MyBatis,Druid]
categories: 
- [Java,JavaJar]
- [Java,SpringBoot]
description: 
---

### MyBatis-Plus 介绍

[MyBatis-Plus](https://github.com/baomidou/mybatis-plus)（简称 MP）是一个 [MyBatis](http://www.mybatis.org/mybatis-3/)的增强工具，在 MyBatis 的基础上只做增强不做改变，为简化开发、提高效率而生。

- 官网：https://baomidou.com/
- GitHub：https://github.com/baomidou/mybatis-plus

#### 依赖引入

```xml
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-boot-starter</artifactId>
    <version>3.4.1</version>
</dependency>
```

<!--more-->

### MyBatis-Plus 特性

- **无侵入**：只做增强不做改变，引入它不会对现有工程产生影响，如丝般顺滑
- **损耗小**：启动即会自动注入基本 CURD，性能基本无损耗，直接面向对象操作
- **强大的 CRUD 操作**：内置通用 Mapper、通用 Service，仅仅通过少量配置即可实现单表大部分 CRUD 操作，更有强大的条件构造器，满足各类使用需求
- **支持 Lambda 形式调用**：通过 Lambda 表达式，方便的编写各类查询条件，无需再担心字段写错
- **支持主键自动生成**：支持多达 4 种主键策略（内含分布式唯一 ID 生成器 - Sequence），可自由配置，完美解决主键问题
- **支持 ActiveRecord 模式**：支持 ActiveRecord 形式调用，实体类只需继承 Model 类即可进行强大的 CRUD 操作
- **支持自定义全局通用操作**：支持全局通用方法注入（ Write once, use anywhere ）
- **内置代码生成器**：采用代码或者 Maven 插件可快速生成 Mapper 、 Model 、 Service 、 Controller 层代码，支持模板引擎，更有超多自定义配置等您来使用
- **内置分页插件**：基于 MyBatis 物理分页，开发者无需关心具体操作，配置好插件之后，写分页等同于普通 List 查询
- **分页插件支持多种数据库**：支持 MySQL、MariaDB、Oracle、DB2、H2、HSQL、SQLite、Postgre、SQLServer 等多种数据库
- **内置性能分析插件**：可输出 Sql 语句以及其执行时间，建议开发测试时启用该功能，能快速揪出慢查询
- **内置全局拦截插件**：提供全表 delete 、 update 操作智能分析阻断，也可自定义拦截规则，预防误操作

### MyBatis-Plus 语法

#### 构造查询

[参考文档](https://baomidou.com/guide/wrapper.html#abstractwrapper)

```java
QueryWrapper<User> wrapper=new QueryWrapper<>();
wrapper.like("author","tom");
List<Book> list = bookService.selectAll(wrapper);
```

### Druid 注解多数据源示例

相关配置如下：

1. 使用注解方式，需要引入 druid 包：

   ```xml
   <dependency>
       <groupId>com.alibaba</groupId>
       <artifactId>druid-spring-boot-starter</artifactId>
       <version>1.2.4</version>
   </dependency>
   ```

2. 配置文件

   ```properties
   spring.datasource.first.driverClassName=com.mysql.cj.jdbc.Driver
   spring.datasource.first.jdbc-url=jdbc:mysql://127.0.0.1:3306/vuedb?serverTimezone=UTC
   spring.datasource.first.username=xxx
   spring.datasource.first.password=xxx
   
   spring.datasource.second.driverClassName=com.mysql.cj.jdbc.Driver
   spring.datasource.second.jdbc-url=jdbc:mysql://127.0.0.1:3306/test?serverTimezone=UTC
   spring.datasource.second.username=xxx
   spring.datasource.second.password=xxx
   
   mybatis.mapper-location=classpath*:mapper/*.xml
   ```

3. 数据源通用方法 AbstractDatasource：

   ```java
   import com.alibaba.druid.pool.DruidDataSource;
   import com.baomidou.mybatisplus.extension.spring.MybatisSqlSessionFactoryBean;
   import org.apache.ibatis.session.SqlSessionFactory;
   import org.springframework.core.io.Resource;
   import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
   import org.springframework.core.io.support.ResourcePatternResolver;
   
   import javax.sql.DataSource;
   
   public abstract class AbstractDbConfig {
   
       protected SqlSessionFactory sqlSessionFactory(DataSource dataSource, String mapperLocation) throws Exception {
           MybatisSqlSessionFactoryBean factoryBean = new MybatisSqlSessionFactoryBean();
           factoryBean.setDataSource(dataSource);
           ResourcePatternResolver resourceResolver = new PathMatchingResourcePatternResolver();
           Resource[] resource= resourceResolver.getResources(mapperLocation);
           factoryBean.setMapperLocations(resource);
           return factoryBean.getObject();
       }
   
       protected DataSource dataSourceFactory(String driveClassName, String url, String userName, String password){
           DruidDataSource datasource = new DruidDataSource();
           datasource.setDriverClassName(driveClassName);
           datasource.setUrl(url);
           datasource.setUsername(userName);
           datasource.setPassword(password);
           datasource.setMaxActive(20);
           datasource.setInitialSize(20);
           return datasource;
       }
   }
   ```

   {% note warning %}

   在这个配置类中，应该使用 `MybatisSqlSessionFactoryBean` 而不是 `SqlSessionFactoryBean`，否则会报错：

   > Invalid bound statement (not found)

   {% endnote %}

4. 对应不同的数据源，进行匹配

   ```java
   import com.jueee.repository.FirstRepository;
   import org.mybatis.spring.SqlSessionTemplate;
   import org.mybatis.spring.annotation.MapperScan;
   import org.springframework.beans.factory.annotation.Qualifier;
   import org.springframework.beans.factory.annotation.Value;
   import org.springframework.context.annotation.Bean;
   import org.springframework.context.annotation.Configuration;
   import org.springframework.jdbc.datasource.DataSourceTransactionManager;
   import org.springframework.transaction.PlatformTransactionManager;
   
   import javax.sql.DataSource;
   
   @Configuration
   @MapperScan(basePackages = {"com.jueee"},annotationClass = FirstRepository.class,
           sqlSessionTemplateRef = "firstUserTemplate")
   public class DataSourceConfigFirst extends AbstractDbConfig {
   
       @Value("${spring.datasource.first.jdbc-url}")
       private String url;
   
       @Value("${spring.datasource.first.username}")
       private String userName;
   
       @Value("${spring.datasource.first.password}")
       private String password;
   
       @Value("${spring.datasource.first.driver-class-name}")
       private String driveClassName;
   
       @Value(value = "${mybatis.mapper-location}")
       private String mapperLocation;
   
   
       @Bean(name = "firstUser")
       public DataSource secondaryDataSource() {
           return dataSourceFactory(driveClassName, url, userName, password);
       }
   
       @Bean(name = "firstUserTemplate")
       public SqlSessionTemplate firstUserSqlTemplate() throws Exception {
           return new SqlSessionTemplate((sqlSessionFactory(secondaryDataSource(), mapperLocation)));
       }
   
       @Bean
       @Qualifier("firstUserTransaction")
       public PlatformTransactionManager firstUserTransaction() {
           return new DataSourceTransactionManager(secondaryDataSource());
       }
   }
   ```

   第二数据源配置如下：

   ```java
   import com.jueee.repository.SecondRepository;
   import org.mybatis.spring.SqlSessionTemplate;
   import org.mybatis.spring.annotation.MapperScan;
   import org.springframework.beans.factory.annotation.Qualifier;
   import org.springframework.beans.factory.annotation.Value;
   import org.springframework.context.annotation.Bean;
   import org.springframework.context.annotation.Configuration;
   import org.springframework.jdbc.datasource.DataSourceTransactionManager;
   import org.springframework.transaction.PlatformTransactionManager;
   
   import javax.sql.DataSource;
   
   @Configuration
   @MapperScan(basePackages = {"com.jueee"},annotationClass = SecondRepository.class,
           sqlSessionTemplateRef = "secondUserTemplate")
   public class DataSourceConfigSecond extends AbstractDbConfig {
   
       @Value("${spring.datasource.second.jdbc-url}")
       private String url;
   
       @Value("${spring.datasource.second.username}")
       private String userName;
   
       @Value("${spring.datasource.second.password}")
       private String password;
   
       @Value("${spring.datasource.second.driver-class-name}")
       private String driveClassName;
   
       @Value(value = "${mybatis.mapper-location}")
       private String mapperLocation;
   
   
       @Bean(name = "secondUser")
       public DataSource secondaryDataSource() {
           return dataSourceFactory(driveClassName, url, userName, password);
       }
   
       @Bean(name = "secondUserTemplate")
       public SqlSessionTemplate secondUserSqlTemplate() throws Exception {
           return new SqlSessionTemplate((sqlSessionFactory(secondaryDataSource(), mapperLocation)));
       }
   
       @Bean
       @Qualifier("secondUserTransaction")
       public PlatformTransactionManager secondUserTransaction() {
           return new DataSourceTransactionManager(secondaryDataSource());
       }
   }
   ```

5. 定义注解，分别作为不同数据库的表识。

   ```java
   import org.apache.ibatis.annotations.Mapper;
   import org.springframework.stereotype.Component;
   
   import java.lang.annotation.*;
   
   @Documented
   @Retention(RetentionPolicy.RUNTIME)
   @Target(ElementType.TYPE)
   @Component
   @Mapper
   public @interface FirstRepository {
       String value() default "";
   }
   ```

   ```java
   import org.apache.ibatis.annotations.Mapper;
   import org.springframework.stereotype.Component;
   
   import java.lang.annotation.*;
   
   @Documented
   @Retention(RetentionPolicy.RUNTIME)
   @Target(ElementType.TYPE)
   @Component
   @Mapper
   public @interface SecondRepository {
       String value() default "";
   }
   ```

6. Bean：

   `com.jueee.bean.User` 类：

   ```java
   import com.baomidou.mybatisplus.annotation.TableName;
   import lombok.Data;
   
   @Data
   @TableName("user")
   public class User {
       private Long id;
   
       private String username;
   
       private String nickname;
   }
   ```

   `com.jueee.bean.Book`类：

   ```java
   import com.baomidou.mybatisplus.annotation.TableName;
   import lombok.Data;
   
   @Data
   @TableName("book")
   public class Book {
       private Long id;
   
       private String author;
   
       private String description;
   
       private String title;
   }
   ```

7. Mapper `com.jueee`类：

   ```java
   import com.baomidou.mybatisplus.core.mapper.BaseMapper;
   import com.jueee.bean.User;
   import com.jueee.repository.FirstRepository;
   
   @FirstRepository
   public interface UserMapper extends BaseMapper<User> {
   }
   ```

   ```java
   import com.baomidou.mybatisplus.core.mapper.BaseMapper;
   import com.jueee.bean.Book;
   import com.jueee.repository.SecondRepository;
   
   @SecondRepository
   public interface BookMapper extends BaseMapper<Book> {
   }
   ```

8. Service 类如下：

   ```java
   import com.jueee.bean.User;
   import com.jueee.mapper.UserMapper;
   import org.springframework.beans.factory.annotation.Autowired;
   import org.springframework.stereotype.Service;
   
   @Service
   public class UserService {
       @Autowired
       private UserMapper userMapper;
   
       public User selectById(int id){
           return userMapper.selectById(id);
       }
   }
   ```

   ```java
   import com.jueee.bean.Book;
   import com.jueee.mapper.BookMapper;
   import org.springframework.beans.factory.annotation.Autowired;
   import org.springframework.stereotype.Service;
   
   import java.util.List;
   
   @Service
   public class BookService {
       @Autowired
       private BookMapper bookMapper;
   
       public List<Book> selectAll(){
           return bookMapper.selectList(null);
       }
   }
   ```

9. 测试类如下：

   ```java
   import com.jueee.bean.Book;
   import com.jueee.bean.User;
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
       @Autowired
       private BookService bookService;
   
       @Test
       public void selectById(){
           User user = userService.selectById(1);
           log.info(user.getNickname());
       }
       @Test
       public void selectAll(){
           List<Book> list = bookService.selectAll();
           list.forEach(t->log.info(t.getAuthor()+" - "+t.getTitle()));
       }
   }
   ```

   