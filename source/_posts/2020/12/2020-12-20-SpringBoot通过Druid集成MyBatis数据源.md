---
title: SpringBoot通过Druid集成MyBatis数据源
layout: info
commentable: true
date: 2020-12-20
mathjax: true
mermaid: true
tags: [Java,JavaJar,MyBatis,Druid]
categories: 
- [Java,JavaJar]
- [Java,SpringBoot]
description: 
---

### MyBatis 介绍

MyBatis 是一款优秀的持久层框架，它支持自定义 SQL、存储过程以及高级映射。MyBatis 免除了几乎所有的 JDBC 代码以及设置参数和获取结果集的工作。MyBatis 可以通过简单的 XML 或注解来配置和映射原始类型、接口和 Java POJO（Plain Old Java Objects，普通老式 Java 对象）为数据库中的记录。

<!--more-->

### maven 配置

```xml
<dependencies>
    <dependency>
        <groupId>org.mybatis.spring.boot</groupId>
        <artifactId>mybatis-spring-boot-starter</artifactId>
        <version>2.1.4</version>
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
   
   mybatis.mapper-locations=classpath:mapper/*Mapper.xml
   mybatis.type-aliases-package=com.jueee.bean
   ```

2. Bean

   ```java
   import lombok.Data;
   
   @Data
   public class User {
       private Long id;
   
       private String username;
   
       private String nickname;
   }
   ```
   
3. Mapper

   ```java
   import com.jueee.bean.User;
   import org.springframework.stereotype.Repository;
   
   @Repository
   public interface UserMapper {
       User selectById(int id);
   }
   ```
   
4. Mapper

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
   <mapper namespace="com.jueee.mapper.UserMapper">
   
       <select id="selectById" resultType="com.jueee.bean.User">
           select * from user where id = #{id}
       </select>
   
   </mapper>
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
           return userMapper.selectById(id);
       }
   }
   ```

6. 测试类

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
           log.info(user.getNickname()); // 小章鱼
       }
   }
   ```

#### 项目结构

![image-20201218153328612](/images/2020/12/image-20201218153328612.png)

### 配置多数据源

**注意点**：

- @Primary注解的使用
- 目录结构中，实体类目录建议根据多数据源的配置进行分层，因为在多数据源配置中存在相关配置

相关配置如下：

1. 配置文件

   ```properties
   spring.datasource.first.driverClassName=com.mysql.cj.jdbc.Driver
   spring.datasource.first.jdbc-url=jdbc:mysql://127.0.0.1:3306/vuedb?serverTimezone=UTC
   spring.datasource.first.username=xxx
   spring.datasource.first.password=xxx
   
   spring.datasource.second.driverClassName=com.mysql.cj.jdbc.Driver
   spring.datasource.second.jdbc-url=jdbc:mysql://127.0.0.1:3306/test?serverTimezone=UTC
   spring.datasource.second.username=xxx
   spring.datasource.second.password=xxx
   ```

   {% note warning %}

   与单数据源配置 `spring.datasource.second.url` 不同，多数据源时需配置`spring.datasource.second.jdbc-url`，否则会报错：

   ```
   jdbcUrl is required with driverClassName
   ```

   spring.datasource.url 数据库的 JDBC URL。

   spring.datasource.jdbc-url 用来重写自定义连接池

   [官方文档](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#howto-configure-a-datasource) 的解释是：

   因为连接池的实际类型没有被公开，所以在您的自定义数据源的元数据中没有生成密钥，而且在IDE中没有完成(因为DataSource接口没有暴露属性)。

   {% endnote %}

2. 对应不同的数据源，，进行匹配

   主数据源primary 配置如下：

   ```java
   import org.apache.ibatis.session.SqlSessionFactory;
   import org.mybatis.spring.SqlSessionFactoryBean;
   import org.mybatis.spring.SqlSessionTemplate;
   import org.mybatis.spring.annotation.MapperScan;
   import org.springframework.beans.factory.annotation.Qualifier;
   import org.springframework.boot.context.properties.ConfigurationProperties;
   import org.springframework.boot.jdbc.DataSourceBuilder;
   import org.springframework.context.annotation.Bean;
   import org.springframework.context.annotation.Configuration;
   import org.springframework.context.annotation.Primary;
   import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
   
   import javax.sql.DataSource;
   
   @Configuration
   @MapperScan(basePackages = "com.jueee.mapper.first", sqlSessionFactoryRef = "firstSqlSessionFactory")
   public class DataSourceConfigFirst {
   
       @Primary // 表示这个数据源是默认数据源
       @Bean(name = "firstDataSource")
       @ConfigurationProperties(prefix = "spring.datasource.first") // 读取application.properties中的配置参数映射成为一个对象
       public DataSource getDateSource1() {
           return DataSourceBuilder.create().build();
       }
   
       @Primary // 表示这个数据源是默认数据源
       @Bean(name = "firstSqlSessionFactory")
       public SqlSessionFactory firstSqlSessionFactory(@Qualifier("firstDataSource") DataSource datasource) // @Qualifier表示查找Spring容器中名字为firstDataSource的对象
               throws Exception {
           SqlSessionFactoryBean bean = new SqlSessionFactoryBean();
           bean.setDataSource(datasource);
           bean.setMapperLocations(new PathMatchingResourcePatternResolver().getResources("classpath*:mapper/first/*.xml")); // // 设置mybatis的xml所在位置
           return bean.getObject();
       }
   
       @Primary // 表示这个数据源是默认数据源
       @Bean("firstSqlSessionTemplate")
       public SqlSessionTemplate firstSqlSessionTemplate(
               @Qualifier("firstSqlSessionFactory") SqlSessionFactory sessionFactory) {
           return new SqlSessionTemplate(sessionFactory);
       }
   }
   ```

   {% note warning %}

   主数据源配置中，相对应的注入bean一定要加上注解@Primary，否则报错！

   {% endnote %}

   第二数据源配置如下：

   ```java
   import org.apache.ibatis.session.SqlSessionFactory;
   import org.mybatis.spring.SqlSessionFactoryBean;
   import org.mybatis.spring.SqlSessionTemplate;
   import org.mybatis.spring.annotation.MapperScan;
   import org.springframework.beans.factory.annotation.Qualifier;
   import org.springframework.boot.context.properties.ConfigurationProperties;
   import org.springframework.boot.jdbc.DataSourceBuilder;
   import org.springframework.context.annotation.Bean;
   import org.springframework.context.annotation.Configuration;
   import org.springframework.context.annotation.Primary;
   import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
   
   import javax.sql.DataSource;
   
   @Configuration
   @MapperScan(basePackages = "com.jueee.mapper.second", sqlSessionFactoryRef = "secondSqlSessionFactory")
   public class DataSourceConfigSecond {
   
       // 将这个对象放入Spring容器中
       @Bean(name = "secondDataSource")
       @ConfigurationProperties(prefix = "spring.datasource.second") // 读取application.properties中的配置参数映射成为一个对象
       public DataSource getDateSource1() {
           return DataSourceBuilder.create().build();
       }
   
       @Bean(name = "secondSqlSessionFactory")
       public SqlSessionFactory secondSqlSessionFactory(@Qualifier("secondDataSource") DataSource datasource) // @Qualifier表示查找Spring容器中名字为secondDataSource的对象
               throws Exception {
           SqlSessionFactoryBean bean = new SqlSessionFactoryBean();
           bean.setDataSource(datasource);
           bean.setMapperLocations(new PathMatchingResourcePatternResolver().getResources("classpath*:mapper/second/*.xml")); // // 设置mybatis的xml所在位置
           return bean.getObject();
       }
   
       @Bean("secondSqlSessionTemplate")
       public SqlSessionTemplate secondSqlSessionTemplate(
               @Qualifier("secondSqlSessionFactory") SqlSessionFactory sessionFactory) {
           return new SqlSessionTemplate(sessionFactory);
       }
   
   }
   ```

3. Bean

   `com.jueee.bean.first.User` 类：

   ```java
   import lombok.Data;
   
   @Data
   public class User {
       private Long id;
   
       private String username;
   
       private String nickname;
   }
   ```

   `com.jueee.bean.second.Book`类：

   ```java
   import lombok.Data;
   
   @Data
   public class Book {
       private Long id;
   
       private String author;
   
       private String description;
   
       private String title;
   }
   ```

4. Mapper

   `com.jueee.first`类：

   ```java
   import com.jueee.bean.first.User;
   import org.springframework.stereotype.Repository;
   
   @Repository
   public interface UserMapper {
       User selectById(int id);
   }
   ```

   `com.jueee.mapper.second`类：

   ```java
   import com.jueee.bean.second.Book;
   import org.springframework.stereotype.Repository;
   
   import java.util.List;
   
   @Repository
   public interface BookMapper {
       List<Book> selectAll();
   }
   ```

5. Mapper 对应的 xml 文件。

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
   <mapper namespace="com.jueee.mapper.first.UserMapper">
   
       <select id="selectById" resultType="com.jueee.bean.first.User">
           select * from user where id = #{id}
       </select>
   
   </mapper>
   ```

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
   <mapper namespace="com.jueee.mapper.second.BookMapper">
   
       <resultMap id="BaseResultMap" type="com.jueee.bean.second.Book">
           <result column="id" jdbcType="INTEGER" property="id" />
           <result column="author" jdbcType="VARCHAR" property="author" />
           <result column="description" jdbcType="VARCHAR" property="description" />
           <result column="title" jdbcType="VARCHAR" property="title" />
       </resultMap>
   
       <select id="selectAll" resultMap="BaseResultMap">
           select * from book
       </select>
   
   </mapper>
   ```

6. Service 和 Test 与单数据源一致，不再赘述。

#### 项目结构

![image-20201218160646087](/images/2020/12/image-20201218160646087.png)

### 注解匹配多数据源

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
   import lombok.Data;
   
   @Data
   public class User {
       private Long id;
   
       private String username;
   
       private String nickname;
   }
   ```

   `com.jueee.bean.Book`类：

   ```java
   import lombok.Data;
   
   @Data
   public class Book {
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
   
   @FirstRepository
   public interface UserMapper {
       User selectById(int id);
   }
   ```

   ```java
   import com.jueee.bean.Book;
   import com.jueee.repository.SecondRepository;
   
   import java.util.List;
   
   @SecondRepository
   public interface BookMapper {
       List<Book> selectAll();
   }
   ```

8. Service 和 Test 与单数据源一致，不再赘述。

#### 项目结构

![image-20201218164353447](/images/2020/12/image-20201218164353447.png)