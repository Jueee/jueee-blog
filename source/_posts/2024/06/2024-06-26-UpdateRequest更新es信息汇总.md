---
title: UpdateRequest更新es信息汇总
layout: info
commentable: true
date: 2024-06-26
mathjax: true
mermaid: true
tags: [Blog]
categories: Blog
description: 
---

可以使用 UpdateRequest 更新 es 文档信息。

<!--more-->


### 更新单id单属性

```java
// 创建更新请求
UpdateRequest request = new UpdateRequest();
request.index("your_index"); // 设置索引名
request.id("your_id"); // 设置文档ID

// 创建更新的文档
Map<String, Object> jsonMap = new HashMap<>();
jsonMap.put("updated_field", "new_value"); // 设置需要更新的字段和新值
request.doc(jsonMap); // 设置更新的文档

// 执行更新请求
UpdateResponse updateResponse = client.update(request, RequestOptions.DEFAULT);
```



### 更新单id嵌套属性

```java
// 创建更新请求
UpdateRequest request = new UpdateRequest();
request.index("your_index"); // 设置索引名
request.id("your_id"); // 设置文档ID

// 创建脚本
Map<String, Object> parameters = new HashMap<>();
parameters.put("key", "your_key");
parameters.put("value", "new_value");
Script inline = new Script(ScriptType.INLINE, "painless",
  "def found = false; for (int i = 0; i < ctx._source.properties.length; ++i) {" +
  " if (ctx._source.properties[i].key == params.key) { found = true; ctx._source.properties[i].value = params.value; break; }}" +
  " if (!found) { ctx._source.properties.add(['key':params.key, 'value':params.value]); }", parameters);
request.script(inline);

// 执行更新请求
UpdateResponse updateResponse = client.update(request, RequestOptions.DEFAULT);
```



### 更新多 id 嵌套属性

```java
// 创建批量请求
BulkRequest request = new BulkRequest();

// 创建脚本
Map<String, Object> parameters = new HashMap<>();
parameters.put("key", "your_key");
parameters.put("value", "new_value");
Script inline = new Script(ScriptType.INLINE, "painless",
  "def found = false; for (int i = 0; i < ctx._source.properties.length; ++i) {" +
  " if (ctx._source.properties[i].key == params.key) { found = true; ctx._source.properties[i].value = params.value; break; }}" +
  " if (!found) { ctx._source.properties.add(['key':params.key, 'value':params.value]); }", parameters);

// 添加多个更新请求到批量请求
for (String id : your_ids) {
  UpdateRequest updateRequest = new UpdateRequest("your_index", id);
  updateRequest.script(inline);
  request.add(updateRequest);
}

// 执行批量请求
BulkResponse bulkResponse = client.bulk(request, RequestOptions.DEFAULT);
```



### 更新多 id 多个嵌套属性

```java
// 创建批量请求
BulkRequest request = new BulkRequest();

// 创建脚本参数
Map<String, Object> parameters = new HashMap<>();
parameters.put("properties", Arrays.asList(
  new HashMap<String, Object>() {{ put("key", "your_key1"); put("value", "new_value1"); }},
  new HashMap<String, Object>() {{ put("key", "your_key2"); put("value", "new_value2"); }}
  // 添加更多属性...
));

// 创建脚本
Script inline = new Script(ScriptType.INLINE, "painless",
  "for (def property : params.properties) {" +
  "  def found = false;" +
  "  for (int i = 0; i < ctx._source.properties.length; ++i) {" +
  "    if (ctx._source.properties[i].key == property.key) {" +
  "      found = true;" +
  "      ctx._source.properties[i].value = property.value;" +
  "      break;" +
  "    }" +
  "  }" +
  "  if (!found) {" +
  "    ctx._source.properties.add(property);" +
  "  }" +
  "}", parameters);

// 添加多个更新请求到批量请求
for (String id : your_ids) {
  UpdateRequest updateRequest = new UpdateRequest("your_index", id);
  updateRequest.script(inline);
  request.add(updateRequest);
}

// 执行批量请求
BulkResponse bulkResponse = client.bulk(request, RequestOptions.DEFAULT);
```



