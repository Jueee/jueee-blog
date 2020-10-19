---
title: PHP之通过MySQLi操作MySQL数据库
layout: info
commentable: true
date: 2020-10-16
mathjax: true
mermaid: true
tags: [PHP,MySQL]
categories: 
- [PHP]
- [MySQL]
description: 
---

### MySQLi 介绍

MySQLi 扩展使得用户可以利用MySQL 4.1及其更高版本的新功能，与mysql扩展相比，MySQLi 扩展在以下方面有了明显的提高。

- **兼容性与维护性**：

  MySQLi 扩展可以很容易地使用MySQL的新功能，所以MySQLi 拥有与MySQL更高的兼容性。即使MySQL的新版本又出现了更多功能，MySQLi 扩展也可以很容易的支持。

- **面向对象**：

  MySQLi 扩展已封装到一个类中，从而可使用面向对象的方式编程。即使对面向对象不了解，MySQLi 扩展也提供了面向过程的编程方式来供用户选择。

- **速度和安全性**：

  MySQLi 扩展执行的速度要比之前版本的mysql扩展快了很多。MySQLi 扩展支持MySQL新版本的密码杂凑（Password Hashes）和验证程序，更加提高了应用程序的安全性。

- **预准备语句**：

  预准备语句可提高重复使用的语句的性能，MySQLi 扩展提供了对预准备语句的支持。

- **调试功能**：

  MySQLi 扩展进一步改进了调试功能，提高了开发效率。

### MySQLi 安装

Linux 和 Windows: 在 php7 mysql 包安装时 MySQLi 扩展多数情况下是自动安装的。

安装详细信息，请查看： http://php.net/manual/en/mysqli.installation.php

可以通过 phpinfo() 查看是否安装成功：

![1603075261487](/images/2020/10/1603075261487.png)

### 连接 MySQL

```php
<?php
$servername = "localhost";
$username = "user";
$password = "password";
 
// 创建连接
$conn = mysqli_connect($servername, $username, $password);
 
// 检测连接
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}
echo "连接成功";
?>
```

### 关闭连接

连接在脚本执行完后会自动关闭。你也可以使用以下代码来关闭连接：

```php
mysqli_close($conn);
```

### 创建数据库

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
 
// 创建连接
$conn = mysqli_connect($servername, $username, $password);
// 检测连接
if (!$conn) {
    die("连接失败: " . mysqli_connect_error());
}
 
// 创建数据库
$sql = "CREATE DATABASE myDB";
if (mysqli_query($conn, $sql)) {
    echo "数据库创建成功";
} else {
    echo "Error creating database: " . mysqli_error($conn);
}
 
mysqli_close($conn);
?>
```

### 创建 MySQL 表

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";
 
// 创建连接
$conn = mysqli_connect($servername, $username, $password, $dbname);
// 检测连接
if (!$conn) {
    die("连接失败: " . mysqli_connect_error());
}
 
// 使用 sql 创建数据表
$sql = "CREATE TABLE MyGuests (
id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
firstname VARCHAR(30) NOT NULL,
lastname VARCHAR(30) NOT NULL,
email VARCHAR(50),
reg_date TIMESTAMP
)";
 
if (mysqli_query($conn, $sql)) {
    echo "数据表 MyGuests 创建成功";
} else {
    echo "创建数据表错误: " . mysqli_error($conn);
}
 
mysqli_close($conn);
?>
```

### 插入数据

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";
 
// 创建连接
$conn = mysqli_connect($servername, $username, $password, $dbname);
// 检测连接
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}
 
$sql = "INSERT INTO MyGuests (firstname, lastname, email)
VALUES ('John', 'Doe', 'john@example.com')";
 
if (mysqli_query($conn, $sql)) {
    echo "新记录插入成功";
} else {
    echo "Error: " . $sql . "<br>" . mysqli_error($conn);
}
 
mysqli_close($conn);
?>
```

`mysqli_multi_query()` 函数可用来执行多条SQL语句。

### 使用预处理语句

```php
<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";
 
// 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);
// 检测连接
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
} else {
    $sql = "INSERT INTO MyGuests(firstname, lastname, email)  VALUES(?, ?, ?)";
 
    // 为 mysqli_stmt_prepare() 初始化 statement 对象
    $stmt = mysqli_stmt_init($conn);
 
    //预处理语句
    if (mysqli_stmt_prepare($stmt, $sql)) {
        // 绑定参数
        mysqli_stmt_bind_param($stmt, 'sss', $firstname, $lastname, $email);
 
        // 设置参数并执行
        $firstname = 'John';
        $lastname = 'Doe';
        $email = 'john@example.com';
        mysqli_stmt_execute($stmt);
 
        $firstname = 'Mary';
        $lastname = 'Moe';
        $email = 'mary@example.com';
        mysqli_stmt_execute($stmt);
 
        $firstname = 'Julie';
        $lastname = 'Dooley';
        $email = 'julie@example.com';
        mysqli_stmt_execute($stmt);
    }
}
?>
```

注意参数的绑定。让我们看下 mysqli_stmt_bind_param() 中的代码：

```php
mysqli_stmt_bind_param($stmt, 'sss', $firstname, $lastname, $email);
```

该函数绑定参数查询并将参数传递给数据库。第二个参数是 "sss" 。以下列表展示了参数的类型。 s 字符告诉 mysql 参数是字符串。

可以是以下四种参数:

- i - 整数
- d - 双精度浮点数
- s - 字符串
- b - 布尔值

每个参数必须指定类型，来保证数据的安全性。

通过类型的判断可以减少SQL注入漏洞带来的风险。

### 查询读取数据

```php
<?php
$servername = "localhost";
$username = "user";
$password = "password";
$dbname = "myDB";
 
// 创建连接
$conn = mysqli_connect($servername, $username, $password, $dbname);
// Check connection
if (!$conn) {
    die("连接失败: " . mysqli_connect_error());
}
 
$sql = "SELECT id, firstname, lastname FROM MyGuests";
$result = mysqli_query($conn, $sql);
 
if (mysqli_num_rows($result) > 0) {
    // 输出数据
    while($row = mysqli_fetch_assoc($result)) {
        echo "id: " . $row["id"]. " - Name: " . $row["firstname"]. " " . $row["lastname"]. "<br>";
    }
} else {
    echo "0 结果";
}
 
mysqli_close($conn);
?>
```

