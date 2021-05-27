---
title: maven打包找不到程序包 java.lang
layout: info
commentable: true
date: 2021-05-27
mathjax: true
mermaid: true
tags: [Apache,Maven]
categories: [Apache,Maven]
description: 
---

maven 打包项目时出现如下问题：

```
[ERROR] Failure executing javac, but could not parse the error:
致命错误: 在类路径或引导类路径中找不到程序包 java.lang
```

<!--more-->

### 问题

这是在基于 maven 编写java项目的时候，使用 mvn install 时发生的异常，异常信息如下

```
[INFO] --- maven-compiler-plugin:2.5.1:compile (default-compile) @ webAdmin ---
[INFO] Compiling 537 source files to E:\code\webAdmin\target\classes
[INFO] -------------------------------------------------------------
[ERROR] COMPILATION ERROR :
[INFO] -------------------------------------------------------------
[ERROR] Failure executing javac, but could not parse the error:
致命错误: 在类路径或引导类路径中找不到程序包 java.lang

[INFO] 1 error
[INFO] -------------------------------------------------------------
[INFO] ------------------------------------------------------------------------
[INFO] BUILD FAILURE
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 01:26 min
[INFO] Finished at: 2021-05-26T17:10:55+08:00
[INFO] Final Memory: 65M/1934M
```

### 原因

原因在于 compiler 插件的配置。

如下所示的配置很特殊：windows下使用分号（;）分隔，linux/mac下使用冒号（:）分隔

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>${maven.compiler.version}</version>
    <configuration>
        <source>${java.version}</source>
        <target>${java.version}</target>
        <encoding>UTF-8</encoding>
        <!-- 不是maven推荐的方式，只是为了方便管理后台人员频繁开发的jar包 -->
        <compilerArguments>
            <extdirs>src\main\webapp\WEB-INF\lib</extdirs>
            <!-- 这个配置很特殊：windows下使用分号（;）分隔，linux/mac下使用冒号（:）分隔 -->
          <bootclasspath>${java.home}/lib/rt.jar:${java.home}/lib/jce.jar</bootclasspath>
        </compilerArguments>
    </configuration>
</plugin>
```

### 解决

修改为 使用分号（;）分隔后，再次打包，即可成功。