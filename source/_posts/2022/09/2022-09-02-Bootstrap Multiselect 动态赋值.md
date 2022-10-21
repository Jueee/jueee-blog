---
title: Bootstrap Multiselect 动态赋值
layout: info
commentable: true
date: 2022-09-02
mathjax: true
mermaid: true
tags: [JavaScript]
categories: JavaScript
description: 
---

记录在用 Bootstrap Multiselect 的时候，从后台传来的值，动态赋值的解决方法。

<!--more-->

### 动态赋值

```js
var newDatas = new Array();
var obj = new Object();
$.each(datas, function(index, temp) {
    obj = {
        label : temp.text,
        value : temp.id
    };
    newDatas.push(obj);
});
$("#dataId").multiselect('dataprovider', newDatas);     
$('#dataId').multiselect('refresh');
```

其中，`datas` 为动态赋值的键值对数组。

### FreeMarker

```js
var newDatas = new Array();
var obj = new Object();
 <#list dataList as temp>
    obj = {
        label : '${temp.text}',
        value : '${temp.id}'
    };
    newDatas.push(obj);
 </#list>
$("#dataId").multiselect('dataprovider', newDatas);
$('#dataId').multiselect('refresh');
```

其中，`dataList` 为后台返回的键值对数组。

### 动态赋值后重新勾选

```js
var dataSearch = $("#dataSearch").val();
if(dataSearch!=''){
	$('#dataId').multiselect('select', dataSearch.split(','));
}
```

其中，`dataSearch` 为动态赋值前的勾选值。
