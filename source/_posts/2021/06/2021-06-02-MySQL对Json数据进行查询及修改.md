---
title: MySQL对Json数据进行查询及修改
layout: info
commentable: true
date: 2021-06-02
mathjax: true
mermaid: true
tags: [Database,MySQL]
categories: [Database,MySQL]
description: 
---

在项目中，有部分数据是以 JsonObject 和 JsonArray 的形式直接存储在 MySQL 中的。

如果想对 这部分数据进行查询 等操作，非常不便。

经查询，MySQL 5.7.8 新增了对 Json 数据的相关支持，MySQL 8.0.4 新增了 Json 表函数的功能。

通过使用 内置的 函数，可以非常方便的对以 JsonObject 和 JsonArray 的形式直接存储在 MySQL 中的字段，进行查找、排序等操作。

本文总结了 MySQL 对 Json 操作的相关用法。

<!--more-->

### MySQL Json 支持

MySQL 5.7.8 新增了对 Json 数据的相关支持，可以对 JsonObject 数据进行解析、查询等操作。

MySQL 8.0.4 新增了 Json 表函数的功能，可以将 JsonArray 数据解析为表格形式，再进行查询等操作。

同时，也可以通过 Json 函数建立虚拟列，并加相关索引，提供检索效率。

本博客总结 MySQL 对 Json 操作的相关用法。

对字符串列JSON格式的字符串：

- 自动验证存储在 Json 列中的 Json 文档 。无效的文档会产生错误。
- 优化的存储格式。存储在 Json 列中的Json 文档 被转换为允许有效访问文档元素的内部格式。

此外，还可以使用 SQL 函数对 Json 值进行操作，例如创建、操作和搜索。

#### 相关链接

- [MySQL 5.7 更新日志](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/)
- [MySQL 5.7.8 中 Json 更新说明](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-8.html#mysqld-5-7-8-json)
- [MySQL 5.7.8 中 Json 数据类型](https://dev.mysql.com/doc/refman/5.7/en/json.html)
- [MySQL 8.0 更新日志](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/)
- [MySQL 8.0.4 中 Json 表函数](https://dev.mysql.com/doc/refman/8.0/en/json-table-functions.html)

### Json 函数汇总

[MySQL官方]([MySQL 5.7.8 中 Json 函数](https://dev.mysql.com/doc/refman/5.7/en/json-functions.html)) 列出json相关的函数，完整列表如下:

| 分类                                                         | 函数                                                         | 描述                                         |
| :----------------------------------------------------------- | :----------------------------------------------------------- | :------------------------------------------- |
| [创建json](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html) | [JSON_ARRAY](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array) | 创建json数组                                 |
|                                                              | [JSON_OBJECT](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object) | 创建json对象                                 |
|                                                              | [JSON_QUOTE](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-quote) | 将json转成json字符串类型                     |
| [查询json](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html) | [JSON_CONTAINS](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains) | 判断是否包含某个json值                       |
|                                                              | [JSON_CONTAINS_PATH](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains-path) | 判断某个路径下是否包含 json值                |
|                                                              | [JSON_EXTRACT](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract) | 提取json值                                   |
|                                                              | [column->path](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-column-path) | JSON_EXTRACT的简洁写法，MySQL 5.7.9开始支持  |
|                                                              | [column->>path](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-inline-path) | JSON_UNQUOTE(column -> path)的简洁写法       |
|                                                              | [JSON_KEYS](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-keys) | 提取json中的键值为json数组                   |
|                                                              | [JSON_SEARCH](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-search) | 按给定字符串关键字搜索json，返回匹配的路径   |
| [修改json](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html) | [JSON_APPEND](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-append) | 废弃，MySQL 5.7.9开始改名为json_array_append |
|                                                              | [JSON_ARRAY_APPEND](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-array-append) | 末尾添加数组元素                             |
|                                                              | [JSON_ARRAY_INSERT](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-array-insert) | 插入数组元素                                 |
|                                                              | [JSON_INSERT](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert) | 插入值（插入新值，但不替换已经存在的旧值）   |
|                                                              | [JSON_MERGE](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge) | 合并json数组或对象                           |
|                                                              | [JSON_REMOVE](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove) | 删除json数据                                 |
|                                                              | [JSON_REPLACE](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace) | 替换值（只替换已经存在的旧值）               |
|                                                              | [JSON_SET](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set) | 设置值（替换旧值，并插入不存在的新值）       |
|                                                              | [JSON_UNQUOTE](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote) | 去除json字符串的引号，将值转成string类型     |
| [返回json属性](https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html) | [JSON_DEPTH](https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-depth) | 返回json文档的最大深度                       |
|                                                              | [JSON_LENGTH](https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html%23function_json-length) | 返回json文档的长度                           |
|                                                              | [JSON_TYPE](https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html%23function_json-type) | 返回json值得类型                             |
|                                                              | [JSON_VALID](https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html%23function_json-valid) | 判断是否为合法json文档                       |

### 创建 JSON

如想插入如下所示的 Json 对中：

```simple
version: My MySQL version is "5.7.33".
```

#### JSON_OBJECT

在这种情况下，必须使用**反斜杠**对每个引号字符进行转义，如下所示：

```sql
INSERT INTO json_demo(json_data) 
VALUES (JSON_OBJECT("version", "My MySQL version is \"5.7.33\"."));
```

具有与文档中先前找到的键重复的键的成员将被丢弃（即使值不同）

```sql
SELECT JSON_OBJECT('key1', 'aaa', 'key2', 'bbb', 'key1', 'ccc');

>> {"key1": "aaa", "key2": "bbb"}
```

#### Json 对象文本

如果将值作为 Json 对象文本插入，必须使用**双反斜杠**转义序列，如下所示：

```sql
INSERT INTO json_demo(json_data) 
VALUES ('{"version": "My MySQL version is \\"5.7.33\\"."}');
```

#### JSON_ARRAY

创建 Json Array

```sql
SELECT JSON_ARRAY(JSON_OBJECT("key1", "aaa"),JSON_OBJECT("key2", "bbb"),JSON_OBJECT("key3", "ccc"));
>> [{"key1": "aaa"}, {"key2": "bbb"}, {"key3": "ccc"}]

SELECT JSON_ARRAY(true,JSON_OBJECT("key1", "aaa"),'bbb',10);
>> [true, {"key1": "aaa"}, "bbb", 10]
```

#### JSON_QUOTE

通过用双引号字符包裹字符串并转义内部引号和其他字符，将`utf8mb4`字符串引用为 Json 值，然后将结果作为字符串返回 。

```sql
原始 json_data 列数据：
>> {"a": 1, "b": {"c": 30}}

SELECT JSON_QUOTE(json_data) FROM json_demo;
>> "{\"a\": 1, \"b\": {\"c\": 30}}"
```



### 查找 JSON

#### JSON_EXTRACT

要查找 version 用作关键字的特定句子 ，您可以使用列路径运算符 **->**，如下所示：

```mysql
SELECT json_data->'$.version' FROM json_demo;

>> "My MySQL version is \"5.7.33\"."
```

或者：

```sql
SELECT JSON_EXTRACT(json_data, '$.version') FROM json_demo;

>> "My MySQL version is \"5.7.33\"."
```

#### JSON_UNQUOTE

如果想不包括周围的引号或任何转义符，请使用内联路径运算符  **->>** ，如下所示：

```sql
SELECT json_data,json_data->>'$.version' FROM json_demo;

>> My MySQL version is "5.7.33".
```

或者 使用 `JSON_UNQUOTE` 函数 ，可以去除 Json 字符串的引号，将值转成 String 类型：

```sql
SELECT JSON_UNQUOTE(JSON_EXTRACT(json_data, '$.version')) FROM json_demo;

>> My MySQL version is "5.7.33".
```

#### JSON_CONTAINS

格式如：`JSON_CONTAINS(target, candidate[, path])`

通过返回 1 或 0 指示给定的 candidate Json 文档是否包含在target Json 文档中。

如果提供了*`path`* 参数，则在目标内的特定路径中查找候选者。

```sql
原始 json_data 列数据：
>> {"a": 1, "b": {"c": 30}}

查询文档 "a":1 是否在上述 Json 中
SELECT JSON_CONTAINS(json_data,JSON_OBJECT('a',1)) FROM json_demo;
>> 1

查询 30 是否在指定的 JsonPath 中
SELECT JSON_CONTAINS(json_data,'30','$.b.c') FROM json_demo;
>> 1
```

#### JSON_CONTAINS_PATH

格式如：`JSON_CONTAINS_PATH(json_doc, one_or_all, path[, path] ...)`

返回 0 或 1 以指示 Json 文档是否包含给定路径或多个路径中的数据。

如果文档中不存在指定路径，则返回值为 0。否则，返回值取决于 *`one_or_all`*参数：

- `'one'`: 如果文档中至少存在一个路径，则为 1，否则为 0。
- `'all'`: 1 如果文档中存在所有路径，否则为 0。

```sql
原始 json_data 列数据：
>> {"a": 1, "b": {"c": 30}}

查询 one ，至少存在一个
SELECT JSON_CONTAINS_PATH(json_data,'one','$.a','$.b','$.c') FROM json_demo;
>> 1

查询 all , 存在所有路径
SELECT JSON_CONTAINS_PATH(json_data,'all','$.a','$.b','$.c') FROM json_demo;
>> 0
```

#### JSON_KEYS

将 Json 对象的顶级值中的键作为 Json 数组返回，或者，如果path 给出了参数，则返回所选路径中的顶级键。

```sql
原始 json_data 列数据：
>> {"a": 1, "b": {"c": 30}}

SELECT JSON_KEYS(json_data) FROM json_demo;
>> ["a", "b"]

SELECT JSON_KEYS(json_data,'$.b') FROM json_demo;
>> ["c"]
```

#### JSON_SEARCH

格式如：`JSON_SEARCH(json_doc, one_or_all, search_str[, escape_char[, path] ...])`

返回 Json 文档中给定字符串的路径。

该*`one_or_all`* 参数影响搜索如下：

- `'one'`：搜索在第一次匹配后终止并返回一个路径字符串。未定义首先考虑哪个匹配。
- `'all'`：搜索返回所有匹配的路径字符串，这样就不会包含重复的路径。如果有多个字符串，它们会自动包装为一个数组。数组元素的顺序未定义。

```sql
原始 json_data 列数据：
>> ["abc", [{"k": "10"}, "def"], {"x":"abc"}, {"y":"bcd"}]

one 第一次匹配
SELECT JSON_SEARCH(json_data,'one','abc') FROM json_demo;
>> "$[0]"

all 所有匹配
SELECT JSON_SEARCH(json_data,'all','abc') FROM json_demo;
>> ["$[0]", "$[2].x"]
```



### 修改 JSON

#### JSON_MERGE：合并

```sql
SELECT JSON_MERGE('{"key1": 1, "key2": 2}', '{"key3": 3, "key1": 4}');

>> {"key1": [1, 4], "key2": 2, "key3": 3}
```

将对象自动包装为数组、合并两个数组和对象值：

```sql
SELECT JSON_MERGE('[10, 20]', '{"a": "x", "b": "y"}');

>> [10, 20, {"a": "x", "b": "y"}]
```

#### JSON_SET：替换

JSON_SET() 可以替换存在路径的值、或者为不存在的路径添加值：

```sql
原始 json_data 列数据：
>> {"version": "My MySQL version is \"5.7.33\"."}

修改 value 值：
SELECT JSON_SET(json_data, '$.version', 'new version info') FROM json_demo;
>> {"version": "new version info"}

添加值：
SELECT JSON_SET(json_data, '$[1]', JSON_OBJECT("newkey","new info")) FROM json_demo;
>> [{"version": "My MySQL version is \"5.7.33\"."}, {"newkey": "new info"}]
```

#### JSON_INSERT：添加

JSON_INSERT() 添加新值但不替换现有值。

#### JSON_REPLACE：替换

JSON_REPLACE() 替换现有值并忽略新值。

#### JSON_REMOVE：删除

JSON_REMOVE()接受一个 Json 文档和一个或多个指定要从文档中删除的值的路径。

返回值是原始文档减去文档中存在的路径选择的值：

```sql
原始 json_data 列数据：
>> {"version": "My MySQL version is \"5.7.33\"."}

SELECT JSON_REMOVE(json_data, '$.version') FROM json_demo;
>> {}
```

```sql
原始 json_data 列数据：
>> ["a", {"b": [1, false]}, [10, 20]]

SELECT JSON_REMOVE(json_data, '$[2]', '$[1].b[1]', '$[1].b[1]') FROM json_demo;
>> ["a", {"b": [1]}]
```

### Json 属性

#### JSON_DEPTH：深度

返回 Json 文档的最大深度。

空数组、空对象或标量值的深度为 1。仅包含深度为 1 的元素的非空数组或仅包含深度为 1 的成员值的非空对象的深度为 2。

```sql
原始 json_data 列数据：
>> {"a": 1, "b": {"c": 30}}

SELECT JSON_DEPTH(json_data) FROM json_demo;
>> 3
```

```sql
原始 json_data 列数据：
>> ["abc", [{"k": "10"}, "def"], {"x":"abc"}, {"y":"bcd"}]

SELECT JSON_DEPTH(json_data) FROM json_demo;
>> 4
```

#### JSON_LENGTH：长度

返回 Json 文档的长度。

文档的长度确定如下：

- 标量的长度为 1。
- 数组的长度是数组元素的数量。
- 对象的长度是对象成员的数量。
- 长度不计算嵌套数组或对象的长度。

```sql
原始 json_data 列数据：
>> {"a": 1, "b": {"c": 30}}

SELECT JSON_LENGTH(json_data) FROM json_demo;
>> 2
```

```sql
原始 json_data 列数据：
>> ["abc", [{"k": "10"}, "def"], {"x":"abc"}, {"y":"bcd"}]

SELECT JSON_LENGTH(json_data) FROM json_demo;
>> 4
```

#### JSON_TYPE：类型

返回`utf8mb4`指示 Json 值类型的字符串。这可以是 OBJECT、ARRAY、INTEGER、BOOLEAN。

```sql
原始 json_data 列数据：
>> ["a", {"b": [1, false]}, [10, 20]]

SELECT JSON_TYPE(json_data) FROM json_demo;
>> ARRAY            

SELECT JSON_TYPE(JSON_EXTRACT(json_data, '$[1]')) FROM json_demo;
>> OBJECT

SELECT JSON_TYPE(JSON_EXTRACT(json_data, '$[1].b[1]')) FROM json_demo;
>> BOOLEAN
```

#### JSON_VALID：有效

返回 0 或 1 以指示值是否为有效的 JSON。

```sql
原始 json_data 列数据：
>> ["a", {"b": [1, false]}, [10, 20]]

SELECT JSON_VALID(json_data) FROM json_demo;
>> 1  
```

```sql
原始 json_data 列数据：
>> hello

SELECT JSON_VALID(json_data) FROM json_demo;
>> 0
```

```sql
原始 json_data 列数据：
>> "hello"

SELECT JSON_VALID(json_data) FROM json_demo;
>> 1
```

### JSON_TABLE 表操作

在 MySQL 8.0.4 及更高版本中，JSON_TABLE 函数可以将 Json 数据转换为表格数据的 Json 函数的信息。

格式为：

```
JSON_TABLE(
    expr,
    path COLUMNS (column_list)
)   [AS] alias
```

注意：

- 必须起别名 alias，否则会报错 `Every table function must have an alias`。

示例：

```mysql
set @jsoninfo='[{"name":"Alice"},{"name":"Bob"},{"name":"Cindy"}]';
SELECT * from JSON_TABLE(@jsoninfo,
                         "$[*]" COLUMNS( 
                             rowid FOR ORDINALITY,
                             name VARCHAR(100) PATH "$.name")) as t;
查询结果：
+-------+-------+
| rowid | name  |
+-------+-------+
|     1 | Alice |
|     2 | Bob   |
|     3 | Cindy |
+-------+-------+
```

从数据库中进行取值：

```mysql
原始 json_data 列数据：
>> [{"name":"Alice"},{"name":"Bob"},{"name":"Cindy"}]

SELECT t.* from json_demo,JSON_TABLE(json_data,"$[*]" COLUMNS( rowid FOR ORDINALITY,name VARCHAR(100) PATH "$.name")) as t;

查询结果：
+-------+-------+
| rowid | name  |
+-------+-------+
|     1 | Alice |
|     2 | Bob   |
|     3 | Cindy |
+-------+-------+
```

```
原始 json_data 列数据（在表中 id = 2）：
>> [{"x":2,"y":"8"},{"x":"3","y":"7"},{"x":"4","y":6}]

SELECT t.* from json_demo a,
JSON_TABLE(json_data,"$[*]" COLUMNS( 
    rowid FOR ORDINALITY,xval VARCHAR(100) PATH "$.x",
    yval VARCHAR(100) PATH "$.y")) as t
where a.id=2;

查询结果：
+-------+------+------+
| rowid | xval | yval |
+-------+------+------+
|     1 | 2    | 8    |
|     2 | 3    | 7    |
|     3 | 4    | 6    |
+-------+------+------+
```

### Json 虚拟列

#### 新增虚拟列

建立 员工信息表 如下所示，其中 JSON_EXTRACT 和 JSON_UNQUOTE 都是上面介绍过的：

```sql
CREATE TABLE `employee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `json_data` mediumtext NULL,
  `name` varchar(20) GENERATED ALWAYS AS (JSON_UNQUOTE(JSON_EXTRACT(`json_data`,'$.name'))) VIRTUAL NULL,
  PRIMARY KEY (`id`),
  KEY `name_index` (`name`)
) ENGINE=InnoDB
```

或者使用内联路径运算符  **->>** ，如下所示：

```sql
CREATE TABLE `employee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `json_data` mediumtext NULL,
  `name` varchar(20) GENERATED ALWAYS AS (json_data->>'$.name') VIRTUAL NULL,
  PRIMARY KEY (`id`),
  KEY `name_index` (`name`)
) ENGINE=InnoDB
```

其中，name 列即为虚拟字段，它是根据 json_data 列的 Json 数据，自动生成的。

对表中插入数据：

```sql
// Json 中包含 name 
INSERT INTO employee (`json_data`) VALUES ('{"name":"Alice","age":25}');
INSERT INTO employee (`json_data`) VALUES ('{"name":"Bob","age":28}');
INSERT INTO employee (`json_data`) VALUES ('{"name":"Cindy","age":24}');

// Json 中不包含 name 
INSERT INTO employee (`json_data`) VALUES ('{"sex":"male","age":24}');

// 插入非 Json 的数据
INSERT INTO employee (`json_data`) VALUES ('test text info');
```

可以发现，前面四条数据都添加成功了，第四条由于不包含 name ，所以 name 虚拟列为 null。

但五条数据报错，因为它不是 Json 格式：

```
Invalid Json text in argument 1 to function json_extract: "Invalid value." at position 1
```

使用 JSON_SET 更新某条 Json 数据，可以发现虚拟列也同步进行了更新：

```
原始 json_data 列数据：
>> {"name":"Bob","age":28}

update employee set json_data=JSON_SET(json_data, '$.name', 'Bassam') where id=2;

更新后数据：
+----+-------------------------------+--------+
| id | json_data                     | name   |
+----+-------------------------------+--------+
|  2 | {"age": 28, "name": "Bassam"} | Bassam |
+----+-------------------------------+--------+
```

#### 虚拟列索引

分析查询语句可以发现：

```
explain SELECT name FROM employee where name='Bob';
```

![image-20210603174344730](/images/2021/06/image-20210603174344730.png)

会用到 name 虚拟列的 `name_index` 索引。

通过 `json_data->'$.name'` 查询，也会用到 虚拟列的 `name_index` 索引。

```
explain SELECT name FROM employee where json_data->'$.name'='Bob';
```

#### 省略虚拟列

建立索引的时候，也可以省略虚拟列，直接创建索引。

建表示例如下：

```sql
CREATE TABLE `employee` (
  `id` int NOT NULL AUTO_INCREMENT,
  `json_data` mediumtext,
  PRIMARY KEY (`id`),
  KEY `json_data_name_index` ((cast(`json_data`->>'$.name' as char(255))))
) ENGINE=InnoDB
```

新增语句如前所述。

查看 explain 执行计划：

```
explain SELECT * FROM `test`.`employee` where json_data->>'$.name'='Bob';
```

可以发现并没有用到所创建的索引。

![image-20210603192327275](/images/2021/06/image-20210603192327275.png)

这是由于前面表定义中的索引表达式`WHERE`与查询中的子句表达式之间存在排序规则不匹配，[参考](https://dev.mysql.com/doc/refman/8.0/en/create-index.html)。

可以在查询中指定完整表达式：

```
explain SELECT * FROM `test`.`employee` where CAST(json_data->>'$.name'AS CHAR(25))='Bob';
```

即可看到，使用了所创建的索引。

![image-20210603192300147](/images/2021/06/image-20210603192300147.png)