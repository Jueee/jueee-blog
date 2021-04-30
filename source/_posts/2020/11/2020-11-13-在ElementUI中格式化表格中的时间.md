---
title: 在ElementUI中格式化表格中的时间
layout: info
commentable: true
date: 2020-11-13
mathjax: true
mermaid: true
tags: [Vue,Element]
categories: Vue
description: 
---

### ElementUI 基础表格

```html
<el-table :data="tableData" style="width: 100%">
   <el-table-column prop="date" label="日期" width="180"></el-table-column>
   <el-table-column prop="name" label="姓名" width="180"></el-table-column>  
</el-table>
```

<!--more-->

### 定义过滤器

#### 过滤器文件

```js
// filters/index.js
export function formatDate(date, fmt) {
    date = new Date(date);
    if (typeof(fmt) === "undefined") {
        fmt = "yyyy-MM-dd HH:mm:ss";
    }
    if (/(y+)/.test(fmt)) {
        fmt = fmt.replace(RegExp.$1, (date.getFullYear() + '').substr(4 - RegExp.$1.length))
    }
    let o = {
        'M+': date.getMonth() + 1,
        'd+': date.getDate(),
        'H+': date.getHours(),
        'm+': date.getMinutes(),
        's+': date.getSeconds()
    }
    for (let k in o) {
        if (new RegExp(`(${k})`).test(fmt)) {
            let str = o[k] + ''
            fmt = fmt.replace(RegExp.$1, RegExp.$1.length === 1 ? str : ('00' + str).substr(str.length));
        }
    }
    return fmt
}
```

#### 全局注册

在 main.js 中全局注册所有自定义的过滤器

```js
import * as filters from './filters'

Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})
```

### 使用过滤器的写法

默认格式

```html
<el-table :data="tableData" style="width: 100%">
   <el-table-column label="日期" width="180">
        <template slot-scope="scope">
            <span>{{ scope.row.date | formatDate() }}</span>
        </template>
   </el-table-column>
   <el-table-column prop="name" label="姓名" width="180"></el-table-column>  
</el-table>
```

把时间转换成 时:分:秒 格式

```html
<el-table :data="tableData" style="width: 100%">
   <el-table-column label="日期" width="180">
        <template slot-scope="scope">
            <span>{{ scope.row.date | formatDate('HH:mm:ss') }}</span>
        </template>
   </el-table-column>
   <el-table-column prop="name" label="姓名" width="180"></el-table-column>  
</el-table>
```

