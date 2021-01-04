---
title: SpringBoot用AOP切面实现权限校验
layout: info
commentable: true
date: 2021-01-02
mathjax: true
mermaid: true
tags: [Java,Spring,AOP]
categories: 
- [Java,Spring]
- [Java,SpringBoot]
description: 
---

使用 AOP，首先需要引入 **AOP 的依赖**。

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

<!--more-->

### 截获Get请求

在所有的`get`请求被调用前在控制台输出一句"get请求的advice触发了"。

#### 创建AOP切面类

创建一个AOP切面类，只要在类上加个 `@Aspect` 注解即可。

- `@Aspect` 注解用来描述一个切面类，定义切面类的时候需要打上这个注解。
- `@Component` 注解将该类交给 Spring 来管理。

```java
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class LogAdvice {
    // 定义一个切点：所有被GetMapping注解修饰的方法会织入advice
    @Pointcut("@annotation(org.springframework.web.bind.annotation.GetMapping)")
    private void logAdvicePointcut() {}

    // Before表示logAdvice将在目标方法执行前执行
    @Before("logAdvicePointcut()")
    public void logAdvice(){
        // 这里只是一个示例，你可以写任何处理逻辑
        System.out.println("get请求的advice触发了");
    }
}
```

#### 创建接口类

创建一个接口类，内部创建一个get请求：

```java
@RestController
@RequestMapping(value = "/aop")
public class AopController {
    @GetMapping(value = "/getTest")
    public JSONObject aopTest() {
        return JSON.parseObject("{\"message\":\"SUCCESS\",\"code\":200}");
    }

    @PostMapping(value = "/postTest")
    public JSONObject aopTest2(@RequestParam("id") String id) {
        return JSON.parseObject("{\"message\":\"SUCCESS\",\"code\":200}");
    }
}
```

#### 请求接口

项目启动后，请求`http://localhost:8080/aop/getTest`接口：

![image-20201231112432589](/images/2021/01/image-20201231112432589.png)

### 截获权限校验注解

#### 自定义注解

自定义一个注解`PermissionsAnnotation`

```java
import java.lang.annotation.*;

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface PermissionAnnotation{
}
```

#### 创建切面类

创建一个切面类，切点设置为拦截所有标注`PermissionsAnnotation`的方法，截取到接口的参数，进行简单的权限校验。

- `@Aspect` 注解用来描述一个切面类，定义切面类的时候需要打上这个注解。
- `@Component` 注解将该类交给 Spring 来管理。
- `@Order`注解管理切面类执行顺序，该注解后的数字越小，所在切面类越先执行。

```java
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Slf4j
@Aspect
@Component
@Order(1)
public class PermissionFirstAdvice {

    // 定义一个切面，括号内写入第1步中自定义注解的路径
    @Pointcut("@annotation(com.jueee.annotation.PermissionAnnotation)")
    private void permissionCheck() {
    }

    @Around("permissionCheck()")
    public Object permissionCheckFirst(ProceedingJoinPoint joinPoint) throws Throwable {
        System.out.println("===================权限切面===================：" + System.currentTimeMillis());

        //获取请求参数，详见接口类
        Object[] objects = joinPoint.getArgs();
        Long id = ((JSONObject) objects[0]).getLong("id");
        String name = ((JSONObject) objects[0]).getString("name");
        System.out.println("id->>>>>>>>>>>>>>>>>>>>>>" + id);
        System.out.println("name->>>>>>>>>>>>>>>>>>>>>>" + name);

        // name不是管理员则抛出异常
        if (!name.equals("admin")) {
            return JSON.parseObject("{\"message\":\"not admin\",\"code\":403}");
        }
        return joinPoint.proceed();
    }

}
```

#### 创建接口类

创建接口类，并在目标方法上标注自定义注解 `PermissionsAnnotation`：

```java
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.jueee.annotation.PermissionAnnotation;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping(value = "/permission")
public class TestController {

    @RequestMapping(value = "/check", method = RequestMethod.POST)
    @PermissionAnnotation()  // 添加这个注解
    public JSONObject getGroupList(@RequestBody JSONObject request) {
        return JSON.parseObject("{\"message\":\"SUCCESS\",\"code\":200,\"data\":" + request + "}");
    }
}
```

#### 请求接口

有权限请求：

```java
JSONObject jsonObject = new JSONObject();
jsonObject.put("id",11);
jsonObject.put("name","admin");
String result = HttpClient4.doPost("http://localhost:8080/permission/check",jsonObject.toString());
log.info(result); // {"code":200,"data":{"name":"admin","id":11},"message":"SUCCESS"}
```

无权限请求：

```java
JSONObject jsonObject = new JSONObject();
jsonObject.put("id",23);
jsonObject.put("name","jueee");
String result = HttpClient4.doPost("http://localhost:8080/permission/check",jsonObject.toString());
log.info(result); // {"code":403,"message":"not admin"}
```

