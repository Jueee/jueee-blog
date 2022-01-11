---
title: Java编译class并运行文件的main方法
layout: info
commentable: true
date: 2021-12-10
mathjax: true
mermaid: true
tags: [Java]
categories: Java
description: 
---

验证 jvm 参数对 Jar 包中参数值的影响。

<!--more-->

### Java 文件

Log4jCoreTest.java 文件：

```java

import org.apache.logging.log4j.core.util.Constants;

public class Log4jCoreTest {

    public static void main(String[] args) {
            boolean value = Constants.FORMAT_MESSAGES_PATTERN_DISABLE_LOOKUPS;
            System.out.println("value is:"+value);
    }
}

```

### 依赖 Jar

放入 lib 文件夹下：

```
$ ls
lib  Log4jCoreTest.class  Log4jCoreTest.java

$ ls lib/
log4j-api-2.15.1.jar  log4j-core-2.15.1.jar
```

### 编译 Java 文件

```
javac -encoding UTF-8 -classpath lib/log4j-core-2.13.3.jar Log4jCoreTest.java
```

### 运行 Java 文件

```
java -classpath .:./lib/*   Log4jCoreTest
```

### 运行结果

如果是 2.13.3 版本：

```
$ java -classpath .:./lib/*   Log4jCoreTest
value is:false

$ java -classpath .:./lib/*  -Dlog4j2.formatMsgNoLookups=true  Log4jCoreTest
value is:true
```

如果是 2.15.1 版本：

```
$ java -classpath .:./lib/*   Log4jCoreTest
value is:true
```

