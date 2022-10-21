---
title: Spring的IOC容器管理对象示例
layout: info
commentable: true
date: 2021-01-03
mathjax: true
mermaid: true
tags: [Java,Spring,AOP]
categories: 
- [Java,Spring]
- [Java,SpringBoot]
description: 
---

### IOC 控制反转

IOC—Inversion of Control，即“控制反转”，不是什么技术，而是一种设计思想。

在Java开发中，IOC意味着将你设计好的对象交给容器控制，而不是传统的在你的对象内部直接控制。

所谓IOC，对于Spring框架来说，就是由Spring来负责控制对象的生命周期和对象间的关系。

Spring所倡导的开发方式就是如此，所有的类都会在Spring容器中登记。所有的类的创建、销毁都由 Spring来控制，也就是说控制对象生存周期的不再是引用它的对象，而是Spring。对于某个具体的对象而言，以前是它控制其他对象，现在是所有对象都被Spring控制，所以这叫控制反转。

<!--more-->

#### 理解 IOC

如何理解好IOC呢？理解好IOC的关键是要明确：

- 谁控制谁，控制什么？

  传统 Java SE 程序设计，我们直接在对象内部通过new进行创建对象，是程序主动去创建依赖对象；而 IOC 是有专门一个容器来创建这些对象，即由IOC容器来控制对 象的创建；谁控制谁？当然是IOC容器控制了对象；控制什么？那就是主要控制了外部资源获取（不只是对象包括比如文件等）。

- 为何是反转，哪些方面反转了？

  有反转就有正转，传统应用程序是由我们自己在对象中主动控制去直接获取依赖对象，也就是正转；而反转则是由容器来帮忙创建及注入依赖对象；为何是反转？因为由容器帮我们查找及注入依赖对象，对象只是被动的接受依赖对象，所以是反转；哪些方面反转了？依赖对象的获取被反转了。

### 对象示例

```java
public class HelloWorld {
    private String userName;

    public void setUserName(String userName) {
        this.userName = userName;
    }
    public String getUserName() {
        return userName;
    }
    public void sayHello(){
        System.out.println("Hello,"+userName);
    }
}
```

### 传统方式加载对象

```java
HelloWorld helloWorld=new HelloWorld();
helloWorld.setUserName("周杰伦");
helloWorld.sayHello();
```

### IOC 容器加载对象

#### 新建IOC配置文件

在resources目录下新建一个IOC的配置文件applicationContext.xml，等下需要通过这个配置文件去创建IOC容器。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
        http://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="helloWorld" class="com.jueee.bean.HelloWorld">
        <property name="userName" value="林俊杰"></property>
    </bean>
</beans>
```

#### IOC 普通方式加载

- BeanFactory：表示Spring IOC容器，专门生产bean对象的工厂，负责配置，创建和管理bean
- bean：被Spring IOC容器管理的对象都是bean，可以理解为Spring下皆为bean

```java
//1.从classpath路径去寻找配置文件，加载我们的配置
Resource resources= new ClassPathResource("applicationContext.xml");
//2.加载配置文件之后，创建IOC容器
BeanFactory factory=new XmlBeanFactory(resources);
//3.从Spring IOC容器中获取指定名称的对象
HelloWorld helloWorld= (HelloWorld) factory.getBean("helloWorld");
//--------------------IOC结束了---------------------
helloWorld.sayHello();
```

#### IOC 注解方式加载

- 先在测试类头上加个 @ContextConfiguration，意思是找到Spring容器，classpath就是resource目录
- @Autowired：表示自动按照类型去Spring容器中找到对应的Bean对象，然后自动注入

```java
@SpringBootTest
@ContextConfiguration("classpath:applicationContext.xml")
public class HelloWorldTest2 {

    @Autowired
    private HelloWorld helloWorld;

    @Test
    public void testHelloIOCNB(){
        helloWorld.sayHello();
    }
}
```

#### IOC 加载工作原理

IOC的工作原理，使用到的技术有两个，反射和内省。

如下示例所示：

```java
String className = "com.jueee.bean.HelloWorld";
//--------------------模拟IOC开始了-------------------
//1.使用反射创建对象
Class clzz = Class.forName(className);
Constructor con = clzz.getConstructor();
con.setAccessible(true);//设置构造器可访问性为true
Object obj = con.newInstance();

//2.使用内省机制获取所有的属性名称
BeanInfo beanInfo = Introspector.getBeanInfo(clzz, Object.class);
PropertyDescriptor[] pds = beanInfo.getPropertyDescriptors();

for (PropertyDescriptor pd : pds) {
    String propertyName = pd.getName();
    if ("userName".equals(propertyName)) {
        pd.getWriteMethod().invoke(obj, "陈奕迅");
    }
}
HelloWorld helloWorld = (HelloWorld) obj;
//--------------------模拟IOC结束了---------------------
helloWorld.sayHello();
```

### IOC的容器类型

#### BeanFactory

```java
//--------------------IOC开始了-------------------
//1.从classpath路径去寻找配置文件，加载我们的配置
Resource resources= new ClassPathResource("applicationContext.xml");
//2.加载配置文件之后，创建IOC容器
BeanFactory factory=new XmlBeanFactory(resources);
//3.从Spring IOC容器中获取指定名称的对象
HelloWorld helloWorld= (HelloWorld) factory.getBean(HelloWorld.class);
//--------------------IOC结束了---------------------
helloWorld.sayHello();
```

#### ApplicationContext

ApplicationContext这个其实是BeanFactory的一个子接口。

```java
//--------------------IOC开始了-------------------
ApplicationContext ctx=new ClassPathXmlApplicationContext("applicationContext.xml");
System.out.println("上面的代码已经创建Bean对象了，下面的获取Bean，获取已有的Bean");
HelloWorld helloWorld= ctx.getBean("helloWorld",HelloWorld.class);
//--------------------IOC结束了---------------------
helloWorld.sayHello();
```

### 加载Bean的方式

1. 根据Bean对象在容器中的id来获取。当有两个 id 重复时，就会报错。

   ```java
   HelloWorld helloWorld= (HelloWorld) factory.getBean("helloWorld");
   ```

2. 根据类型获取Bean。当两个bean的id不一样，class一样的时候，还是会报错，报类找到的Bean不是唯一的

   ```java
   HelloWorld helloWorld= (HelloWorld) factory.getBean(HelloWorld.class);
   ```

3. 根据id+类型来获取Bean，推荐方式。

   ```java
   HelloWorld helloWorld= ctx.getBean("helloWorld",HelloWorld.class);
   ```

### Bean的作用域

1. singltton:单例，在IOC容器中的Bean实例，都是唯一的

   ```java
   <bean id="helloWorld1" class="com.jueee.bean.HelloWorld" scope="singleton"></bean>
   ```

2. prototype:多例，在IOC容器中的Bean，每次都返回一个新的对象

   ```java
   <bean id="helloWorld2" class="com.jueee.bean.HelloWorld" scope="prototype"></bean>
   ```

### 配置文件的import导入

我们的applicationContext.xml里面写的是Bean，当项目里面多个需要控制反转的配置，如果都写在一个xml文件里，太大，也太乱。

所以我们可以分开写每个包里面写个自己的xml，然后applicationContext.xml直接import导入就可以了。

```xml
<!--导入其他的配置文件-->
<import resource="classpath:HelloWorld.xml"></import>
```

### Bean的初始化和销毁

1. 构建Bean

   ```java
   public class MyDataSource {
       public void open(){
           System.out.println(this + " 初始化");
       }
   
       public void dowork(){
           System.out.println(this + " 工作");
       }
   
       public void close(){
           System.out.println(this + " 销毁");
       }
   }
   ```

2. 配置 xml

   ```xml
   <bean id="myDataSource" class="com.jueee.bean.MyDataSource"  init-method="open" destroy-method="close"></bean>
   ```

3. 普通模式

   ```java
   MyDataSource myDataSource=new MyDataSource();
   myDataSource.open();
   myDataSource.dowork();
   myDataSource.close();
   ```

   输出：

   ```
   com.jueee.bean.MyDataSource@4ae33a11 初始化
   com.jueee.bean.MyDataSource@4ae33a11 工作
   com.jueee.bean.MyDataSource@4ae33a11 销毁
   ```

4. IOC 模式

   ```java
   @SpringBootTest
   @ContextConfiguration("classpath:applicationContext4.xml")
   public class MyDataSourceTest {
       
       @Autowired
       private MyDataSource myDataSource;
   
       //IOC容器的方式
       @Test
       public void test2(){
           myDataSource.dowork();
       }
   }
   ```

   输出（自动进行创建和销毁）：

   ![image-20201231164806006](/images/2021/01/image-20201231164806006.png)

   





