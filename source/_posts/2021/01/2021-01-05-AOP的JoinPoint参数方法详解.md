---
title: AOP的JoinPoint参数方法详解
layout: info
commentable: true
date: 2021-01-05
mathjax: true
mermaid: true
tags: [Java,Spring,AOP]
categories: 
- [Java,Spring]
- [Java,JavaClass]
description: 
---
### 重要方法

```java
        /*获取参数的值数组*/
        Object[] args = point.getArgs();                                    //  [1] 参数的值

        /*获取目标对象(被加强的对象)*/
        Object target = point.getTarget();

        /*获取signature 该注解作用在方法上，强转为 MethodSignature*/
        MethodSignature signature = (MethodSignature) point.getSignature();

        /*方法名*/
        String signatureName = signature.getName();                         //  findById

        /*参数名称数组(与args参数值意义对应)*/
        String[] parameterNames = signature.getParameterNames();            //  [i] 参数名称

        /*获取执行的方法对应Method对象*/
        Method method = signature.getMethod();                              
        //  public void com.jueee.test.service.UserService.findById(int)

        /*获取返回值类型*/
        Class returnType = signature.getReturnType();                       //  void

        /*获取方法上的注解*/
        OperationLog operationLog = method.getDeclaredAnnotation(OperationLog.class);
```

### request / response

```java
// 获取request/response(ThreadLocal模式)
RequestAttributes requestAttributes = RequestContextHolder.getRequestAttributes();
ServletRequestAttributes servletRequestAttributes = (ServletRequestAttributes) requestAttributes;
HttpServletRequest request = servletRequestAttributes.getRequest();
HttpServletResponse response = servletRequestAttributes.getResponse();
HttpSession session = request.getSession();
```