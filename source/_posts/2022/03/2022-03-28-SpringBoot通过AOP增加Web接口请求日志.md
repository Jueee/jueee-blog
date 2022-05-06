---
title: SpringBoot通过AOP增加Web接口请求日志
layout: info
commentable: true
date: 2022-03-28
mathjax: true
mermaid: true
tags: [Java,SpringBoot,AOP]
categories: [Java,SpringBoot]
description: 
---

在使用 SpringBoot 开发Web接口时，时常需要对接口的访问情况进行统计和追踪溯源。

下面介绍通过AOP实现接口请求日志的功能。

<!--more-->

### 引入依赖

```xml
<!--引入AOP依赖-->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

### 日志切面

- 使用@Aspect注解将一个java类定义为切面类
- 使用@Pointcut定义一个切入点，可以是一个规则表达式，比如下例中某个package下的所有函数，也可以是一个注解等。
- 根据需要在切入点不同位置的切入内容
  - 使用@Before在切入点开始处切入内容
  - 使用@After在切入点结尾处切入内容
  - 使用@AfterReturning在切入点return内容之后切入内容（可以用来对处理返回值做一些加工处理）
  - 使用@Around在切入点前后切入内容，并自己控制何时执行切入点自身的内容
  - 使用@AfterThrowing用来处理当切入内容部分抛出异常之后的处理逻辑

### 实现代码

```java
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.stereotype.Component;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import javax.servlet.http.HttpServletRequest;
import java.util.Enumeration;

@Slf4j // 日志打印
@Component // 将对象交由spring进行管理
@Aspect // 代表此类为一个切面类
public class ControllerAopInterceptor {
 
    @Pointcut("execution(public * com.jue.*.controller.*.*(..))")
    public void privilege() {
    }
 
    @Around("privilege()")
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        String className = pjp.getTarget().getClass().getName(); // 获取类名
        String methodName = pjp.getSignature().getName(); // 获取执行的方法名称
        String[] parameterNamesArgs = ((MethodSignature) pjp.getSignature()).getParameterNames(); // 获取参数名称
        Object result = null; // 定义返回参数
        Object[] args = pjp.getArgs(); // 获取方法参数
        HttpServletRequest request = ((ServletRequestAttributes) RequestContextHolder.getRequestAttributes()).getRequest();
        // 请求的URL
        String requestURL = request.getRequestURL().toString();
        String ip = getIpAddr(request);
 
        StringBuffer paramsBuf = new StringBuffer();
        // 获取请求参数集合并进行遍历拼接
        for (int i = 0; i < args.length; i++) {
            if (paramsBuf.length() > 0) {
                paramsBuf.append("|");
            }
            paramsBuf.append(parameterNamesArgs[i]).append(" = ").append(args[i]);
        }
        StringBuffer headerBuf = new StringBuffer();
        Enumeration<String> headerNames = request.getHeaderNames();
        while (headerNames.hasMoreElements()) {
            String key = (String) headerNames.nextElement();
            String value = request.getHeader(key);
            if (headerBuf.length() > 0) {
                headerBuf.append("|");
            }
            headerBuf.append(key).append("=").append(value);
        }
 
        // 打印请求参数参数
        long start = System.currentTimeMillis();// 记录开始时间
        log.info("请求| ip:{} | 请求接口:{} | 请求类:{} | 方法 :{} | 参数:{} | 请求header:{}|请求时间 :{}", ip, requestURL, className, methodName, paramsBuf.toString(), headerBuf.toString(), start);
        result = pjp.proceed();// 执行目标方法
        // 获取执行完的时间 打印返回报文
        log.info("返回| 请求接口:{}| 方法 :{} | 请求时间:{} | 处理时间:{} 毫秒 | 返回结果 :{}", requestURL, methodName, start, (System.currentTimeMillis() - start), result);
        return result;
    }
 
    /**
     * @Description: 获取ip
     */
    public String getIpAddr(HttpServletRequest request) {
        String ipAddress = null;
        ipAddress = request.getHeader("x-forwarded-for");
        if (ipAddress == null || ipAddress.length() == 0 || "unknown".equalsIgnoreCase(ipAddress)) {
            ipAddress = request.getHeader("Proxy-Client-IP");
        }
        if (ipAddress == null || ipAddress.length() == 0 || "unknown".equalsIgnoreCase(ipAddress)) {
            ipAddress = request.getHeader("WL-Proxy-Client-IP");
        }
        if (ipAddress == null || ipAddress.length() == 0 || "unknown".equalsIgnoreCase(ipAddress)) {
            ipAddress = request.getRemoteAddr();
        }
        // 对于通过多个代理的情况，第一个IP为客户端真实IP,多个IP按照','分割
        if (ipAddress != null && ipAddress.length() > 15) { // "***.***.***.***".length()
            // = 15
            if (ipAddress.indexOf(",") > 0) {
                ipAddress = ipAddress.substring(0, ipAddress.indexOf(","));
            }
        }
        // 或者这样也行,对于通过多个代理的情况，第一个IP为客户端真实IP,多个IP按照','分割
        return ipAddress;
    }
}
```

