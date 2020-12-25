---
title: JavaScript校验密码复杂度
layout: info
commentable: true
date: 2020-12-04
mathjax: true
mermaid: true
tags: [JavaScript]
categories: JavaScript
description: 
---

1、密码中必须包含大小字母、数字、特称字符，至少8个字符，最多30个字符。

```js
var regex = new RegExp('(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[^a-zA-Z0-9]).{8,30}');
if (!regex.test('123456@qq.com')) {
	alert("密码中必须包含字母、数字、特殊字符，请重新设置！");
}
```

2、密码中必须包含字母、数字、特称字符，至少8个字符，最多30个字符。
```js
var regex = new RegExp('(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[^a-zA-Z0-9]).{8,30}');
 
if (!regex.test('123456@qq.com')) {
	alert("密码中必须包含字母、数字、特殊字符，请重新设置！");
}
```
3、密码中必须包含字母、数字，至少8个字符，最多30个字符。
```js
var regex = new RegExp('(?=.*[0-9])(?=.*[a-zA-Z]).{8,30}');
 
if (!regex.test('123456@qq.com')) {
	alert("密码中必须包含字母、数字，请重新设置！");
}
```