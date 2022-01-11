---
title: 基于colResizable-1.6实现一个表头固定、列宽可调的table
layout: info
commentable: true
date: 2021-11-30
mathjax: true
mermaid: true
tags: [JavaScript]
categories: JavaScript
description: 
---

### colResizable

- 官网：http://www.bacubacu.com/colresizable/
- GitHub：https://github.com/alvaro-prieto/colResizable

<!--more-->

### 实现功能

- 能够实现各列完全对齐
- 能够兼容有无滚动条两种情况
- 只能在表头部分拖动改变列宽（不能在表体列边框上拖动）

### 实现代码

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style type="text/css">
    table {
        border-collapse: collapse;
        width: 100%;
        /* 关键样式 */
        table-layout: fixed;
    }
    .table-header tr th {
        border: 1px solid red;
    }
    .table-body-wrapper {
        border: 1px solid red;
        height: 75px;
        overflow-x: hidden;
        overflow-y: auto;
    }
    .table-body tr td {
        border-right: 1px solid red;
        border-bottom: 1px solid red;
        /* 关键样式：不设置padding:0会导致无法完全对齐 */
        overflow: hidden;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    </style>
</head>

<body>
    <div class="table-header-wrapper">
        <table class="table-header">
            <tr>
                <th> header </th>
                <th> header header </th>
                <th> header </th>
            </tr>
        </table>
    </div>
    <div class="table-body-wrapper">
        <table class="table-body">
            <tr>
                <td> cell </td>
                <td> cell </td>
                <td> cell </td>
            </tr>
            <tr>
                <td> cell </td>
                <td> cell </td>
                <td> cell </td>
            </tr>
            <tr>
                <td> cell </td>
                <td> cell </td>
                <td> cell </td>
            </tr>
            <tr>
                <td> cell </td>
                <td> cell </td>
                <td> cell </td>
            </tr>
            <tr>
                <td> cell </td>
                <td> cell </td>
                <td> cell </td>
            </tr>
        </table>
    </div>
    <script src="https://cdn.bootcss.com/jquery/3.4.1/jquery.min.js"></script>
    <script src="colResizable-1.6.min.js"></script>
    <script type="text/javascript">
    $(function() {
        $(".table-header").colResizable({
            liveDrag: true,
            onDrag: syncCol
        });
        //页面加载完成后，手动对齐一次
        syncCol();
        //window resize的时候，会出现列不完全对齐的情况，手动对齐
        $(window).resize(function() {
            syncCol();
        });
    });

    function syncCol() {
        $('.table-body tr:first-child td').each(function() {
            $(this).width($('.table-header tr th:eq(' + $(this).index() + ')').css('width'));
        });
    }
    </script>
</body>

</html>
```

#### 细节调整

部分情况下，会出现上下列宽度不一致的情况，可再次微调：

```js
function syncCol() {
    $('.table-body tr:first-child td').each(function() {
        var px = $('.table-header tr th:eq(' + $(this).index() + ')').css('width').replace('px','');
        var pxN = (Number(px)-2)+'px';
        $(this).css('width',pxN);
    });
}
```

