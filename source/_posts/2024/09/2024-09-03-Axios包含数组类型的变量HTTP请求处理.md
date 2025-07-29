---
title: Axios包含数组类型的变量HTTP请求处理
layout: info
commentable: true
date: 2024-09-03
mathjax: true
mermaid: true
tags: [Vue,axios]
categories: [Vue]
description: 
---

### 问题描述
```js
axios.request({
    url: url,
    method: "post",
    responseType: "blob",
    params: this.queryMap
})
```

在使用 Axios 进行 HTTP 请求时，如果 `params` 包含数组类型的变量，默认情况下，Axios 会将数组参数转换成类似 `param[]=value1&param[]=value2` 的形式。

然而，这种默认行为可能与服务器的预期格式不匹配，导致异常。

如果你希望数组参数以其他格式传递，可以使用 `paramsSerializer` 来自定义序列化过程。

<!--more-->

下面是一个示例，展示如何使用 `qs` 库将数组参数序列化为所需的格式。

### 使用 `qs` 库进行自定义序列化



首先，确保你已经安装了 `qs` 库：



```bash

npm install qs

```



然后，你可以在 Axios 请求中使用 `qs.stringify` 方法来自定义参数序列化：



```javascript

import axios from 'axios';

import qs from 'qs';



axios.request({

  url: url,

  method: 'post',

  responseType: 'blob',

  params: this.queryMap,

  paramsSerializer: params => {

​    return qs.stringify(params, { arrayFormat: 'repeat' });

  }

});

```



在 `qs.stringify` 方法中，`arrayFormat` 有多种选项，你可以根据需要选择适合你的选项：



\- `'indices'` (默认): `param[0]=value0&param[1]=value1`

\- `'brackets'`: `param[]=value0&param[]=value1`

\- `'repeat'`: `param=value0&param=value1`

\- `'comma'`: `param=value0,value1`



例如：



```javascript

paramsSerializer: params => {

  return qs.stringify(params, { arrayFormat: 'brackets' });

}

```



### 另一种方式：手动序列化



如果你不想引入额外的库，可以手动实现参数序列化：



```javascript

function customParamsSerializer(params) {

  const queryString = Object.keys(params).map(key => {

​    const value = params[key];

​    if (Array.isArray(value)) {

​      return value.map(val => `${encodeURIComponent(key)}=${encodeURIComponent(val)}`).join('&');

​    } else {

​      return `${encodeURIComponent(key)}=${encodeURIComponent(value)}`;

​    }

  }).join('&');

  

  return queryString;

}



axios.request({

  url: url,

  method: 'post',

  responseType: 'blob',

  params: this.queryMap,

  paramsSerializer: customParamsSerializer

});

```



#### 完整示例



##### 使用 `qs` 库



```javascript

import axios from 'axios';

import qs from 'qs';



axios.request({

  url: url,

  method: 'post',

  responseType: 'blob',

  params: this.queryMap,

  paramsSerializer: params => {

​    return qs.stringify(params, { arrayFormat: 'repeat' });

  }

});

```



##### 手动序列化



```javascript

function customParamsSerializer(params) {

  const queryString = Object.keys(params).map(key => {

​    const value = params[key];

​    if (Array.isArray(value)) {

​      return value.map(val => `${encodeURIComponent(key)}=${encodeURIComponent(val)}`).join('&');

​    } else {

​      return `${encodeURIComponent(key)}=${encodeURIComponent(value)}`;

​    }

  }).join('&');

  

  return queryString;

}



axios.request({

  url: url,

  method: 'post',

  responseType: 'blob',

  params: this.queryMap,

  paramsSerializer: customParamsSerializer

});

```



通过自定义 `paramsSerializer`，你可以确保数组类型的请求变量以正确的格式发送，从而避免出现异常。
