---
title: 使用SpringBoot Security登录Web页面
layout: info
commentable: true
date: 2022-02-12
mathjax: true
mermaid: true
tags: [Java,SpringBoot]
categories: [Java,SpringBoot]
description: 
---

使用 SpringBoot 开发简单 Web 页面时，如果没有身份验证是非常不安全的。

此时，可以考虑使用 Spring Security 进行身份验证的登录。

<!--more-->

### Spring Security

Spring Security是一个功能强大且高度可定制的身份验证和访问控制框架。

提供了完善的**认证机制**和方法级的**授权功能**。是一款非常优秀的权限管理框架。它的核心是一组过滤器链，不同的功能经由不同的过滤器。

#### 引入依赖

```xml
<dependency>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

### 配置用户和密码登录

可以在 application.properteis 中配置对应的用户和密码：

```properties
spring.security.user.name=admin
spring.security.user.password=password
```

![image-20220214184538321](/images/2022/02/image-20220214184538321.png)

### 自定义登录页面

如果觉得默认登录页面不太满意实际需要，那么可以自定义登录页面。

#### 登录 HTML

页面命名为 `login.html`，需要放在`\src\main\resources\resources\`这个路径下（注意有两个resources文件夹）。

放在这个路径下呢，项目启动起来之后可以直接访问到我们的html文件，这是spring boot默认配置。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <title>Please sign in</title>
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" rel="stylesheet"
          crossorigin="anonymous">
    <link href="https://getbootstrap.com/docs/4.0/examples/signin/signin.css" rel="stylesheet" crossorigin="anonymous"/>
</head>
<body>
<div class="container">
    <form class="form-signin" method="post" action="/login">
        <h2 class="form-signin-heading">请登录：</h2>
        <p>
            <label for="username" class="sr-only">用户名</label>
            <input type="text" id="username" name="username" class="form-control" placeholder="请输入用户名" required
                   autofocus>
        </p>
        <p>
            <label for="password" class="sr-only">密码</label>
            <input type="password" id="password" name="password" class="form-control" placeholder="请输入密码" required>
        </p>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
    </form>
</div>
</body>
</html>
```

为方便演示，以上只是把默认的登录页面 HTML，进行了中文翻译。

#### 配置 Spring Security

配置Spring Security需要写一个类，继承`WebSecurityConfigurerAdapter`，然后根据自己的需求重写一些方法。

我们自定义登录页面这个需求只需要重写`void configure(HttpSecurity http)`这个方法即可。

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;

@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.formLogin()
                .loginPage("/login.html")
                .loginProcessingUrl("/login")
                .and()
                .authorizeRequests()
                .antMatchers("/login.html", "/login").permitAll()
                .anyRequest().authenticated()
                .and()
                .csrf().disable();
    }
}
```

配置大概解释一下：

- `.formLogin()`，表示Spring Security使用form表单登录的方式（另外还有一种登录的方式是Basic登录）。

- `.loginPage("/login.html")`，表示spring security默认的登录页路径为`/login.html`，就是我们上面写的html文件的名字。

- `.loginProcessingUrl("/login")`，表示处理登录请求的接口为`/login`，就是我们上面写的form表单`action`属性的值。

- `.and().authorizeRequests().anyRequest().authenticated()` 三行配置表示所有的请求都需要认证。

- `.antMatchers("/login.html", "/login").permitAll()` 表示将登录页面配置为不需要认证。

- `.csrf().disable()` 是关闭 csrf。

#### csrf 防护

Spring Security 默认开启了csrf 防护，只要在请求中带上 csrf token 就可以了。

这个 token 在返回登录页面的时候 Spring Security 已经帮我们准备好了，只是我们没有使用模板引擎，所以取到 token 比较困难。

![image-20220214185645015](/images/2022/02/image-20220214185645015.png)

#### 页面效果

![image-20220215095848804](/images/2022/02/image-20220215095848804.png)

  

  

  

  

  

  

  

  

  
