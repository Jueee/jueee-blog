---
title: 自定义element-ui的table表格数据样式
layout: info
commentable: true
date: 2021-01-25
mathjax: true
mermaid: true
tags: [Vue,elementUI]
categories: 
- [Vue]
description: 
---

有需要根据不同状态来区分table数据样式的需求，比如更换不同的颜色。

<!--more-->

### 原始状态

```html
<el-table :data="tableData" border style="width: 70%">
    <el-table-column fixed prop="id" label="编号" width="50"></el-table-column>
    <el-table-column prop="name" label="图书名" width="120"></el-table-column>
    <el-table-column prop="author" label="作者" width="120"></el-table-column>
    <el-table-column prop="status" label="状态" width="120"></el-table-column>
</el-table>
```



![image-20210125184037289](/images/2021/01/image-20210125184037289.png)

### 方案一：简单判断

```html
<el-table :data="tableData" border style="width: 70%">
    <el-table-column fixed prop="id" label="编号" width="50"></el-table-column>
    <el-table-column prop="name" label="图书名" width="120"></el-table-column>
    <el-table-column prop="author" label="作者" width="120"></el-table-column>
    <el-table-column prop="status" label="状态" width="120">
        <template slot-scope="scope">
            <font v-if="scope.row.status === '1'" color="green">已收藏</font>
            <font v-else-if="scope.row.status === '2'" color="red">正阅读</font>
            <font v-else color="blue">已读完</font>
        </template>
    </el-table-column>
</el-table>
```

效果：

![image-20210125192704801](/images/2021/01/image-20210125192704801.png)

### 方案二：cell-style

[elementUI文档](https://element.eleme.cn/#/zh-CN/component/table)，有个cell-style的属性，可以通过回调，返回样式。

![image-20210125192415426](/images/2021/01/image-20210125192415426.png)

```html
<el-table :data="tableData" border style="width: max-content;" :cell-style="cellStyle">
    <el-table-column fixed prop="id" label="编号" width="50"></el-table-column>
    <el-table-column prop="name" label="图书名" width="120"></el-table-column>
    <el-table-column prop="author" label="作者" width="120"></el-table-column>
    <el-table-column prop="status" label="状态" width="120"></el-table-column>
</el-table>
```

其中：

```js
    methods: {
        cellStyle(row,column,rowIndex,columnIndex){
            // console.log(row);
            // console.log(row.column);
            if(row.column.label==="状态" && row.row.status==="1"){
                return "color:green"
            } else if(row.column.label==="状态" && row.row.status==="2"){
                return 'color:red'
            } else if(row.column.label==="状态" && row.row.status==="3"){
                return 'color:blue'
            }
        }
    },
```

效果：

![image-20210125192823150](/images/2021/01/image-20210125192823150.png)