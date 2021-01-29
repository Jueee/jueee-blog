---
title: Spring AOP 拦截注解接口的所有方法
layout: info
commentable: true
date: 2021-01-29
mathjax: true
mermaid: true
tags: [Java,Spring,AOP]
categories: 
- [Java,Spring]
description: 
---

### 背景

MyBatis多源数据库切换问题，希望通过注解标注Dao类的数据库源，但使用注解切点表达式，因实现类是MyBatis动态代理生成，无法在实现类上添加注解，而添加到接口上又无效，需要寻找替代方案。

<!--more-->

### 解决方案

不采用AspectJ表达式方式定义切点和切面，使用 AnnotationMatchingPointcut 和 DefaultPointcutAdvisor 来定义。

### 实现方式

示例代码如下，将 ChangeMySqlType 注解添加到接口上，即可拦截实现类的方法。

#### 类注解

```java
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface ChangeMySqlType {

}
```

#### Aspect 实现

```java
import lombok.extern.slf4j.Slf4j;
import org.aopalliance.aop.Advice;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.aop.Advisor;
import org.springframework.aop.Pointcut;
import org.springframework.aop.support.DefaultPointcutAdvisor;
import org.springframework.aop.support.annotation.AnnotationMatchingPointcut;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Slf4j
@Aspect
@Component
@Order(2)
public class ChangeMySqlTypeAspect {

    @Autowired
    DataBasesConfig dataBasesConfig;

    @Bean
    public Advisor dataSourceAdvisor(){
        Pointcut pointcut = new AnnotationMatchingPointcut(ChangeMySqlType.class, true);
        Advice advice = new MethodAroundAdvice(dataBasesConfig);
        return new DefaultPointcutAdvisor(pointcut, advice);
    }
}
```

#### Advice 实现

```java
import lombok.extern.slf4j.Slf4j;
import org.springframework.aop.AfterReturningAdvice;
import org.springframework.aop.MethodBeforeAdvice;
import org.springframework.stereotype.Component;

import java.lang.reflect.Method;

@Slf4j
@Component
public class MethodAroundAdvice implements MethodBeforeAdvice, AfterReturningAdvice {

    private DataBasesConfig dataBasesConfig;

    public MethodAroundAdvice(DataBasesConfig dataBasesConfig){
        this.dataBasesConfig = dataBasesConfig;
    }

    @Override
    public void before(Method method, Object[] args, Object target) throws Throwable {
        log.info("before {} called", method.getName());
    }

    @Override
    public void afterReturning(Object returnValue, Method method, Object[] args, Object target) throws Throwable {
        log.info("after {} called", method.getName());
    }
}
```

