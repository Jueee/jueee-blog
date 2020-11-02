---
title: 基于Vue组件库Element搭建管理系统
layout: info
commentable: true
date: 2020-11-03
mathjax: true
mermaid: true
tags: [Vue,Element]
categories: Vue
description: 
---

### Element 介绍

Element，一套为开发者、设计师和产品经理准备的基于 Vue 2.0 的桌面端组件库。

Element 提供了配套设计资源，帮助你的网站快速成型。

是由饿了么公司前端团队开源的。

- 官网：https://element.eleme.cn/
- GitHub：https://github.com/ElemeFE/element/

<!--more-->

### 安装 Element

```bash
npm i element-ui -S
```

### 引入 Element

在 main.js 中写入以下内容：

```javascript
import Vue from 'vue';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';

Vue.use(ElementUI);

new Vue({
  el: '#app',
  render: h => h(App)
});
```

若报错：

![image-20201102153341973](/images/2020/11/image-20201102153341973.png)

原因：缺少匹配规则

解决办法：在webpack.config.js文件中的module中增加如下json

```json
{
   test: /\.(eot|svg|ttf|woff|woff2)(\?\S*)?$/,
   loader: 'file-loader'
}
```

如下图所示：

![image-20201102153601127](/images/2020/11/image-20201102153601127.png)