---
title: Springboot启用https安全协议
layout: info
commentable: true
date: 2021-12-17
mathjax: true
mermaid: true
tags: [Java,SpringBoot,keytool,https]
categories: [Java,SpringBoot]
description: 
---

有时候我们需要使用https安全协议，本文记录在SpringBoot项目启用https。

<!--more-->

### 生成证书

#### 自签名证书

使用java jdk自带的生成SSL证书的工具keytool生成自己的证书

打开cmd，输入命令生成证书：

```shell
keytool -genkeypair -alias tomcat_https -keypass 123456 -keyalg RSA -keysize 1024 -validity 365 -keystore e:/tomcat_https.keystore -storepass 123456
```

如下图所示：

![image-20211217150947402](/images/2021/12/image-20211217150947402.png)

### 项目配置

#### 导入证书

把生成的 tomcat_https.keystore 放在 resources 里：

![image-20211217151120125](/images/2021/12/image-20211217151120125.png)

#### 配置文件

在 `application.properties` 配置文件中增加配置：

```properties
#https默认端口：443，http默认端口：80
server.port=443
server.http-port=80

#开启https，配置跟证书一一对应
server.ssl.enabled=true
#指定证书
server.ssl.key-store=classpath:tomcat_https.keystore
server.ssl.key-store-type=JKS
#别名
server.ssl.key-alias=tomcat_https
#密码
server.ssl.key-password=123456
server.ssl.key-store-password=123456

spring.application.name=springboot-https
```

#### 加载keystore文件

Springboot 工程可能出现不能加载`.keystore`文件的情况(can not load .keystore)

明明是加入到了类路径，但却没有加载，于是到编译生成的 target\class 去找 tomcat_https.keystore 文件，发现确实没有这个文件，那么就是在编译的时候将这个 tomcat_https.keystore 文件排除了。

注意 tomcat_https.keystore文件是二进制文件，应该是这个插件将这个过滤了。

此时，需要在项目 pom 文件中增加如下配置：

```xml
<build>
    <resources>
        <resource>
            <directory>src/main/resources</directory>
            <filtering>true</filtering>
            <excludes>
                <exclude>*.keystore</exclude>
            </excludes>
        </resource>
        <resource>
            <directory>src/main/resources</directory>
            <filtering>false</filtering>
            <includes>
                <include>*.keystore</include>
            </includes>
        </resource>
    </resources>
</build>
```

### 测试功能

测试类：

```java
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Date;

@Slf4j
@RestController
@RequestMapping("/hello")
public class HelloController {

    @GetMapping("/info")
    public String info() {
        log.info("init info.."+new Date());
        return "success!!!";
    }
}
```

访问：https://127.0.0.1:443/hello/info

![image-20211217152249160](/images/2021/12/image-20211217152249160.png)
