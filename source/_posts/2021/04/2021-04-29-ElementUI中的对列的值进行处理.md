---
title: ElementUI中的对列的值进行处理
layout: info
commentable: true
date: 2021-04-29
mathjax: true
mermaid: true
tags: [Vue,ElementUI]
categories: Vue
description: 
---

### 超链接

```html
<el-table-column label="URL">
    <template slot-scope="scope">
        <el-link :href="scope.row.urlString" target="_blank" class="buttonText"  type="primary" :underline="false"> {{ scope.row.keyword }}</el-link>
    </template>
</el-table-column>
```

### 状态翻译

```html
<el-table-column prop="anttype" label="类型" width="120" :formatter="anttypeFormat"></el-table-column>
```

以下函数无效：

```js
    anttypeFormat(row, column) {
        this.markerCategorys.forEach(t => {
          if(t.id == row.anttype){
            return t.name;
          }
        })
    },
```

需要修改为：

```js
    anttypeFormat(row, column) {
        for (var i = 0; i < this.markerCategorys.length; i++) {
          if(this.markerCategorys[i].id == row.anttype){
            return this.markerCategorys[i].name;
          }
        }
    },
```

这是由于 Vue 中的 forEach 循环无法终止程序 return 无效。需要改为用for循环即可。