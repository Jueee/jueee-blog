---
title: SpringBoot通过Druid集成Tkmybatis
layout: info
commentable: true
date: 2020-12-24
mathjax: true
mermaid: true
tags: [Java,JavaJar,MyBatis,Druid,Tkmybatis]
categories: 
- [Java,JavaJar]
- [Java,SpringBoot]
description: 
---

### Tkmybatis 介绍

Tk mybatis 可以极大的方便开发人员。可以随意的按照自己的需要选择通用方法，还可以很方便的开发自己的通用方法。

极其方便的使用MyBatis单表的增删改查。

支持单表操作，不支持通用的多表联合查询。

- GitHub：https://github.com/abel533/Mapper
- JavaDoc：https://apidoc.gitee.com/free/Mapper/

<!--more-->

#### 引入依赖

```xml
<dependency>
    <groupId>tk.mybatis</groupId>
    <artifactId>mapper-spring-boot-starter</artifactId>
    <version>2.1.5</version>
</dependency>
```

### 常见使用

#### 忽略属性

在需要忽略的属性上增加@transient注解

javax.persistence.Transient;

transient是类型修饰符，只能用来修饰字段。在对象序列化过程中， 被 @Transient 标记的变量不会被序列化

```java
@Transient
private String res_typeInfo;
```

### Tkmybatis 单数据源

2. 配置文件：

   ```properties
   spring.datasource.driverClassName=com.mysql.cj.jdbc.Driver
   spring.datasource.url=jdbc:mysql://127.0.0.1:3306/vuedb?serverTimezone=UTC
   spring.datasource.username=xxx
   spring.datasource.password=xxx
   ```

3. Bean

   ```java
   import lombok.Data;
   
   import javax.persistence.GeneratedValue;
   import javax.persistence.Id;
   import javax.persistence.Table;
   
   @Data
   @Table(name = "user")
   public class User {
       @Id
       @GeneratedValue(generator = "JDBC")
       private Long id;
   
       private String username;
   
       private String nickname;
   
       private String email;
   
       private String phoneNumber;
   
       private Integer status;
   
   }
   ```

4. Mapper

   ```java
   import com.jueee.bean.User;
   import org.apache.ibatis.annotations.Select;
   import tk.mybatis.mapper.common.Mapper;
   
   public interface UserMapper extends Mapper<User> {
       @Select("select * from user where username=#{username}")
       User selectByUserName(String username);
   }
   ```

5. Service

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
           return userMapper.selectByPrimaryKey(id);
       }
   
       public User selectByUserName(String username){
           User user = new User();
           user.setUsername(username);
           return userMapper.selectByUserName(username);
       }
   }
   ```

6. Application

   ```java
   import org.springframework.boot.SpringApplication;
   import org.springframework.boot.autoconfigure.SpringBootApplication;
   import tk.mybatis.spring.annotation.MapperScan;
   
   @MapperScan("com.jueee.mapper") //扫描的mapper
   @SpringBootApplication
   public class MysqlMybatisApplication {
   
   	public static void main(String[] args) {
   		SpringApplication.run(MysqlMybatisApplication.class, args);
   	}
   
   }
   ```

7. Test

   ```java
   import com.jueee.bean.User;
   import lombok.extern.slf4j.Slf4j;
   import org.junit.jupiter.api.Test;
   import org.springframework.beans.factory.annotation.Autowired;
   import org.springframework.boot.test.context.SpringBootTest;
   
   @Slf4j
   @SpringBootTest
   public class UserServiceTest {
   
       @Autowired
       private UserService userService;
   
       @Test
       public void selectById(){
           User user = userService.selectById(1);
           log.info(user.getNickname());
       }
       @Test
       public void selectByUserName(){
           User user = userService.selectByUserName("admin");
           log.info(user.getEmail()+"-"+user.getNickname());
       }
   }
   ```

#### 目录结构

![image-20201222174948100](/images/2020/12/image-20201222174948100.png)

### Tkmybatis 多数据源

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
   import org.apache.ibatis.session.SqlSessionFactory;
   import org.mybatis.spring.SqlSessionFactoryBean;
   import org.springframework.core.io.Resource;
   import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
   import org.springframework.core.io.support.ResourcePatternResolver;
   
   import javax.sql.DataSource;
   
   public abstract class AbstractDbConfig {
   
       protected SqlSessionFactory sqlSessionFactory(DataSource dataSource, String mapperLocation) throws Exception {
           SqlSessionFactoryBean factoryBean = new SqlSessionFactoryBean();
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

4. 对应不同的数据源，进行匹配。注：需引入 `tk.mybatis.spring.annotation.MapperScan`

   第一数据源配置如下：

   ```java
   import com.jueee.repository.FirstRepository;
   import org.mybatis.spring.SqlSessionTemplate;
   import org.springframework.beans.factory.annotation.Qualifier;
   import org.springframework.beans.factory.annotation.Value;
   import org.springframework.context.annotation.Bean;
   import org.springframework.context.annotation.Configuration;
   import org.springframework.context.annotation.Primary;
   import org.springframework.jdbc.datasource.DataSourceTransactionManager;
   import org.springframework.transaction.PlatformTransactionManager;
   import tk.mybatis.spring.annotation.MapperScan;
   
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
   
       @Primary
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
   import org.springframework.beans.factory.annotation.Qualifier;
   import org.springframework.beans.factory.annotation.Value;
   import org.springframework.context.annotation.Bean;
   import org.springframework.context.annotation.Configuration;
   import org.springframework.jdbc.datasource.DataSourceTransactionManager;
   import org.springframework.transaction.PlatformTransactionManager;
   import tk.mybatis.spring.annotation.MapperScan;
   
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
   import lombok.Data;
   
   import javax.persistence.GeneratedValue;
   import javax.persistence.Id;
   import javax.persistence.Table;
   
   @Data
   @Table(name="user")
   public class User {
       @Id
       @GeneratedValue(generator = "JDBC")
       private Long id;
   
       private String username;
   
       private String nickname;
   
       private String email;
   
       private String phoneNumber;
   
       private Integer status;
   
   }
   ```

   `com.jueee.bean.Book`类：

   ```java
   import lombok.Data;
   
   import javax.persistence.GeneratedValue;
   import javax.persistence.Id;
   import javax.persistence.Table;
   
   @Data
   @Table(name="book")
   public class Book {
       @Id
       @GeneratedValue(generator = "JDBC")
       private Long id;
   
       private String author;
   
       private String description;
   
       private String title;
   }
   ```

7. Mapper `com.jueee`类：

   ```java
   import com.jueee.bean.User;
   import com.jueee.repository.FirstRepository;
   import tk.mybatis.mapper.common.Mapper;
   
   import java.io.Serializable;
   
   @FirstRepository
   public interface UserMapper extends Mapper<User> {
       User selectByUserName(Serializable id);
   }
   ```

   ```java
   import com.jueee.bean.Book;
   import com.jueee.repository.SecondRepository;
   import tk.mybatis.mapper.common.Mapper;
   
   @SecondRepository
   public interface BookMapper extends Mapper<Book> {
   }
   ```

8. Service 类如下：

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
           return bookMapper.selectAll();
       }
   
   }
   ```

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
           return userMapper.selectByPrimaryKey(id);
       }
   
       public User selectByUserName(String username){
           return userMapper.selectByUserName(username);
       }
   }
   ```

9. 自定义 `selectByUserName` 方法对应的 Mapping.xml ：

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
   <mapper namespace="com.jueee.mapper.UserMapper">
   
       <select id="selectByUserName" resultType="com.jueee.bean.User">
           select * from user where username = #{username}
       </select>
   
   </mapper>
   ```

10. 测试类如下：

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
       public void selectUserById(){
           User user = userService.selectById(1);
           log.info(user.getNickname());
       }
       @Test
       public void selectByUserName(){
           User user = userService.selectByUserName("admin");
           log.info(user.getEmail()+"-"+user.getNickname());
       }
   
       @Test
       public void selectAllBook(){
           List<Book> list = bookService.selectAll();
           list.forEach(t->log.info(t.getAuthor()));
       }
   }
   ```

#### 目录结构

![image-20201222192502651](/images/2020/12/image-20201222192502651.png)

### 问题解决

报错：

![image-20201222143508821](/images/2020/12/image-20201222143508821.png)

解决办法，不是导入 `org.mybatis.spring.annotation.MapperScan`，应该导入 `tk.mybatis.spring.annotation.MapperScan` 包。

![image-20201222143643372](/images/2020/12/image-20201222143643372.png)