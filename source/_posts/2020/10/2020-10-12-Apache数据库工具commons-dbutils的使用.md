---
title: Apache数据库工具commons-dbutils的使用
layout: info
commentable: true
date: 2020-10-12
mathjax: true
mermaid: true
tags: [Apache,Java,JavaJar,MySQL]
categories: 
- [Java,JavaJar]
- [MySQL]
description: 
---

### Jar引入

官网：http://commons.apache.org/proper/commons-dbutils/

```xml
<dependency>
    <groupId>commons-dbutils</groupId>
    <artifactId>commons-dbutils</artifactId>
    <version>1.7</version>
</dependency>
<dependency>
    <groupId>mysql</groupId>
    <artifactId>mysql-connector-java</artifactId>
    <version>8.0.22</version>
</dependency>
```

### Jar介绍

Apache Commons DbUtils库是一个相当小的一组类，它们被设计用来在没有资源泄漏的情况下简化JDBC调用处理，并且具有更简洁的代码。

由于JDBC资源清理非常繁琐且容易出错，因此DBUtils类有助于抽取出重复代码，以便开发人员只专注于与数据库相关的操作。

<!--more-->

#### 使用优点

- **无资源泄漏** - DBUtils类确保不会发生资源泄漏。
- **清理和清除代码** - DBUtils类提供干净清晰的代码来执行数据库操作，而无需编写任何清理或资源泄漏防护代码。
- **Bean映射** - DBUtils类支持从结果集中自动填充javabeans。

#### 设计原则

- **小** - DBUtils库的体积很小，只有较少的类，因此易于理解和使用。
- **透明** - DBUtils库在后台没有做太多工作，它只需查询并执行。
- **快速** - DBUtils库类不会创建许多背景对象，并且在数据库操作执行中速度非常快。

### 连接测试

#### 异常处理

**异常一**：连接报错：

> Exception in thread "main" java.sql.SQLException: The server time zone value '�й���׼ʱ��' is unrecognized or represents more than one time zone. You must configure either the server or JDBC driver (via the 'serverTimezone' configuration property) to use a more specific time zone value if you want to utilize time zone support.

**解决**：在连接字符串后面加上`?serverTimezone=UTC`，其中UTC是统一标准世界时间。如下所示：

```java
static final String DB_URL = "jdbc:mysql://localhost:3306/test?serverTimezone=UTC";
```

**异常二**：若使用驱动 `com.mysql.jdbc.Driver` ，则虽然程序正常运行，但提示：

> Loading class `com.mysql.jdbc.Driver'. This is deprecated. The new driver class is `com.mysql.cj.jdbc.Driver'. The driver is automatically registered via the SPI and manual loading of the driver class is generally unnecessary.

**解决**：解决方案有两种：

1. 切换驱动 `com.mysql.jdbc.Driver` 为 `com.mysql.cj.jdbc.Driver`。

2. 删除驱动连接。

   ```java
   static final String JDBC_DRIVER = "com.mysql.jdbc.Driver";
   DbUtils.loadDriver(JDBC_DRIVER);
   ```

   此时，通过SPI自动注册驱动程序，不需要手动加载驱动程序类。

### 参考资料

- https://www.yiibai.com/dbutils