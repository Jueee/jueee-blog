---
title: Bootstrap Table列宽拖动的方法
layout: info
commentable: true
date: 2021-05-12
mathjax: true
mermaid: true
tags: [HTML]
categories: HTML
description: 
---

### Bootstrap

- 官方插件：https://bootstrap-table.com/docs/extensions/resizable/

### 方法一：colResizable

- 官网介绍：http://www.bacubacu.com/colresizable/
- GitHub：https://github.com/alvaro-prieto/colResizable

#### 引入依赖

```html
<script type="text/javascript" src="http://www.bacubacu.com/colresizable/js/colResizable-1.6.min.js"></script>
```

#### 示例代码

```html
<html>
<title>colResizable</title>    
<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
<script type="text/javascript" src="http://www.bacubacu.com/colresizable/js/colResizable-1.6.min.js"></script>
<script type="text/javascript"> 
    $(function(){
        $("#table").colResizable();
    })
</script>

</head>
<body>
  <table id="table" class="table table-bordered table-hover"> 
   <thead>
    <tr>
     <th style="width: 19.09%;" >ID</th>
     <th style="width: 33.56%;" >Item Name</th>
     <th style="width: 47.28%;" >Item Price</th>
    </tr>
   </thead> 
   <tbody>
    <tr data-index="0">
     <td>0</td>
     <td>Item 0</td>
     <td>$0</td>
    </tr>
    <tr data-index="1">
     <td>1</td>
     <td>Item 1</td>
     <td>$1</td>
    </tr>
    <tr data-index="2">
     <td>10</td>
     <td>Item 10</td>
     <td>$10</td>
    </tr>
   </tbody>
  </table> 
</body>
```

### 方法二：resizableColumns

- GitHub：https://github.com/dobtco/jquery-resizable-columns
- 官方示例：http://dobtco.github.io/jquery-resizable-columns/

#### 引入依赖

```html
<script src="js/main/jquery.resizableColumns.min.js"></script>
<link rel="stylesheet" href="css/main/jquery.resizableColumns.css">
```

#### 示例代码

```html
<html>
<head>
<link rel="stylesheet" href="http://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<link rel="stylesheet" href="http://dobtco.github.io/jquery-resizable-columns/dist/jquery.resizableColumns.css">
<script src="http://dobtco.github.io/jquery-resizable-columns/dist/jquery.resizableColumns.min.js"></script>
<body>

 <table id="table" class="table table-bordered table-hover"> 
   <thead>
    <tr>
     <th style="width: 19.09%;" >ID</th>
     <th style="width: 33.56%;" >Item Name</th>
     <th style="width: 47.28%;" >Item Price</th>
    </tr>
   </thead> 
   <tbody>
    <tr data-index="0">
     <td>0</td>
     <td>Item 0</td>
     <td>$0</td>
    </tr>
    <tr data-index="1">
     <td>1</td>
     <td>Item 1</td>
     <td>$1</td>
    </tr>
    <tr data-index="2">
     <td>10</td>
     <td>Item 10</td>
     <td>$10</td>
    </tr>
   </tbody>
  </table> 
</body>
<script>
$(function(){
  $("#table").resizableColumns({
    store: window.store
  });
});
</script>
```

![image-20210512155456453](/images/2021/05/image-20210512155456453.png)