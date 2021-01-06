---
title: Spring面向切面编程AOP介绍及注解
layout: info
commentable: true
date: 2021-01-01
mathjax: true
mermaid: true
tags: [Java,Spring,AOP]
categories: 
- [Java,Spring]
description: 
---

### Spring AOP

**AOP 即 Aspect Oriented Program 面向切面编程**。

首先，在面向切面编程的思想里面，把功能分为核心业务功能，和周边功能。

- **所谓的核心业务**，比如登陆，增加数据，删除数据都叫核心业务
- **所谓的周边功能**，比如性能统计，日志，事务管理等等

周边功能在 Spring 的面向切面编程AOP思想里，即被定义为切面。

在面向切面编程AOP的思想里面，核心业务功能和切面功能分别独立进行开发，然后把切面功能和核心业务功能 "编织" 在一起，这就叫AOP。

<!--more-->

#### AOP 的目的

AOP能够将那些与业务无关，却为业务模块所共同调用的逻辑或责任（例如事务处理、日志管理、权限控制等）封装起来，便于减少系统的重复代码，降低模块间的耦合度，并有利于未来的可拓展性和可维护性。

#### AOP术语

- **连接点（Joinpoint)** 程序执行的某个特定位置，如某个方法调用前，调用后，方法抛出异常后，这些代码中的特定点称为连接点。简单来说，就是在哪加入你的逻辑增强
  连接点表示具体要拦截的方法，上面切点是定义一个范围，而连接点是具体到某个方法

- **切点（PointCut）** 每个程序的连接点有多个，如何定位到某个感兴趣的连接点，就需要通过切点来定位。比如，连接点--数据库的记录，切点--查询条件
  切点用于来限定Spring-AOP启动的范围，通常我们采用表达式的方式来设置，所以关键词是范围

- **业务增强（Advice）** 业务增强是织入到目标类连接点上的一段程序代码。

  业务增强分为如下几种：

  - **前置通知(before)**:在执行业务代码前做些操作，比如获取连接对象
  - **后置通知(after)**:在执行业务代码后做些操作，无论是否发生异常，它都会执行，比如关闭连接对象
  - **异常通知（afterThrowing）**:在执行业务代码后出现异常，需要做的操作，比如回滚事务
  - **返回通知(afterReturning)**,在执行业务代码后无异常，会执行的操作
  - **环绕通知(around)**，在执行业务代码前和执行业务代码后都会执行的操作

- **目标对象（Target）** 需要被加强的业务对象

- **织入（Weaving）** 织入就是将增强添加到对目标类具体连接点上的过程。
  织入是一个形象的说法，具体来说，就是生成代理对象并将切面内容融入到业务流程的过程。

- **代理类（Proxy）** 一个类被AOP织入增强后，就产生了一个代理类。

- **切面（Aspect）** 切面由切点和增强组成，它既包括了横切逻辑的定义，也包括了连接点的定义，SpringAOP就是将切面所定义的横切逻辑织入到切面所制定的连接点中。

### AOP 体系

![image-20201231111624405](/images/2021/01/image-20201231111624405.png)

### AOP 相关注解

#### @Pointcut

`@Pointcut` 注解，用来定义一个切面，即上文中所关注的某件事情的入口，切入点定义了事件触发时机。

有两个常用的表达式：

##### execution() 表达式

```java
/**
 * 定义一个切面，拦截 com.jueee.controller 包和子包下的所有方法
 */
@Pointcut("execution(* com.jueee.controller..*.*(..))")
public void pointCut() {}
```

以 `execution(* * com.jueee.controller..*.*(..)))` 表达式为例：

- 第一个 * 号的位置：表示返回值类型，* 表示所有类型。
- 包名：表示需要拦截的包名，后面的两个句点表示当前包和当前包的所有子包，在本例中指 com.mutest.controller包、子包下所有类的方法。
- 第二个 * 号的位置：表示类名，* 表示所有类。
- *(..)：这个星号表示方法名，* 表示所有的方法，后面括弧里面表示方法的参数，两个句点表示任何参数。

##### annotation() 表达式

`annotation()` 方式是针对某个注解来定义切面，比如我们对具有 @PostMapping 注解的方法做切面，可以如下定义切面：

```java
@Pointcut("@annotation(org.springframework.web.bind.annotation.GetMapping)")
private void logAdvicePointcut() {}
```

然后使用该切面的话，就会切入注解是 `@PostMapping` 的所有方法。

这种方式很适合处理 `@GetMapping、@PostMapping、@DeleteMapping`不同注解有各种特定处理逻辑的场景。

#### @Around

`@Around`注解用于修饰`Around`增强处理，`Around`增强处理非常强大，表现在：

1. `@Around`可以自由选择增强动作与目标方法的执行顺序，也就是说可以在增强动作前后，甚至过程中执行目标方法。这个特性的实现在于，调用`ProceedingJoinPoint`参数的`procedd()`方法才会执行目标方法。
2. `@Around`可以改变执行目标方法的参数值，也可以改变执行目标方法之后的返回值。

`Around`增强处理有以下特点：

1. 当定义一个`Around`增强处理方法时，该方法的第一个形参必须是 `ProceedingJoinPoint` 类型（至少一个形参）。在增强处理方法体内，调用`ProceedingJoinPoint`的`proceed`方法才会执行目标方法：这就是`@Around`增强处理可以完全控制目标方法执行时机、如何执行的关键；如果程序没有调用`ProceedingJoinPoint`的`proceed`方法，则目标方法不会执行。
2. 调用`ProceedingJoinPoint`的`proceed`方法时，还可以传入一个`Object[ ]`对象，该数组中的值将被传入目标方法作为实参——这就是`Around`增强处理方法可以改变目标方法参数值的关键。这就是如果传入的`Object[ ]`数组长度与目标方法所需要的参数个数不相等，或者`Object[ ]`数组元素与目标方法所需参数的类型不匹配，程序就会出现异常。

`@Around`功能虽然强大，但通常需要在线程安全的环境下使用。

因此，如果使用普通的`Before`、`AfterReturning`就能解决的问题，就没有必要使用`Around`了。如果需要目标方法执行之前和之后共享某种状态数据，则应该考虑使用`Around`。尤其是需要使用增强处理阻止目标的执行，或需要改变目标方法的返回值时，则只能使用`Around`增强处理了。

```java
@Aspect
@Component
@Slf4j
public class AroundAdvice {
    @Pointcut("@annotation(com.jueee.annotation.PermissionAnnotation)")
    private void permissionCheck() {
    }
    @Around("permissionCheck()")
    public Object permissionCheck(ProceedingJoinPoint joinPoint) throws Throwable {
        System.out.println("===================开始增强处理===================");
        //获取请求参数，详见接口类
        Object[] objects = joinPoint.getArgs();
        Long id = ((JSONObject) objects[0]).getLong("id");
        String name = ((JSONObject) objects[0]).getString("name");
        System.out.println("id1->>>>>>>>>>>>>>>>>>>>>>" + id);
        System.out.println("name1->>>>>>>>>>>>>>>>>>>>>>" + name);
        // 修改入参
        JSONObject object = new JSONObject();
        object.put("id", 8);
        object.put("name", "lisi");
        objects[0] = object;
        // 将修改后的参数传入
        return joinPoint.proceed(objects);
    }
}
```

处理日志：

```
服务端：
===================开始增强处理===================
id1->>>>>>>>>>>>>>>>>>>>>>23
name1->>>>>>>>>>>>>>>>>>>>>>jueee

客户端：
{"code":200,"data":{"name":"lisi","id":8},"message":"SUCCESS"}
```

#### @Before

`@Before` 注解指定的方法在切面切入目标方法之前执行，可以做一些 `Log` 处理，也可以做一些信息的统计，比如获取用户的请求 `URL` 以及用户的 `IP` 地址等等，这个在做个人站点的时候都能用得到，都是常用的方法。

`JointPoint` 对象很有用，可以用它来获取一个签名，利用签名可以获取请求的包名、方法名，包括参数（通过 `joinPoint.getArgs()` 获取）等。如下示例：

```java
@Aspect
@Component
@Slf4j
public class BeforeAdvice {
    /**
     * 定义一个切面，拦截 com.mutest.controller 包下的所有方法
     */
    @Pointcut("execution(* com.jueee.controller..*.*(..))")
    public void pointCut() {}
    /**
     * 在上面定义的 pointCut() 切面方法之前执行该方法
     * @param joinPoint jointPoint
     */
    @Before("pointCut()")
    public void doBefore(JoinPoint joinPoint) {
        log.info("====doBefore方法进入了====");

        // 获取签名
        Signature signature = joinPoint.getSignature();
        // 获取切入的包名
        String declaringTypeName = signature.getDeclaringTypeName();
        // 获取即将执行的方法名
        String funcName = signature.getName();
        log.info("即将执行方法为: {}，属于{}包", funcName, declaringTypeName);

        // 也可以用来记录一些信息，比如获取请求的 URL 和 IP
        ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        HttpServletRequest request = attributes.getRequest();
        // 获取请求 URL
        String url = request.getRequestURL().toString();
        // 获取请求 IP
        String ip = request.getRemoteAddr();
        log.info("用户请求的url为：{}，ip地址为：{}", url, ip);
    }
}
```

输出日志：

```
: ====doBefore方法进入了====
: 即将执行方法为: getGroupList，属于com.jueee.controller.TestController包
: 用户请求的url为：http://localhost:8080/permission/check，ip地址为：127.0.0.1
```

#### @After

`@After` 注解和 `@Before` 注解相对应，指定的方法在切面切入目标方法之后执行，也可以做一些完成某方法之后的 Log 处理。

```java
@Aspect
@Component
@Slf4j
public class AfterAdvice {
    /**
     * 定义一个切面，拦截 com.mutest.controller 包下的所有方法
     */
    @Pointcut("execution(* com.jueee.controller..*.*(..))")
    public void pointCut() {}
    /**
     * 在上面定义的切面方法之后执行该方法
     * @param joinPoint jointPoint
     */
    @After("pointCut()")
    public void doAfter(JoinPoint joinPoint) {
        log.info("==== doAfter 方法进入了====");
        Signature signature = joinPoint.getSignature();
        String method = signature.getName();
        log.info("方法{}已经执行完", method);
    }
}
```

输出日志：

```java
: ==== doAfter 方法进入了====
: 方法getGroupList已经执行完
```

#### @AfterReturning

`@AfterReturning` 注解和 `@After` 有些类似，区别在于 `@AfterReturning` 注解可以用来捕获切入方法执行完之后的返回值，对返回值进行业务逻辑上的增强处理，例如：

```java
@Aspect
@Component
@Slf4j
public class AfterReturningAdvice {
    /**
     * 定义一个切面，拦截 com.mutest.controller 包下的所有方法
     */
    @Pointcut("execution(* com.jueee.controller..*.*(..))")
    public void pointCut() {}
    /**
     * 在上面定义的切面方法返回后执行该方法，可以捕获返回对象或者对返回对象进行增强
     * @param joinPoint joinPoint
     * @param result result
     */
    @AfterReturning(pointcut = "pointCut()", returning = "result")
    public void doAfterReturning(JoinPoint joinPoint, Object result) {
        Signature signature = joinPoint.getSignature();
        String classMethod = signature.getName();
        log.info("方法{}执行完毕，返回参数为：{}", classMethod, result);
        // 实际项目中可以根据业务做具体的返回值增强
        log.info("对返回参数进行业务上的增强：{}", result + "增强版");
    }
}
```

日志如下：

```
: 方法getGroupList执行完毕，返回参数为：{"code":200,"message":"SUCCESS"}
: 对返回参数进行业务上的增强：{"code":200,"message":"SUCCESS"}增强版
```

#### @AfterThrowing

当被切方法执行过程中抛出异常时，会进入 `@AfterThrowing` 注解的方法中执行，在该方法中可以做一些异常的处理逻辑。

要注意的是 `throwing` 属性的值必须要和参数一致，否则会报错。

该方法中的第二个入参即为抛出的异常。

```java
@Aspect
@Component
@Slf4j
public class AfterThrowingAdvice {
    /**
     * 定义一个切面，拦截 com.mutest.controller 包下的所有方法
     */
    @Pointcut("execution(* com.jueee.controller..*.*(..))")
    public void pointCut() {}
    /**
     * 在上面定义的切面方法执行抛异常时，执行该方法
     * @param joinPoint jointPoint
     * @param ex ex
     */
    @AfterThrowing(pointcut = "pointCut()", throwing = "ex")
    public void afterThrowing(JoinPoint joinPoint, Throwable ex) {
        Signature signature = joinPoint.getSignature();
        String method = signature.getName();
        // 处理异常的逻辑
        log.info("执行方法{}出错，异常为：{}", method, ex);
    }
}
```

