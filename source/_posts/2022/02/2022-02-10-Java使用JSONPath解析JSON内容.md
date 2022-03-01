---
title: Java使用JSONPath解析JSON内容
layout: info
commentable: true
date: 2022-02-10
mathjax: true
mermaid: true
tags: [Java]
categories: [Java,JavaJar]
description: 
---

### JSONPath

用来解析多层嵌套的json数据;JsonPath 是一种信息抽取类库，是从JSON文档中抽取指定信息的工具。

<!--more-->

#### JSONPath 操作符

| 操作                    | 说明                                      |
| ----------------------- | ----------------------------------------- |
| $                       | 查询根元素。这将启动所有路径表达式。      |
| @                       | 当前节点由过滤谓词处理。                  |
| *                       | 通配符，必要时可用任何地方的名称或数字。  |
| ..                      | 深层扫描。 必要时在任何地方可以使用名称。 |
| .<name>                 | 点，表示子节点                            |
| ['<name>' (, '<name>')] | 括号表示子项                              |
| [<number> (, <number>)] | 数组索引或索引                            |
| [start:end]             | 数组切片操作                              |
| [?(<expression>)]       | 过滤表达式。 表达式必须求值为一个布尔值。 |

#### JSONPath 函数

函数可以在路径的尾部调用，函数的输出是路径表达式的输出，该函数的输出是由函数本身所决定的。

| 函数       | 描述                     | 输出     |
| :--------- | :----------------------- | :------- |
| `min()`    | 提供数字数组的最小值     | `Double` |
| `max()`    | 提供数字数组的最大值     | `Double` |
| `avg()`    | 提供数字数组的平均值     | `Double` |
| `stddev()` | 提供数字数组的标准偏差值 | `Double` |
| `length()` | 提供数组的长度           | Integer  |

#### 过滤器运算符

过滤器是用于筛选数组的逻辑表达式。一个典型的过滤器将是[?(@.age > 18)]，其中@表示正在处理的当前项目。 可以使用逻辑运算符&&和||创建更复杂的过滤器。 字符串文字必须用单引号或双引号括起来([?(@.color == 'blue')] 或者 [?(@.color == "blue")]).

| 操作符  | 描述                                     |
| :------ | :--------------------------------------- |
| `==`    | left等于right（注意1不等于'1'）          |
| `!=`    | 不等于                                   |
| `<`     | 小于                                     |
| `<=`    | 小于等于                                 |
| `>`     | 大于                                     |
| `>=`    | 大于等于                                 |
| `=~`    | 匹配正则表达式[?(@.name =~ /foo.*?/i)]   |
| `in`    | 左边存在于右边 [?(@.size in ['S', 'M'])] |
| `nin`   | 左边不存在于右边                         |
| `size`  | （数组或字符串）长度                     |
| `empty` | （数组或字符串）为空                     |

### 使用 fastjson 解析

#### 介绍

- GitHub：https://github.com/alibaba/fastjson

#### 用法

```java
JSONPath.read(json, path).toString();
```

示例：JsonObject

```java
String jsonString = "{\"name\":\"jue\",\"age\":30}";
JSONPath.read(jsonString, "$.name").toString(); // jue

JSONObject jsonObject = JSON.parseObject(jsonString);
JSONPath.eval(jsonObject, "$.name").toString(); // jue
```

示例：JsonArray

```java
String jsonString = "[{\"name\":\"jue\",\"age\":30},{\"name\":\"kai\",\"age\":12}]";
JSONPath.read(jsonString,"$.name").toString();    // ["jue","kai"]
JSONPath.read(jsonString,"$.name[0]").toString(); // jue
JSONPath.read(jsonString,"$[*].name").toString(); // ["jue","kai"]
JSONPath.read(jsonString,"$[0].name").toString(); // jue
JSONPath.read(jsonString, "$[*][?(@.age > 20)]").toString();     // [{"name":"jue","age":30}]
JSONPath.read(jsonString, "$[*][?(@.age > 20)].age").toString(); // [30]

String jsonString = "[{\"name\":\"jue\",\"age\":30},{\"name\":\"kai\",\"age\":12}]";
JSONArray jsonArray = JSON.parseArray(jsonString);
JSONPath.eval(jsonArray, "$.name").toString();    // ["jue","kai"]
JSONPath.eval(jsonArray, "$.name[0]").toString(); // jue
JSONPath.eval(jsonArray, "$[*].name").toString(); // ["jue","kai"]
JSONPath.eval(jsonArray, "$[0].name").toString(); // jue
JSONPath.eval(jsonArray, "$[*][?(@.age > 20)]").toString();     // [{"name":"jue","age":30}]
JSONPath.eval(jsonArray, "$[*][?(@.age > 20)].age").toString(); // [30]
```

### 使用 json-path 解析

#### 介绍

- GitHub：https://github.com/json-path/JsonPath

#### 依赖

```xml
<dependency>
    <groupId>com.jayway.jsonpath</groupId>
    <artifactId>json-path</artifactId>
    <version>2.7.0</version>
</dependency>
```

#### 用法一

每次获取都需要再解析整个文档：

```java
JsonPath.read(json,path).toString();
```

示例：JsonObject

```java
String jsonString = "{\"name\":\"jue\",\"age\":30}";
JsonPath.read(jsonString,"$.name").toString(); // jue
```

示例：JsonArray

```java
String jsonString = "[{\"name\":\"jue\",\"age\":30},{\"name\":\"kai\",\"age\":12}]";
JsonPath.read(jsonString, "$.name").toString();    // 异常，不支持该解析
JsonPath.read(jsonString, "$.name[0]").toString(); // 异常，不支持该解析
JsonPath.read(jsonString, "$[*].name").toString(); // ["jue","kai"]
JsonPath.read(jsonString, "$[0].name").toString(); // jue
JsonPath.read(jsonString, "$[*][?(@.age > 20)]").toString();     // [{"name":"jue","age":30}]
JsonPath.read(jsonString, "$[*][?(@.age > 20)].age").toString(); // [30]
List<String> list = JsonPath.read(jsonString, "$[*].name"); // ["jue","kai"]
```

#### 用法二

先解析整个文档，再选择调用路径。

```
Object document = Configuration.defaultConfiguration().jsonProvider().parse(jsonString);
JsonPath.read(document, path);
```

示例：JsonObject

```java
String jsonString = "{\"name\":\"jue\",\"age\":30}";
Object document = Configuration.defaultConfiguration().jsonProvider().parse(jsonString);
JsonPath.read(document,"$.name").toString(); // jue
```

示例：JsonArray

```java
String jsonString = "[{\"name\":\"jue\",\"age\":30},{\"name\":\"kai\",\"age\":12}]";
Object document = Configuration.defaultConfiguration().jsonProvider().parse(jsonString);
JsonPath.read(document,"$[*].name").toString(); // ["jue","kai"]
JsonPath.read(document,"$[0].name").toString(); // jue
JsonPath.read(document,"$[*][?(@.age > 20)]").toString();     // [{"name":"jue","age":30}]
JsonPath.read(document,"$[*][?(@.age > 20)].age").toString(); // [30]
List<String> list = JsonPath.read(document, "$[*].name"); // ["jue","kai"]
```

#### 用法三

先解析整个文档，再选择调用路径。

```
Object document = Configuration.defaultConfiguration().jsonProvider().parse(jsonString);
JsonPath.read(document, path);
```

示例：JsonObject

```java
String jsonString = "{\"name\":\"jue\",\"age\":30}";
ReadContext context = JsonPath.parse(jsonString);
context.read("$.name").toString(); // jue
```

示例：JsonArray

```java
String jsonString = "[{\"name\":\"jue\",\"age\":30},{\"name\":\"kai\",\"age\":12}]";
ReadContext context = JsonPath.parse(jsonString);
context.read("$[*].name").toString(); // ["jue","kai"]
context.read("$[0].name").toString(); // jue
context.read("$[*][?(@.age > 20)]").toString();     // [{"name":"jue","age":30}]
context.read("$[*][?(@.age > 20)].age").toString(); // [30]
List<String> list = context.read("$[*].name"); // ["jue","kai"]
```

### 使用 Snack3 解析

Snack3 是一个轻量的 JSON + JSONPath 框架。

#### 介绍

- GitHub：https://github.com/noear/snack3

#### 依赖

```xml
<dependency>
    <groupId>org.noear</groupId>
    <artifactId>snack3</artifactId>
    <version>3.2.11</version>
</dependency>
```

#### 用法

```java
ONode o = ONode.load(json);
ONode oNode = o.select(path);
```

示例：JsonObject

```java
String jsonString = "{\"name\":\"jue\",\"age\":30}";
ONode o = ONode.load(jsonString);
o.select("$.name").toString(); // jue
```

示例：JsonArray

```java
String jsonString = "[{\"name\":\"jue\",\"age\":30},{\"name\":\"kai\",\"age\":12}]";
ONode o = ONode.load(jsonString);
o.select("$.name").toString();    // ["jue","kai"]
o.select("$.name[0]").toString(); // jue
o.select("$[*].name").toString(); // ["jue","kai"]
o.select("$[0].name").toString(); // jue
o.select("$[*][?(@.age > 20)]");     // [{"name":"jue","age":30}]
o.select("$[*][?(@.age > 20)].age"); // [30]
```

