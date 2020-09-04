---
title: 关于toString方法的重写工具ToStringBuilder
layout: info
commentable: true
date: 2020-07-06
mathjax: true
mermaid: true
tags: [JavaClass,Apache]
categories: 
-	[Java,JavaClass]
description: apache的commons-lang3的工具包里有一个ToStringBuilder类，这样在打日志的时候可以方便的打印出类实例中的各属性的值。

---

Apache 的 `commons-lang3` 的工具包里有一个 `ToStringBuilder` 类，这样在打日志的时候可以方便的打印出类实例中的各属性的值。

### 依赖引入

```xml
<dependency>
    <groupId>commons-lang</groupId>
    <artifactId>commons-lang</artifactId>
    <version>2.4</version>
</dependency>
```

### 重写 toString

```java
@Override
public String toString() {
	return ToStringBuilder.reflectionToString(this);
}
```

打印结果参考：

> com.zzz.other.City@4eec7777[id=1,name=杭州,province=浙江,country=CN]

### ToStringStyle

`ToStringBuilder.reflectionToString`  默认为 `ToStringStyle.DEFAULT_STYLE`。

使用方法：

```
ToStringBuilder.reflectionToString(this, ToStringStyle.DEFAULT_STYLE);
```

ToStringStyle 还有其他样式，可调整 ToStringBuilder 的打印结果：

- **ToStringStyle.DEFAULT_STYLE**：对象及其属性一行显示

  ```
  com.zzz.other.City@4eec7777[id=1,name=杭州,province=浙江,country=CN]
  ```
  
- **ToStringStyle.MULTI_LINE_STYLE**：属性换行显示

  ```
  com.zzz.other.City@4eec7777[
    id=1
    name=杭州
    province=浙江
    country=CN
  ]
  ```
  
- **ToStringStyle.NO_FIELD_NAMES_STYLE**：不显示属性名，只显示属性值

  ```
  com.zzz.other.City@4eec7777[1,杭州,浙江,CN]
  ```

- **ToStringStyle.SHORT_PREFIX_STYLE**：对象名称简写

  ```
  City[id=1,name=杭州,province=浙江,country=CN]
  ```
- **ToStringStyle.SIMPLE_STYLE**：只显示属性

  ```
  1,杭州,浙江,CN
  ```

### 原理解析

`ReflectionToStringBuilder` 主要是通过java 反射实现的属性拼接。

**org.apache.commons.lang.builder.ReflectionToStringBuilder**：


 ```java
public static String toString(Object object, ToStringStyle style, 
                              boolean outputTransients, boolean outputStatics,
                              Class reflectUpToClass) {
	return new ReflectionToStringBuilder(object, style, null, 
                                         reflectUpToClass, outputTransients,
                                         outputStatics).toString();
}

public String toString() {
	if (this.getObject() == null) {
		return this.getStyle().getNullText();
	}
	Class clazz = this.getObject().getClass();
	this.appendFieldsIn(clazz);
	while (clazz.getSuperclass() != null && clazz != this.getUpToClass()) {
		clazz = clazz.getSuperclass();
		this.appendFieldsIn(clazz);
	}
	return super.toString();
}
 ```

其中参数  `ToStringStyle`  是个抽象类，定义了输出的格式 主要是 append了一类类信息到字符串上，可以自己继承 `ToStringStyle`  实现自定义的输出格式。