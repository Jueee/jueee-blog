---
title: Java的JWT实现库java-jwt介绍
layout: info
commentable: true
date: 2020-11-07
mathjax: true
mermaid: true
tags: [Java,JavaJar,JWT]
categories: [Java,JavaJar]
description: 
---

### java-jwt 介绍

auth0 的 java-jwt 是一个 JSON WEB TOKEN（JWT）的一个实现。

GitHub：https://github.com/auth0/java-jwt

#### 依赖引入

```xml
<!-- https://mvnrepository.com/artifact/com.auth0/java-jwt -->
<dependency>
    <groupId>com.auth0</groupId>
    <artifactId>java-jwt</artifactId>
    <version>3.11.0</version>
</dependency>
```

<!--more-->

### 已实现的算法

该库使用以下算法实现JWT验证和签名:

| JWS   | 算法     | 介绍                               |
| :---- | :------- | :--------------------------------- |
| HS256 | HMAC256  | HMAC with SHA-256                  |
| HS384 | HMAC384  | HMAC with SHA-384                  |
| HS512 | HMAC512  | HMAC with SHA-512                  |
| RS256 | RSA256   | RSASSA-PKCS1-v1_5 with SHA-256     |
| RS384 | RSA384   | RSASSA-PKCS1-v1_5 with SHA-384     |
| RS512 | RSA512   | RSASSA-PKCS1-v1_5 with SHA-512     |
| ES256 | ECDSA256 | ECDSA with curve P-256 and SHA-256 |
| ES384 | ECDSA384 | ECDSA with curve P-384 and SHA-384 |
| ES512 | ECDSA512 | ECDSA with curve P-521 and SHA-512 |

### JWT 基本使用

#### 产生加密Token

```java
String token = JWT.create()
		.withExpiresAt(new Date(System.currentTimeMillis()+1000)) // 设置过期时间
		.withAudience("root") // 设置接受方信息，一般时登录用户
		.sign(Algorithm.HMAC256("123456")); // 使用HMAC算法，123456作为密钥加密
System.out.println(token);
// eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJyb290IiwiZXhwIjoxNjA0NjMyMTY0fQ.5JbpimPPzTnXSVX9LL6eekH7tkFc6ApRkhIUnTGt0BY
```

#### 解密Token获取负载信息

```java
DecodedJWT jwt1 = JWT.decode(token);
String userId = jwt1.getAudience().get(0);
System.out.println(userId); // root
```

#### 验证Token是否有效

```java
Algorithm algorithm = Algorithm.HMAC256("123456");
JWTVerifier jwtVerifier = JWT.require(algorithm).withIssuer(userId).build();
DecodedJWT jwt2 = jwtVerifier.verify(token); 
System.out.println(jwt2.getAudience().get(0)); // root
```

