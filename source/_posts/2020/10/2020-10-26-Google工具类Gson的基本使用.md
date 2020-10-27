---
title: Google工具类Gson的基本使用
layout: info
commentable: true
date: 2020-10-26
mathjax: true
mermaid: true
tags: [Google,Java,JavaJar]
categories: [Java,JavaJar]
description: 
---

### Gson 介绍

Google Gson 是一个简单的基于Java的库，用于将Java对象序列化为JSON，反之亦然。 它是由Google开发的一个开源库。

以下几点说明为什么应该使用这个库 

- **标准化** - Gson是一个由Google管理的标准化库。
- **高效** - 这是对Java标准库的可靠，快速和高效的扩展。
- **优化** - Gson库经过高度优化。
- **支持泛型** - 它为泛型提供了广泛的支持。
- **支持复杂的内部类** - 它支持具有深度继承层次结构的复杂对象。

<!--more-->

#### Gson 的特点

这里列出了Gson的一些最显着的特点 

- **易于使用** - Gson API提供了一个高级外观来简化常用的用例。
- **无需创建映射** - Gson API为大部分要序列化的对象提供了默认映射。
- **性能优** - Gson速度相当快，内存占用量低。 它适用于大型对象图或系统。
- **干净**JSON - Gson创建一个干净而紧凑的JSON结果，它易于阅读。
- **无依赖性**—Gson库不需要JDK以外的任何其他库。
- **开源** - Gson库是开源的; 它是免费提供的。

#### 处理JSON的方法

Gson提供了三种处理JSON的替代方法 - 

1. **流媒体API**

   它读取和写入JSON内容作为离散事件。 JsonReader和JsonWriter将数据读取/写入令牌，称为JsonToken。
   这是处理JSON的三种方法中最强大的方法。 它具有最低的开销，并且在读/写操作中速度非常快。 它类似于用于XML的Stax解析器。

2. **树模型**

   它准备JSON文档的内存树表示。 它构建了一个JsonObject节点树。 这是一种灵活的方法，类似于XML的DOM解析器。

3. **数据绑定**

   它使用属性访问器将JSON转换为POJO(普通旧Java对象)并从中转换。 Gson使用数据类型适配器读取/写入JSON。 它类似于XML的JAXB解析器。

#### Gson 链接

- GitHub：https://github.com/google/gson
- 用户指南：https://sites.google.com/site/gson/gson-user-guide

#### Gson 引入

```xml
<!-- https://mvnrepository.com/artifact/com.google.code.gson/gson -->
<dependency>
    <groupId>com.google.code.gson</groupId>
    <artifactId>gson</artifactId>
    <version>2.8.6</version>
</dependency>
```

### Gson 入门程序

Gson是Google Gson库的主要操作类。 它提供了将Java对象转换为匹配的JSON结构的功能，反之亦然。 

Gson首先使用`GsonBuilder`构建，然后使用`toJson(Object)`或`fromJson(String，Class)`方法读取/写入JSON构造。

1. 使用`GsonBuilder`创建Gson对象
   创建一个Gson对象。 它是一个可重用的对象。

   ```java
   GsonBuilder builder = new GsonBuilder(); 
   builder.setPrettyPrinting(); 
   Gson gson = builder.create();
   ```

2. 将JSON反序列化为对象
   使用`fromJson()`方法从JSON获取对象。 传递Json字符串/Json字符串的源和对象类型作为参数。

   ```java
   //Object to JSON Conversion 
   Student student = gson.fromJson(jsonString, Student.class);
   ```

3. 将对象序列化为JSON
   使用`toJson()`方法获取对象的JSON字符串表示形式。

   ```java
   //Object to JSON Conversion   
   jsonString = gson.toJson(student);
   ```

示例如下：

```java
String jsonString = "{\"name\":\"Maxsu\", \"age\":24}";

GsonBuilder builder = new GsonBuilder();
builder.setPrettyPrinting();

Gson gson = builder.create();
Student student = gson.fromJson(jsonString, Student.class);
System.out.println(student);

jsonString = gson.toJson(student);
System.out.println(jsonString);
```

### Gson 序列化

#### 对象序列化

序列化写入：

```java
private void writeJSON(Student student) throws IOException {
	GsonBuilder builder = new GsonBuilder();
	Gson gson = builder.create();
	FileWriter writer = new FileWriter("student.json");
	writer.write(gson.toJson(student));
	writer.close();
}
```

序列化读取：

```java
private Student readJSON() throws FileNotFoundException {
	GsonBuilder builder = new GsonBuilder();
	Gson gson = builder.create();
	BufferedReader bufferedReader = new BufferedReader(new FileReader("student.json"));
	Student student = gson.fromJson(bufferedReader, Student.class);
	return student;
}
```

#### 数组序列化

```java
// 序列化 
int[] marks1 = {100,90,85}; 
System.out.println("marks:" + gson.toJson(marks1));        
// 反序列化
int[] marks2 = gson.fromJson("[100,90,85]", int[].class); 
System.out.println("marks:" + Arrays.toString(marks2));
```

#### 集合序列化

```java
// 序列化 
List<Integer> marks = Arrays.asList(1,2,3,4,5); 
System.out.println("marks:" + gson.toJson(marks));        
// 反序列化 
Type listType = new TypeToken<List<Integer>>(){}.getType(); 
marks = gson.fromJson("[100,90,85]", listType); 
System.out.println("marks:" +marks);
```

#### 泛型序列化

Gson使用Java反射API来获取要将Json文本映射到的对象的类型。 但是在泛型中，这些信息在序列化过程中丢失了。 

为了解决这个问题，Gson提供了一个`com.google.gson.reflect.TypeToken`类来存储通用对象的类型。

```java
Gson gson = new Gson();
// 创建泛型对象
Shape<Circle> shape = new Shape<Circle>();
Circle circle = new Circle(5.0);
shape.setShape(circle);

// 定义 TypeToken
Type shapeType = new TypeToken<Shape<Circle>>() {}.getType();

// 序列化
String jsonString = gson.toJson(shape, shapeType);
System.out.println(jsonString); // {"shape":{"radius":5.0}}

// （错误）通过 类 反序列化
Shape shape1 = gson.fromJson(jsonString, Shape.class);
System.out.println(shape1.get().getClass()); // class com.google.gson.internal.LinkedTreeMap
System.out.println(shape1.get().toString()); // {radius=5.0}
System.out.println(shape1.getArea()); // 0.0

// （正确）通过 TypeToken 反序列化
Shape shape2 = gson.fromJson(jsonString, shapeType); 
System.out.println(shape2.get().getClass()); // class demo.google.gson.Circle
System.out.println(shape2.get().toString()); // Circle
System.out.println(shape2.getArea()); // 78.5
```

其中：

```java
class Shape <T> { 
   public T shape;  

   public void setShape(T shape) { 
      this.shape = shape; 
   }  
   public T get() { 
      return shape; 
   }  
   public double getArea() { 
      if(shape instanceof Circle) { 
         return ((Circle) shape).getArea(); 
      } else { 
         return 0.0; 
      } 
   } 
}  
class Circle { 
   private double radius;  

   public Circle(double radius){ 
      this.radius = radius; 
   }  
   public String toString() { 
      return "Circle"; 
   }  
   public double getRadius() { 
      return radius; 
   }  
   public void setRadius(double radius) { 
      this.radius = radius; 
   }  
   public double getArea() { 
      return (radius*radius*3.14); 
   } 
}
```

#### 内部类序列化

```java
Person person = new Person();
person.setRollNo(1);
Person.Name name = person.new Name();
name.firstName = "Mahesh";
name.lastName = "Kumar";
person.setName(name);

Gson gson = new Gson();

String jsonString = gson.toJson(person);
System.out.println(jsonString); // {"rollNo":1,"name":{"firstName":"Mahesh","lastName":"Kumar"}}

// 主类
person = gson.fromJson(jsonString, Person.class);
System.out.println(person.getRollNo() +":"+ person.getName().firstName +":"+ person.getName().lastName); // 1:Mahesh:Kumar

// 内部类
String nameString = gson.toJson(name);
System.out.println(nameString); // {"firstName":"Mahesh","lastName":"Kumar"}
name = gson.fromJson(nameString, Person.Name.class);
System.out.println(name.getClass()); // class demo.google.gson.Person$Name
System.out.println(name.firstName + ":" + name.lastName); // Mahesh:Kumar
```

其中：

```java
class Person {
	private int rollNo;
	private Name name;

	public int getRollNo() {
		return rollNo;
	}

	public void setRollNo(int rollNo) {
		this.rollNo = rollNo;
	}

	public Name getName() {
		return name;
	}

	public void setName(Name name) {
		this.name = name;
	}

	class Name {
		public String firstName;
		public String lastName;
	}
}
```

### Gson 从序列化中排除字段

#### 使用excludeFieldsWithModifiers()

GsonBuilder使用序列化/反序列化过程中的`excludeFieldsWithModifiers()`方法提供对使用特定修饰符排除字段的控制。 

```java
GsonBuilder builder = new GsonBuilder(); 
builder.excludeFieldsWithModifiers(Modifier.TRANSIENT);    
Gson gson = builder.create();  
```

#### 使用[@Expose](https://github.com/Expose)注解

Gson提供`@Expose`注解来根据其范围控制类的Json序列化/反序列化。

1. 类属性中具有`@Expose`支持的变量的类。 

   ```java
   class Student2 {
   	@Expose
   	private int rollNo;
   	@Expose
   	private String name;
   	
   	private boolean verified;
   	private int id;
   	public static String className;
   }
   ```

   在这个类中，`name`和`rollno`变量将被暴露以进行序列化。 

2. 使用`GsonBuilder.excludeFieldsWithoutExposeAnnotation()`方法来指示只有暴露的变量要被序列化/反序列化。

   ```java
   GsonBuilder builder = new GsonBuilder();
   builder.excludeFieldsWithoutExposeAnnotation();
   Gson gson1 = builder.create();
   ```

### Gson 数据绑定

数据绑定API用于使用属性访问器或使用注释将JSON转换为POJO(普通旧Java对象)以及从POJO(普通旧Java对象)转换。 

它有两种类型，分别如下所示： 

- **原始数据绑定** - 将JSON转换为Java地图，列表，字符串，数字，布尔值和NULL对象。
- **对象数据绑定** - 从任何JAVA类型转换JSON。


Gson为这两种类型的数据绑定读/写JSON。 数据绑定类似于XML的JAXB解析器。

#### 原始数据绑定

基元数据绑定是指将JSON映射到JAVA核心数据类型和内置集合。 

Gson提供了各种内置适配器，可用于序列化/反序列化原始数据类型。

```java
Gson gson = new Gson();
String name = "Maxsu";
long rollNo = 1;
boolean verified = false;
int[] marks = { 100, 90, 85 };

// 序列化
System.out.println("{");
System.out.println("name: " + gson.toJson(name) + ",");
System.out.println("rollNo: " + gson.toJson(rollNo) + ",");
System.out.println("verified: " + gson.toJson(verified) + ",");
System.out.println("marks:" + gson.toJson(marks));
System.out.println("}");

// 反序列化
name = gson.fromJson("\"Maxsu\"", String.class);
rollNo = gson.fromJson("1", Long.class);
verified = gson.fromJson("false", Boolean.class);
marks = gson.fromJson("[100,90,85]", int[].class);
```

#### 对象数据绑定

对象数据绑定是指将JSON映射到任何JAVA对象。

```java
Gson gson = new Gson();
Student student = new Student();
student.setAge(26);
student.setName("Maxsu");

String jsonString = gson.toJson(student);
System.out.println(jsonString);

Student student1 = gson.fromJson(jsonString, Student.class);
System.out.println(student1);
```

### Gson 树模型

#### 从JSON创建树

在读取JSON之后，`JsonParser`提供了一个指向树的根节点的指针。根节点可以用来遍历整个树。 

下面的代码片段来获取提供的JSON字符串的根节点。

```java
JsonParser parser = new JsonParser();
String jsonString = "{\"name\":\"Maxsu\", \"age\":26,\"verified\":false,\"marks\": [100,90,85]}";
// 从JSON创建树
JsonElement rootNode = parser.parse(jsonString);
```

#### 遍历树模型

在遍历树并处理数据时，使用到根节点的相对路径获取每个节点。 

以下代码片段显示了如何遍历树。

```java
// 遍历树模型
if (rootNode.isJsonObject()) { 
	JsonObject details = rootNode.getAsJsonObject();
	JsonElement nameNode = details.get("name");
	System.out.println("Name: " + nameNode.getAsString());
	JsonElement ageNode = details.get("age");
	System.out.println("Age: " + ageNode.getAsInt());
	JsonElement verifiedNode = details.get("verified");
	System.out.println("Verified: " + (verifiedNode.getAsBoolean() ? "Yes" : "No"));
	JsonArray marks = details.getAsJsonArray("marks");
	for (int i = 0; i < marks.size(); i++) {
		JsonPrimitive value = marks.get(i).getAsJsonPrimitive();
		System.out.print(value.getAsInt() + " ");
	}
}
```

### Gson 数据流

Streaming API用于通过令牌读取JSON令牌。 它读取和写入JSON内容作为离散事件。 

`JsonReader`和`JsonWriter`将数据读取/写入令牌，称为`JsonToken`。

这是处理JSON的三种方法中最强大的方法。 它具有最低的开销，并且在读/写操作中速度非常快。 它类似于用于XML的Stax解析器。

下面，我们将展示使用GSON streaming API来读取JSON数据。 Streaming API与令牌的概念一起工作，Json的每个细节都要仔细处理。

```java
// 创建JsonReader对象，并将其传递给json文本。
JsonReader reader = new JsonReader(new StringReader(jsonString));  

// 开始读取   
reader.beginObject(); 

// 获取下一个
JsonToken token = reader.peek(); 

// 检查类型
if (token.equals(JsonToken.NAME)) {     
   // 获取内容
   fieldname = reader.nextName(); 
}
```

### Gson 自定义类型适配器

Gson使用其内置适配器执行对象的序列化/反序列化。 它也支持自定义适配器。 

#### 创建自定义适配器

通过扩展`TypeAdapter`类并传递目标类型的对象来创建自定义适配器。 

重写读写方法分别执行自定义的反序列化和序列化。

```java
class StudentAdapter extends TypeAdapter<Student> { 
   @Override 
   public Student read(JsonReader reader) throws IOException { 
      ... 
   } 
   @Override 
   public void write(JsonWriter writer, Student student) throws IOException { 
   } 
}
```

#### 注册自定义适配器

使用`GsonBuilder`注册自定义适配器并使用`GsonBuilder`创建一个Gson实例。

```java
GsonBuilder builder = new GsonBuilder(); 
builder.registerTypeAdapter(Student.class, new StudentAdapter()); 
Gson gson = builder.create();
```

#### 完整示例

```java
public class CustomAdaptersDemo {
	public static void main(String args[]) {
		GsonBuilder builder = new GsonBuilder();
		builder.registerTypeAdapter(Worker.class, new WorkerAdapter());
		builder.setPrettyPrinting();
		Gson gson = builder.create();

		String jsonString = "{\"name\":\"Maxsu\", \"rollNo\":1}";
		Worker worker = gson.fromJson(jsonString, Worker.class);
		System.out.println(worker);

		jsonString = gson.toJson(worker);
		System.out.println(jsonString);
	} 

}

class WorkerAdapter extends TypeAdapter<Worker> {
	@Override
	public Worker read(JsonReader reader) throws IOException {
		Worker worker = new Worker();
		reader.beginObject();
		String fieldname = null;

		while (reader.hasNext()) {
			JsonToken token = reader.peek();

			if (token.equals(JsonToken.NAME)) {
				fieldname = reader.nextName();
			}
			if ("name".equals(fieldname)) {
				token = reader.peek();
				worker.setName(reader.nextString());
			}
			if ("rollNo".equals(fieldname)) {
				token = reader.peek();
				worker.setRollNo(reader.nextInt());
			}
		}
		reader.endObject();
		return worker;
	}

	@Override
	public void write(JsonWriter writer, Worker worker) throws IOException {
		writer.beginObject();
		writer.name("name");
		writer.value(worker.getName());
		writer.name("rollNo");
		writer.value(worker.getRollNo());
		writer.endObject();
	}
}

class Worker {
	private int rollNo;
	private String name;

	public int getRollNo() {
		return rollNo;
	}

	public void setRollNo(int rollNo) {
		this.rollNo = rollNo;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String toString() {
		return "Worker[ name = " + name + ", roll no: " + rollNo + "]";
	}
}
```

### Gson 空对象支持

Gson默认生成优化的Json内容，忽略`NULL`值。 

但是`GsonBuilder`提供的标志使用`GsonBuilder.serializeNulls()`方法在Json输出中显示`NULL`值。

```java
// 默认
Gson gson1 = new Gson();
demo(gson1); // {"age":1}

// 使用serializeNulls
GsonBuilder builder = new GsonBuilder();
builder.serializeNulls();
builder.setPrettyPrinting();
Gson gson2 = builder.create();
demo(gson2); // {"name": null, "age": 1 }
```

其中，

```java
public static void demo(Gson gson) {
	Student student = new Student();
	student.setAge(1);

	String jsonString = gson.toJson(student);
	System.out.println(jsonString);
}
```

### Gson 版本支持

Gson提供了`@Since`注解来控制基于其各种版本的类的Json序列化/反序列化。

以下具有版本支持的类：

```java
class Demo {
	@Since(1.0)
	private int rollNo;

	@Since(1.0)
	private String name;

	@Since(1.1)
	private boolean verified;

	public int getRollNo() {
		return rollNo;
	}

	public void setRollNo(int rollNo) {
		this.rollNo = rollNo;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public void setVerified(boolean verified) {
		this.verified = verified;
	}

	public boolean isVerified() {
		return verified;
	}
}
```

进行Json序列化/反序列化：

```java
// 构建对象
Demo demo = new Demo();
demo.setRollNo(1);
demo.setName("Maxsu");
demo.setVerified(true);

// 默认
Gson gson1 = new Gson();
String jsonString1 = gson1.toJson(demo);
System.out.println(jsonString1); // {"rollNo":1,"name":"Maxsu","verified":true}

// 版本支持
GsonBuilder builder = new GsonBuilder();
builder.setVersion(1.0);
Gson gson2 = builder.create();
String jsonString2 = gson2.toJson(demo);
System.out.println(jsonString2); // {"rollNo":1,"name":"Maxsu"}
```



### 参考链接

- https://www.yiibai.com/gson