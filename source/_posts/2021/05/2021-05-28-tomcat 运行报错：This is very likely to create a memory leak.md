---
title: tomcat 运行报错：This is very likely to create a memory leak
layout: info
commentable: true
date: 2021-05-28
mathjax: true
mermaid: true
tags: [Apache,Maven]
categories: [Apache,Maven]
description: 
---

### 问题

tomcat 运行时，报如下异常：

```
SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/C:/Users/Jueee/.m2/repository/org/slf4j/slf4j-log4j12/1.7.21/slf4j-log4j12-1.7.21.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/C:/Users/Jueee/.m2/repository/org/apache/logging/log4j/log4j-slf4j-impl/2.13.3/log4j-slf4j-impl-2.13.3.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Detected both log4j-over-slf4j.jar AND slf4j-log4j12.jar on the class path, preempting StackOverflowError. 
SLF4J: See also http://www.slf4j.org/codes.html#log4jDelegationLoop for more details.
26-May-2021 18:44:40.531 严重 [localhost-startStop-1] org.apache.catalina.core.StandardContext.startInternal One or more listeners failed to start. Full details will be found in the appropriate container log file
26-May-2021 18:44:40.531 严重 [localhost-startStop-1] org.apache.catalina.core.StandardContext.startInternal Context [/adminWeb] startup failed due to previous errors
26-May-2021 18:44:40.545 警告 [localhost-startStop-1] org.apache.catalina.loader.WebappClassLoaderBase.clearReferencesThreads The web application [adminWeb] appears to have started a thread named [Timer-0] but has failed to stop it. This is very likely to create a memory leak. Stack trace of thread:
 java.lang.Object.wait(Native Method)
 java.lang.Object.wait(Object.java:502)
 java.util.TimerThread.mainLoop(Timer.java:526)
 java.util.TimerThread.run(Timer.java:505)
```

<!--more-->

### 解决

根据提示，查看 [http://www.slf4j.org/codes.html#log4jDelegationLoop](http://www.slf4j.org/codes.html#log4jDelegationLoop) 获取报错详情。

可以发现是由于 slf4j-log4j12-1.7.21.jar 和 log4j-slf4j-impl-2.13.3.jar 两个 Jar 包冲突导致的。

使用如下命令导致 maven 依赖关系树：

```
mvn dependency:tree>tree.txt
```
从树中找到上述的两个 Jar包 依赖关系，根据项目需要，保留一个，排除另一个即可。

![image-20210527100457799](/images/2021/05/image-20210527100457799.png)

排除 Jar 包：

```xml
<dependency>
    <groupId>xxx</groupId>
    <artifactId>xxx</artifactId>
    <version>xxx</version>
    <exclusions>
        <exclusion>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-log4j12</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

