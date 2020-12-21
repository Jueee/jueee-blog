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
- [Database,MySQL]
- [Apache,Commons]
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

#### 示例代码

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

import org.apache.commons.dbutils.DbUtils;
import org.apache.commons.dbutils.QueryRunner;
import org.apache.commons.dbutils.ResultSetHandler;
import org.apache.commons.dbutils.handlers.BeanHandler;

public class MainApp {
	static final String JDBC_DRIVER = "com.mysql.jdbc.Driver";
	static final String DB_URL = "jdbc:mysql://localhost:3306/test?serverTimezone=UTC";

	static final String USER = "user";
	static final String PASS = "password";

	public static void main(String[] args) throws SQLException {
		Connection conn = null;
		QueryRunner queryRunner = new QueryRunner();
		conn = DriverManager.getConnection(DB_URL, USER, PASS);
		ResultSetHandler<Employee> resultHandler = new BeanHandler<Employee>(Employee.class);
		try {
			Employee emp = queryRunner.query(conn, "SELECT * FROM employees WHERE first=?", resultHandler, "Sumit");
			// Display values
			System.out.print("ID: " + emp.getId() + ", Age: " + emp.getAge() + ", First: " + emp.getFirst() + ", Last: " + emp.getLast());
		} finally {
			DbUtils.close(conn);
		}
	}
}
```

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

### 数据操作

#### 新增数据

```java
String insertQuery ="INSERT INTO employees(id,age,first,last)  VALUES (?,?,?,?)";
int insertedRecords = queryRunner.update(conn, insertQuery, 104, 30, "Sohan","Kumar");
```

#### 读取数据

```java
ResultSetHandler<Employee> resultHandler = new BeanHandler<Employee>(Employee.class);
Employee emp = queryRunner.query(conn, "SELECT * FROM employees WHERE first=?", resultHandler, "Sumit");
```

其中，

- *resultHandler*  − `ResultSetHandler`对象将结果集映射到`Employee`对象。
- *queryRunner* − `QueryRunner`对象在数据库中插入`Employee`对象。

#### 更新数据

```java
String updateQuery = "UPDATE employees SET age=? WHERE id=?";
int updatedRecords = queryRunner.update(conn, updateQuery, 33, 104);
```

其中，

- *updateQuery* − 更新包含占位符的查询。
- *queryRunner* − QueryRunner对象更新数据库中的员工对象。

#### 删除数据

```java
String deleteQuery = "DELETE FROM employees WHERE id=?";
int deletedRecords = queryRunner.delete(conn, deleteQuery, 33,104);
Java
```

其中，

- *deleteQuery* − 删除包含占位符的查询。
- *queryRunner* − `QueryRunner`对象删除数据库中的员工对象。

### DBUtils 核心类

#### QueryRunner

`org.apache.commons.dbutils.QueryRunner`类是DBUtils库中的中心类。 

它执行带有可插入策略的SQL查询来处理`ResultSets`。 这个类是线程安全的。

#### AsyncQueryRunner

`org.apache.commons.dbutils.AsyncQueryRunner`类有助于执行具有异步支持的长时间运行的SQL查询。 这个类是线程安全的。 

该类支持与`QueryRunner`相同的方法，但它返回`Callable`对象，在之后可以使用它来检索结果。

#### ResultSetHandler

`org.apache.commons.dbutils.ResultSetHandler`接口负责将ResultSets转换为对象。

#### BeanHandler

`org.apache.commons.dbutils.BeanHandler`是`ResultSetHandler`接口的实现，负责将第一个`ResultSet`行转换为`JavaBean`。 这个类是线程安全的。

#### BeanListHandler

`org.apache.commons.dbutils.BeanListHandler`是`ResultSetHandler`接口的实现，负责将`ResultSet`行转换为Java Bean列表。 这个类是线程安全的。

#### ArrayListHandler

`org.apache.commons.dbutils.ArrayListHandler`是`ResultSetHandler`接口的实现，负责将`ResultSet`行转换为`object[]`。 这个类是线程安全的。

#### MapListHandler

`org.apache.commons.dbutils.MapListHandler`是`ResultSetHandler`接口的实现，负责将`ResultSet`行转换为Maps列表。 这个类是线程安全的。

### 自定义DBUtils

#### 自定义处理程序

可以通过实现`ResultSetHandler`接口或扩展任何现有的`ResultSetHandler`实现来创建自己的自定义处理程序。

在下面的示例中，我们通过扩展`BeanHandler`类创建了自定义处理程序`EmployeeHandler`。

EmployeeHandler.java

```java
import java.sql.ResultSet;
import java.sql.SQLException;

import org.apache.commons.dbutils.handlers.BeanHandler;

public class EmployeeHandler extends BeanHandler<Employee> {

	public EmployeeHandler() {
		super(Employee.class);
	}

	@Override
	public Employee handle(ResultSet rs) throws SQLException {
		Employee employee = super.handle(rs);
		employee.setName(employee.getFirst() + ", " + employee.getLast());
		return employee;
	}
}
```

MyHandlerMain.java

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

import org.apache.commons.dbutils.DbUtils;
import org.apache.commons.dbutils.QueryRunner;

public class MyHandlerMain {
	static final String DB_URL = "jdbc:mysql://localhost:3306/test?serverTimezone=UTC";
	static final String USER = "user";
	static final String PASS = "password";

	public static void main(String[] args) throws SQLException {
		Connection conn = null;
		QueryRunner queryRunner = new QueryRunner();
		conn = DriverManager.getConnection(DB_URL, USER, PASS);
		EmployeeHandler employeeHandler = new EmployeeHandler();

		try {
			Employee emp = queryRunner.query(conn, "SELECT * FROM employees WHERE first=?", employeeHandler, "Sumit");
			System.out.print("ID: " + emp.getId() + ", Age: " + emp.getAge() + ", Name: " + emp.getName());
		} finally {
			DbUtils.close(conn);
		}
	}
}
```

#### 自定义行处理器

如果数据库表中的列名和等价的javabean对象名称不相似，那么我们可以通过使用自定义的`BasicRowProcessor`对象来映射它们。

EmployeeHandler2.java

```java
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Map;

import org.apache.commons.dbutils.BasicRowProcessor;
import org.apache.commons.dbutils.BeanProcessor;
import org.apache.commons.dbutils.handlers.BeanHandler;

public class EmployeeHandler2 extends BeanHandler<Employee> {

   public EmployeeHandler2() {
      super(Employee.class, new BasicRowProcessor(new BeanProcessor(mapColumnsToFields())));
   }

   @Override
   public Employee handle(ResultSet rs) throws SQLException {
      Employee employee = super.handle(rs);
      employee.setName(employee.getFirst() +", " + employee.getLast());
      return employee;
   }

   public static Map<String, String> mapColumnsToFields() {
      Map<String, String> columnsToFieldsMap = new HashMap<>();
      columnsToFieldsMap.put("ID", "id");
      columnsToFieldsMap.put("AGE", "age");        
      return columnsToFieldsMap;
   }
}
```

MyHandlerMain2.java

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

import org.apache.commons.dbutils.DbUtils;
import org.apache.commons.dbutils.QueryRunner;

public class MyHandlerMain2 {
	static final String DB_URL = "jdbc:mysql://localhost:3306/test?serverTimezone=UTC";
	static final String USER = "user";
	static final String PASS = "password";

	public static void main(String[] args) throws SQLException {
		Connection conn = null;
		QueryRunner queryRunner = new QueryRunner();
		conn = DriverManager.getConnection(DB_URL, USER, PASS);
		EmployeeHandler employeeHandler = new EmployeeHandler();

		try {
			Employee emp = queryRunner.query(conn, "SELECT * FROM employees WHERE first=?", employeeHandler, "Sumit");
			System.out.print("ID: " + emp.getId() + ", Name: " + emp.getName());
		} finally {
			DbUtils.close(conn);
		}
	}
}
```

#### 使用DataSource

 以下示例将演示如何在`QueryRunner`和数据源的帮助下使用查询读取记录。 

**语法**

```java
QueryRunner queryRunner = new QueryRunner( dataSource );
Employee emp = queryRunner.query("SELECT * FROM employees WHERE first=?", resultHandler, "Sumit");
```

其中，

- `dataSource` - 配置了`DataSource`对象。
- `resultHandler` - `ResultSetHandler`对象将结果集映射到`Employee`对象。
- `queryRunner` - 用于从数据库读取`Employee`对象的`QueryRunner`对象。

需要引入 Jar 包：

```xml
<dependency>
    <groupId>commons-dbutils</groupId>
    <artifactId>commons-dbutils</artifactId>
    <version>1.7</version>
</dependency>
```

CustomDataSource.java：

```java
import javax.sql.DataSource;
import org.apache.commons.dbcp2.BasicDataSource;

public class CustomDataSource {
	static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";
	static final String DB_URL = "jdbc:mysql://localhost:3306/test?serverTimezone=UTC";
	static final String USER = "user";
	static final String PASS = "password";
	private static final BasicDataSource basicDataSource;

	static {
		basicDataSource = new BasicDataSource();
		basicDataSource.setDriverClassName(JDBC_DRIVER);
		basicDataSource.setUsername(USER);
		basicDataSource.setPassword(PASS);
		basicDataSource.setUrl(DB_URL);
	}

	public static DataSource getInstance() {
		return basicDataSource;
	}
}
```

MyHandlerMain3.java

```java
import java.sql.SQLException;

import org.apache.commons.dbutils.QueryRunner;
import org.apache.commons.dbutils.ResultSetHandler;
import org.apache.commons.dbutils.handlers.BeanHandler;

public class MyHandlerMain3 {
	public static void main(String[] args) throws SQLException {
		QueryRunner queryRunner = new QueryRunner(CustomDataSource.getInstance());
		ResultSetHandler<Employee> resultHandler = new BeanHandler<Employee>(Employee.class);
		Employee emp = queryRunner.query("SELECT * FROM employees WHERE id=?", resultHandler, 103);
		System.out.print("ID: " + emp.getId() + ", Age: " + emp.getAge() + ", First: " + emp.getFirst() + ", Last: " + emp.getLast());
	}
}
```



### 参考资料

- https://www.yiibai.com/dbutils