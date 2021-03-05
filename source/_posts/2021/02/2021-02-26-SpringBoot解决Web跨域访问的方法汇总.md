---
title: SpringBoot解决Web跨域访问的方法汇总
layout: info
commentable: true
date: 2021-02-26
mathjax: true
mermaid: true
tags: [Java,SpringBoot]
categories: [Java,SpringBoot]
description: 
---

跨域访问时很多需求，所以SpringBoot的跨域解决也是必须的。

```
Access to XMLHttpRequest at 'http://127.0.0.1:18888/XXXX' from origin 'http://127.0.0.1:8080' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

<!--more-->

### 过滤器方式

```java
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Configuration;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

@Slf4j
@Configuration
public class CorsFilter implements Filter {
    public CorsFilter() {
        log.info("SimpleCORSFilter init");
    }

    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest request = (HttpServletRequest) req;
        HttpServletResponse response = (HttpServletResponse) res;

        if (request.getHeader("Origin") != null) {
            response.setHeader("Access-Control-Allow-Origin", request.getHeader("Origin"));
        }

        response.setHeader("Access-Control-Allow-Credentials", "true");
        response.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
        response.setHeader("Access-Control-Max-Age", "3600");
        response.setHeader("Access-Control-Allow-Headers", "Content-Type, Accept, X-Requested-With, remember-me");

        chain.doFilter(req, res);
    }

    @Override
    public void init(FilterConfig filterConfig) {
    }

    @Override
    public void destroy() {
    }
}
```

### Web MVC Configuration

```java
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurationSupport;

@Slf4j
@Configuration
public class CrosConfig extends WebMvcConfigurationSupport {

    @Override
    protected void addCorsMappings(CorsRegistry registry) {
        super.addCorsMappings(registry);
        log.info("WebMVC configuration : addCorsMappings");
        registry.addMapping("/**").allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS");
    }
}
```

### SpringBoot跨域注解

SpringBoot 自带的跨域注解，可以放在RestController的类上或者方法上，还能自定义那些域名可以跨域，非常灵活。

方法上：

```java
    @GetMapping(value = "/sendSessionid")
    @CrossOrigin(origins = "*", allowedHeaders = "*")
```

类上：

```java
@RestController
@CrossOrigin(origins = "*", allowedHeaders = "*")
public class SessionController {

}
```

