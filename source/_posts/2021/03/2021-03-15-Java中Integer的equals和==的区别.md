---
title: Java中Integer的equals和==的区别
layout: info
commentable: true
date: 2021-03-15
mathjax: true
mermaid: true
tags: [Java,JavaClass]
categories: [Java,JavaClass]
description: 
---

近期在 `Map<String,Integer>` 进行计数比较时，发现 Integer 比较有问题，让我们进行下探究。

如：

```java
Integer a = 281;
Integer b = 281;
assertFalse(a==b);
```

<!--more-->

### equals 比较

equals(Object obj)方法，在equals(Object obj)方法中，会先判断参数中的对象obj是否是Integer同类型的对象，如果是则判断值是否相同，值相同则返回true，值不同则返回false，如果obj不是Integer类的对象，则返回false。

需要注意的是：当参数是基本类型int时，编译器会给int自动装箱成Integer类，然后再进行比较。

1. 基本类型(值类型)之间无法使用equals比较。
2. equals参数为值类型，则参数会进行自动装箱为包装类型进行比较。
3. equals参数为包装类型，则先比较是否为同类型，非同类型直接返回false，同类型再比较值。

示例：

```java
//为 false，equals参数默认为int类型，装箱为Integer类型，不同类型直接返回false
assertFalse(new Long(0).equals(0)); 

//为 true，equals参数默认为int类型，装箱为Integer类型，相同类型再比较值返回true
assertTrue(new Integer(500).equals(500)); 

//为 false，equals参数为byte类型，装箱为Byte类型，不同类型直接返回false
assertFalse(new Integer(500).equals((short)500)); 

//为 true，equals参数为long类型，装箱为Long类型，相同类型再比较值返回true
assertTrue(new Long(0).equals(0L)); 
```

### ==比较

1. 基本类型之间互相比较：以值进行比较
2. 一边是基本类型，一边是包装类型
   1. 同类型的进行比较，如Integer 与int，Long与long进行==比较时，会自动拆箱比较值
   2. 不同类型之间进行比较，则会自动拆箱，且会进行自动向上转型再比较值（低级向高级是隐式类型转换如：byte<short<int<long<float<double，高级向低级必须强制类型转换）
3. 两边都是包装类型则直接比较引用地址，但是要注意IntegerCache除外。

### IntegerCache 缓存

JAVA的Integer有IntegerCache会缓存-128~127之间的对象。

Integer 类的源码中的 IntegerCache 子类如下：

![image-20210315174612801](/images/2021/03/image-20210315174612801.png)

如：Integer x = 100，会调用Integer的valueOf()方法，这个方法就是返回一个Integer对象，但是在返回前，作了一个判断，判断要赋给对象的值是否在[-128,127]区间中，且 IntegerCache（是Integer类的内部类，里面有一个Integer对象数组，用于存放已经存在的且范围在[-128,127]中的对象）中是否存在此对象，如果存在，则直接返回引用，否则，创建一个新对象返回。

Integer 类的valueOf()方法的源码如下：

![image-20210315174709788](/images/2021/03/image-20210315174709788.png)

当 Integer 在 [-128,127] 范围时：

```java
Integer a = 81;
Integer b = 81;
assertTrue(a==b); //true 因为59位于缓存区间直接从缓存中获取
```

当 Integer 不在 [-128,127] 范围时：

```java
Integer a = 281;
Integer b = 281;
assertFalse(a==b); //false 因为281超出缓存区间从新创建对象
assertTrue(a.intValue()==b.intValue()); //true 需要 intValue() 转换为 int 进行==比较
```

