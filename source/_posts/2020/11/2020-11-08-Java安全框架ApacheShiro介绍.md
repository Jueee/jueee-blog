---
title: Java安全框架Apache Shiro介绍
layout: info
commentable: true
date: 2020-11-08
mathjax: true
mermaid: true
tags: [Java,JavaJar,Apache]
categories: 
- [Java,JavaJar]
- [Apache,Shiro]
description: 
---

### Apache Shiro 介绍

Apache Shiro 是一个强大灵活的开源安全框架。

Apache Shiro 可以帮助我们完成：认证、授权、加密、会话管理、与 Web 集成、缓存等。

- 官网：https://shiro.apache.org/
- GitHub：https://github.com/apache/shiro

<!--more-->

#### Jar 引入

```xml
<!-- https://mvnrepository.com/artifact/org.apache.shiro/shiro-spring -->
<dependency>
    <groupId>org.apache.shiro</groupId>
    <artifactId>shiro-spring</artifactId>
    <version>1.7.0</version>
</dependency>
```

#### 基本功能点

![image-20201106155220875](/images/2020/11/image-20201106155220875.png)

- **Authentication**：身份认证 / 登录，验证用户是不是拥有相应的身份；
- **Authorization**：授权，即权限验证，验证某个已认证的用户是否拥有某个权限；即判断用户是否能做事情，常见的如：验证某个用户是否拥有某个角色。或者细粒度的验证某个用户对某个资源是否具有某个权限；
- **Session** **Management**：会话管理，即用户登录后就是一次会话，在没有退出之前，它的所有信息都在会话中；会话可以是普通 JavaSE 环境的，也可以是如 Web 环境的；
- **Cryptography**：加密，保护数据的安全性，如密码加密存储到数据库，而不是明文存储；
- **Web Support**：Web 支持，可以非常容易的集成到 Web 环境；
- **Caching**：缓存，比如用户登录后，其用户信息、拥有的角色 / 权限不必每次去查，这样可以提高效率；
- **Concurrency**：shiro 支持多线程应用的并发验证，即如在一个线程中开启另一个线程，能把权限自动传播过去；
- **Testing**：提供测试支持；
- **Run As**：允许一个用户假装为另一个用户（如果他们允许）的身份进行访问；
- **Remember Me**：记住我，这个是非常常见的功能，即一次登录后，下次再来的话不用登录了。

**记住一点，Shiro 不会去维护用户、维护权限；这些需要我们自己去设计 / 提供；然后通过相应的接口注入给 Shiro 即可。**

### Apache Shiro 使用

#### 身份验证

**身份验证**，即在应用中谁能证明他就是他本人。一般提供如他们的身份 ID 一些标识信息来表明他就是他本人，如提供身份证，用户名 / 密码来证明。

在 shiro 中，用户需要提供 `principals` （身份）和 `credentials`（证明）给 shiro，从而应用能验证用户身份：

**principals**：身份，即主体的标识属性，可以是任何东西，如用户名、邮箱等，唯一即可。一个主体可以有多个 `principals`，但只有一个 `Primary principals`，一般是用户名 / 密码 / 手机号。

**credentials**：证明 / 凭证，即只有主体知道的安全值，如密码 / 数字证书等。

1. 首先准备一些用户身份 / 凭据（shiro.ini）

   ```ini
   [users]
   zhang=123
   wang=123
   ```

   此处使用 ini 配置文件，通过 [users] 指定了两个主体：zhang/123、wang/123。

2. 示例：

   ```java
   //1、获取SecurityManager工厂，此处使用Ini配置文件初始化SecurityManager  
   Factory<SecurityManager> factory = new IniSecurityManagerFactory("classpath:shiro.ini");
   //2、得到SecurityManager实例 并绑定给SecurityUtils
   SecurityManager securityManager = factory.getInstance();
   SecurityUtils.setSecurityManager(securityManager);
   //3、得到Subject及创建用户名/密码身份验证Token（即用户身份/凭证）
   Subject subject = SecurityUtils.getSubject();
   UsernamePasswordToken token = new UsernamePasswordToken("zhang", "123");
   try {
       //4、登录，即身份验证
       subject.login(token);
   } catch (Exception e) {
       //5、身份验证失败
   }
   System.out.println(subject.isAuthenticated());
   //6、退出
   subject.logout();
   ```

#### 授权

**基于角色的访问控制（隐式角色）**

在 ini 配置文件配置用户拥有的角色（shiro-role.ini）

```ini
[users]
zhang=123,role1,role2
wang=123,role1
```

规则即：“用户名=密码,角色1，角色2”，如果需要在应用中判断用户是否有相应角色，就需要在相应的 Realm 中返回角色信息。

**基于资源的访问控制（显示角色）**

在 ini 配置文件配置用户拥有的角色及角色-权限关系

```ini
[users]
zhang=123,role1,role2
wang=123,role1
[roles]
role1=user:create,user:update
role2=user:create,user:delete
```

规则：“用户名=密码，角色 1，角色 2”“角色=权限 1，权限 2”，即首先根据用户名找到角色，然后根据角色再找到权限

