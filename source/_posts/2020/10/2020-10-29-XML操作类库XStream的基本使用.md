---
title: XML操作类库XStream的基本使用
layout: info
commentable: true
date: 2020-10-29
mathjax: true
mermaid: true
tags: [Java,JavaJar,XML]
categories: [Java,JavaJar]
description: 
---

### XStream 介绍

XStream是一个简单的基于Java库，Java对象序列化到XML，反之亦然(即：可以轻易的将Java对象和xml文档相互转换)。

- 官网说明：http://x-stream.github.io/
- GitHub：https://github.com/x-stream/xstream
- JavaDoc：http://x-stream.github.io/javadoc/index.html

<!--more-->

#### XStream 特点

-	**使用方便** - XStream的API提供了一个高层次外观，以简化常用的用例。
-	**无需创建映射** - XStream的API提供了默认的映射大部分对象序列化。
-	**性能** - XStream快速和低内存占用，适合于大对象图或系统。
-	**干净的XML** - XStream创建一个干净和紧凑XML结果，这很容易阅读。
-	**不需要修改对象** - XStream可序列化的内部字段，如私有和最终字段，支持非公有制和内部类。默认构造函数不是强制性的要求。
-	**完整对象图支持** - XStream允许保持在对象模型中遇到的重复引用，并支持循环引用。
-	**可自定义的转换策略** - 定制策略可以允许特定类型的定制被表示为XML的注册。
-	**安全框架** - XStream提供了一个公平控制有关解组的类型，以防止操纵输入安全问题。
-	**错误消息** - 出现异常是由于格式不正确的XML时，XStream抛出一个统一的例外，提供了详细的诊断，以解决这个问题。
-	**另一种输出格式** - XStream支持其它的输出格式，如JSON。

#### XStream 引入

```xml
<!-- https://mvnrepository.com/artifact/com.thoughtworks.xstream/xstream -->
<dependency>
    <groupId>com.thoughtworks.xstream</groupId>
    <artifactId>xstream</artifactId>
    <version>1.4.13</version>
</dependency>
```

### XStream 基本使用

#### 基本使用

1. **创建XStream对象**：通过它传递一个StaxDriver创建XStream对象。

   StaxDriver使用SAX解析器(可从Java6)，一个快速的XML解析器。

   ```java
   XStream xstream = new XStream(new StaxDriver());
   ```

2. **序列化对象到XML**：使用toXML() 方法来获取对象的XML字符串表示。

   ```java
   String xml = xstream.toXML(student);
   ```

3. **反序列化XML获得对象**：使用 fromXML()方法来从XML对象。

   ```java
   Student student1 = (Student)xstream.fromXML(xml);
   ```

#### 对象 到 XML 的转换

```java
XStream xstream1 = new XStream(new StaxDriver());
String xml = xstream1.toXML(student);
System.out.println(xml);
System.out.println(formatXml(xml));
```

#### XML 到 对象 的转换

```java
XStream xstream2 = new XStream();
Student student1 = (Student) xstream2.fromXML(xml);
System.out.println(student1);
```

此时，能够正常打印，但会提示异常：

> Security framework of XStream not explicitly initialized, using predefined black list on your own risk.

解决方案有两种：

1. 限制为所需的最小权限：

   ```java
   XStream xstream2 = new XStream();
   XStream.setupDefaultSecurity(xstream2);
   Class<?>[] classes = new Class[] { Student.class };
   xstream2.allowTypes(classes);
   Student student1 = (Student) xstream2.fromXML(xml);
   System.out.println(student1);
   ```

2. 消除所有限制：

   ```java
   XStream xstream3 = new XStream();
   xstream3.addPermission(AnyTypePermission.ANY);
   Student student2 = (Student) xstream3.fromXML(xml);
   System.out.println(student2);
   ```

参考资料：http://x-stream.github.io/security.html

#### 格式化 XML 字符串

```java
public static String formatXml(String xml) {
	try {
		Transformer serializer = SAXTransformerFactory.newInstance().newTransformer();
		serializer.setOutputProperty(OutputKeys.INDENT, "yes");
		serializer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
		Source xmlSource = new SAXSource(new InputSource(new ByteArrayInputStream(xml.getBytes())));
		StreamResult res = new StreamResult(new ByteArrayOutputStream());
		serializer.transform(xmlSource, res);
		return new String(((ByteArrayOutputStream) res.getOutputStream()).toByteArray());
	} catch (Exception e) {
		return xml;
	}
}
```

### XStream 混叠

混叠是一种技术来定制生成XML或者使用XStream特定的格式化XML。

#### 类混叠

类混叠是用来创建一个类的XML完全限定名称的别名。

```java
xstream.alias("student", Student.class);
xstream.alias("note", Note.class);
```

#### 字段混叠

字段混叠用于创建以XML字段的别名。

```java
xstream.aliasField("name", Student.class, "studentName");
```

#### 隐式集合混叠

隐式集合混叠时使用的集合是表示在XML无需显示根。

例如，我们需要一个接一个，但不是在根节点来显示每一个节点。

```java
xstream.addImplicitCollection(Student.class, "notes");
```

#### 属性混叠

属性混叠用于创建一个成员变量作为XML属性序列化。

```java
xstream.useAttributeFor(Student.class, "studentName");
```

#### 包混叠

包装混叠用于创建一个类XML的完全限定名称的别名到一个新的限定名称。

```java
xstream.aliasPackage("my.company.xstream", "demo.xstream");
```

### XStream 注解

```java
@XStreamAlias("student") // 类混叠
class Student {

	@XStreamAlias("name") // 字段混叠
	@XStreamAsAttribute // 属性混叠
	private String studentName;

	@XStreamImplicit // 隐式集合混叠
	private List<Note> notes = new ArrayList<Note>();

    @XStreamOmitField // 忽略不属于 XML 的字段
    private int type;
}
```

### XStream 对象流

XStream提供java.io.ObjectInputStream和java.io.ObjectOutputStream替代实现，使对象流可以被序列化或XML序列化。

#### 输出文件 Output

```java
ObjectOutputStream objectOutputStream = xstream.createObjectOutputStream(new FileOutputStream("test.txt"));
objectOutputStream.writeObject(student1);
objectOutputStream.writeObject(student2);
objectOutputStream.writeObject(student3);
objectOutputStream.writeObject(student4);
objectOutputStream.writeObject("Hello World");
objectOutputStream.close();
```

#### 读取文件 Input

```java
ObjectInputStream objectInputStream = xstream.createObjectInputStream(new FileInputStream("test.txt"));
Student student5 = (Student) objectInputStream.readObject();
Student student6 = (Student) objectInputStream.readObject();
Student student7 = (Student) objectInputStream.readObject();
Student student8 = (Student) objectInputStream.readObject();
String text = (String) objectInputStream.readObject();
```

### XStream 自定义转换器

XStream允许从无到有写入转换器，这样开发人员可以编写一个完全新的实现，如何对象序列化到XML，反之亦然。 转换器接口提供了三种方法。

- **canConvert** - 检查支持的对象类型的序列化。
- **marshal** - 序列化对象到XML。
- **unmarshal** - 从XML对象反序列化

#### 实现转换器接口

```java
class StudentConverter implements Converter {
	// 序列化对象到XML
	@Override
	public void marshal(Object value, HierarchicalStreamWriter writer, MarshallingContext context) {
		Student student = (Student) value;
		writer.startNode("name");
		writer.setValue(student.getName().getFirstName() + "," + student.getName().getLastName());
		writer.endNode();
	}
	// 从XML对象反序列化
	@Override
	public Object unmarshal(HierarchicalStreamReader reader, UnmarshallingContext context) {
		reader.moveDown();
		String[] nameparts = reader.getValue().split(",");
		Student student = new Student(nameparts[0], nameparts[1]);
		reader.moveUp();
		return student;
	}
	// 检查支持的对象类型的序列化
	@Override
	public boolean canConvert(Class object) {
		return object.equals(Student.class);
	}
} 
```

#### 注册转换器

```java
xstream.registerConverter(new StudentConverter());
```

### XStream 编写JSON

XStream支持JSON通过初始化XStream对象适当的驱动程序。 

XStream目前支持JettisonMappedXmlDriver和JsonHierarchicalStreamDriver。

```java
XStream xstream = new XStream(new JsonHierarchicalStreamDriver() {
	public HierarchicalStreamWriter createWriter(Writer writer) {
		return new JsonWriter(writer, JsonWriter.DROP_ROOT_MODE);
	}
});
xstream.setMode(XStream.NO_REFERENCES);
Student student = new Student("Mahesh");
System.out.println(xstream.toXML(student));
```

### 参考资料

- https://www.yiibai.com/xstream