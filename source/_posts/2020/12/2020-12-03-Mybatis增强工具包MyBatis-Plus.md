---
title: Mybatis增强工具包MyBatis-Plus
layout: info
commentable: true
date: 2020-12-03
mathjax: true
mermaid: true
tags: [Java,JavaJar,MyBatis]
categories: 
- [Java,JavaJar]
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

### MyBatis-Plus 基本操作

#### 忽略字段

- @TableField(exist = false)：表示该属性不为数据库表字段，但又是必须使用的。
- @TableField(exist = true)：表示该属性为数据库表字段。

```java
    @TableField(exist = false)
    private int total;
```

#### 查询操作

##### 批量查询

```java
List<User> users = userMapper.selectBatchIds(Arrays.asList(1, 2, 3));
users.forEach(System.out::println);
```

##### 自定义Map查询

```java
HashMap<String, Object> map = new HashMap<>();
map.put("name","Sandy");
map.put("age",21);
List<User> users = userMapper.selectByMap(map);
```

##### 条件构造器

[参考文档](https://baomidou.com/guide/wrapper.html#abstractwrapper)

```java
QueryWrapper<User> wrapper=new QueryWrapper<>();
wrapper.like("author","tom");
List<Book> list = bookService.selectAll(wrapper);
```

##### 主键查询

确定主键：

```java
    @TableId(type = IdType.INPUT)
    private  String	 userid;
```

主键查询：

```java
	userMapper.selectById(userid);
```

##### 分页查询

注册插件

```java
@MapperScan("com.jueee.mapper")
@EnableTransactionManagement
@Configuration // 配置类
public class MyBatisPlusConfig {
    
    @Bean // 分页插件
	public PaginationInterceptor paginationInterceptor() {
  		return  new PaginationInterceptor();
	}
}
```

如果自定义了MybatisSqlSessionFactoryBean 需要手动加入插件，否则分页不生效：

```java
MybatisSqlSessionFactoryBean factoryBean = new MybatisSqlSessionFactoryBean();
factoryBean.setPlugins(paginationInterceptor());
```

测试分页查询：

```java
Page<User> page = new Page<>(2,5); // 参数：当前页、页面大小
userMapper.selectPage(page,null);
page.getRecords().forEach(System.out::println); // 查询对象
System.out.println(page.getTotal()); // 总数
```

#### 新增操作

```java
User user = new User();
user.setName("mybatis-plus_insertTest");
user.setAge(15);
user.setEmail("test@foxmail.com");

int result = userMapper.insert(user); // 帮我们自动生成id
System.out.println(result); // 受影响的行数，打印 1
System.out.println(user); // User(id=1341988615581687810, name=mybatis-plus_insertTest, age=15, email=test@foxmail.com)
```

**主键自增策略：**

1.  实体类字段上 @TableId(type = IdType.AUTO)
2. 数据库id字段设置为自增！

其中， `com.baomidou.mybatisplus.annotation.IdType` 的类型选择如下：

```java
public enum IdType {
  AUTO(0), // 数据库id自增
  NONE(1), // 未设置主键
  INPUT(2), // 手动输入
  ID_WORKER(3), // 默认的方式,全局唯一id
  UUID(4), // 全局唯一id uuid
  ID_WORKER_STR(5); //ID_WORKER 字符串表示法
}
```

#### 更新操作

```java
User user = new User();
// 通过条件自动拼接动态sql
user.setId(1341988615581687811L);
user.setName("kwhua_mybatis-plus_updateTest");
user.setAge(20);
// 注意：updateById 但是参数是一个对象！
int i = userMapper.updateById(user);
System.out.println(i); // 打印：1
```

#### 删除操作

##### 根据ID删除

```java
userMapper.deleteById(1L);
```

##### 通过ID批量删除

```java
userMapper.deleteBatchIds(Arrays.asList(2L,3L));
```

##### 通过map删除

```java
HashMap<String, Object> map = new HashMap<>();
map.put("name","mybatis-plus_insertTest");
userMapper.deleteByMap(map);
```

### MyBatis-Plus 高级操作

#### 自动填充

自动化完成创建时间、修改时间这两个字段的操作，我们不希望手动更新！

1. 在表中新增字段 gmt_create, gmt_modified。

2. 实体类字段属性上需要增加注解

   ```java
   @TableField(fill = FieldFill.INSERT)
   private Date gmt_create;
   
   @TableField(fill = FieldFill.INSERT_UPDATE)
   private Date gmt_modified;
   ```

3. 编写处理器来处理这个注解

   ```java
   import com.baomidou.mybatisplus.core.handlers.MetaObjectHandler;
   import lombok.extern.slf4j.Slf4j;
   import org.apache.ibatis.reflection.MetaObject;
   import org.springframework.stereotype.Component;
   
   import java.util.Date;
   
   @Slf4j
   @Component // 一定不要忘记把处理器加到IOC容器中！
   public class MyMetaObjectHandler implements MetaObjectHandler {
       // 插入时的填充策略
       @Override
       public void insertFill(MetaObject metaObject) {
           log.info("start insert fill.....");
           // setFieldValByName(String fieldName, Object fieldVal, MetaObject metaObject
           this.setFieldValByName("gmt_create",new Date(),metaObject);
           this.setFieldValByName("gmt_modified",new Date(),metaObject);
       }
   
       // 更新时的填充策略
       @Override
       public void updateFill(MetaObject metaObject) {
           log.info("start update fill.....");
           this.setFieldValByName("gmt_modified",new Date(),metaObject);
       }
   }
   ```

4. 注入 Handler

   ```java
   protected SqlSessionFactory sqlSessionFactory(DataSource dataSource, String mapperLocation) throws Exception {
       MybatisSqlSessionFactoryBean factoryBean = new MybatisSqlSessionFactoryBean();
       factoryBean.setDataSource(dataSource);
       ResourcePatternResolver resourceResolver = new PathMatchingResourcePatternResolver();
       Resource[] resource= resourceResolver.getResources(mapperLocation);
       factoryBean.setMapperLocations(resource);
       // 将 MyMetaObjectHandler 设置进入 GlobalConfig
       GlobalConfig globalConfig = new GlobalConfig();
       globalConfig.setMetaObjectHandler(new MyMetaObjectHandler());
       factoryBean.setGlobalConfig(globalConfig);
       return factoryBean.getObject();
   }
   ```

5. 测试插入和更新，检查时间变化。

#### 乐观锁

乐观锁 : 顾名思义，十分乐观，它总是认为不会出现问题，无论干什么不去上锁！如果出现了问题， 再次更新值测试。

悲观锁：顾名思义，十分悲观，它总是认为总是出现问题，无论干什么都会上锁！再去操作！

乐观锁实现方式：取出记录时，获取当前version 更新时，带上这个version 执行更新时， set version = newVersion where version = oldVersion 如果version不对，就更新失败。

1. 给数据库中增加version字段！

2. 实体类加对应的字段

   ```java
   @Version //乐观锁Version注解
   private Integer version;
   ```

3. 注册插件

   ```java
   @MapperScan("com.jueee.mapper")
   @EnableTransactionManagement
   @Configuration // 配置类
   public class MyBatisPlusConfig {
       
       @Bean // 注册乐观锁插件
       public OptimisticLockerInterceptor optimisticLockerInterceptor() {
           return new OptimisticLockerInterceptor();
       }
   }
   ```

4. 乐观锁测试

   ```java
   User user = userMapper.selectById("1"); // 先查询user
   user.setAge(20);
   userMapper.updateById(user); // 然后更新，version字段已经由1变成了2
   ```

   ```java
   // 线程 1
   User user1 = userMapper.selectById(1L);
   user1.setAge(20);
   // 模拟另外一个线程执行了插队操作
   User user2 = userMapper.selectById(1L);
   user2.setAge(18);
   int update2 = userMapper.updateById(user2);
   log.info("update2:"+update2);   // update2:1
   int update1 = userMapper.updateById(user1); // 如果没有乐观锁就会覆盖插队线程的值！
   log.info("update1:"+update1);   // update1:0
   ```

如果自定义了MybatisSqlSessionFactoryBean 需要手动加入插件：

```java
MybatisSqlSessionFactoryBean factoryBean = new MybatisSqlSessionFactoryBean();
factoryBean.setPlugins(optimisticLockerInterceptor());
```

否则会报错：

> org.apache.ibatis.binding.BindingException: Parameter 'MP_OPTLOCK_VERSION_ORIGINAL' not found. Available parameters are [param1, et]

#### 逻辑删除

1. 在数据库加上 is_deleted 字段，默认值为 0（未删除）

2. 实体类中增加属性

   ```java
   @TableLogic //逻辑删除
   private Integer is_deleted;
   ```

3. 配置文件配置：

   ```yaml
   mybatis-plus:
     global-config:
       db-config:
         logic-delete-value: 1 # 逻辑已删除值(默认为 1)
         logic-not-delete-value: 0 # 逻辑未删除值(默认为 0)
   ```

测试删除，is_deleted 字段值也从0修改成了1：

```java
userMapper.deleteById(4L);
```

![image-20201225160326916](/images/2020/12/image-20201225160326916.png)

此时，查询分页时，也会自动携带 `is_deleted=0` 的查询条件。

![image-20201225160519777](/images/2020/12/image-20201225160519777.png)

#### 性能分析插件

导入插件：

```java
@Bean
@Profile({"dev","test"})// 设置 dev test 环境开启，保证我们的效率
public PerformanceInterceptor performanceInterceptor() {
    PerformanceInterceptor performanceInterceptor = new PerformanceInterceptor();
    performanceInterceptor.setMaxTime(100); //ms 设置sql执行的最大时间，如果超过了则不执行
    performanceInterceptor.setFormat(true);
    return performanceInterceptor;
}
```

但是官方在 3.2.0 版本移除 PerformanceInterceptor 了相关, 建议使用 p6spy。[更新文档](https://github.com/baomidou/mybatis-plus/blob/3.0/CHANGELOG.md#v320-20190826)

