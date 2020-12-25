---
title: SpringBoot通过Druid多数据源集成MyBatis-Plus
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

需要引入 maven 包：

```xml
<dependency>
    <groupId>com.baomidou</groupId>
    <artifactId>mybatis-plus-boot-starter</artifactId>
    <version>3.4.1</version>
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
```

<!--more-->

### Druid 注解多数据源

#### 配置文件

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

#### 数据源配置

1. 数据源通用方法 AbstractDatasource：

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

2. 对应不同的数据源，进行匹配

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

#### 定义注解   

定义注解，分别作为不同数据库的表识。

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

#### Bean

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

#### Mapper

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

#### Service

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

#### 测试类

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

#### 

