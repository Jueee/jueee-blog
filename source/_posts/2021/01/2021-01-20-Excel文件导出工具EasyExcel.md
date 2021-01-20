---
title: Excel文件导出工具EasyExcel
layout: info
commentable: true
date: 2021-01-20
mathjax: true
mermaid: true
tags: [Java,JavaJar,Excel]
categories: [Java,JavaJar]
description: 
---

### EasyExcel

EasyExcel 是阿里巴巴开源的一个excel处理框架，以使用简单、节省内存著称。

- 使用说明：https://www.yuque.com/easyexcel/doc/easyexcel
- GitHub：https://github.com/alibaba/easyexcel

<!--more-->

#### EasyExcel 引入

```xml
<!-- https://mvnrepository.com/artifact/com.alibaba/easyexcel -->
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>easyexcel</artifactId>
    <version>2.2.7</version>
</dependency>
```

### EasyExcel 注解

官方 API：https://www.yuque.com/easyexcel/doc/api

#### 类注解

##### 表头高度

```
@HeadRowHeight(int)：
```

##### 内容高度

```
@ContentRowHeight(int):
```

#### 属性注解

##### 忽略字段

@ExcelIgnore：默认所有字段都会写入excel，这个注解会忽略这个字段

##### 表头信息

```
@ExcelProperty(value = String[], index = int):
value: 指定写入的名称，默认成员变量的名字。
index: 指定写到第几列，默认根据成员变量排序。
```

##### 设置列宽

```
@ColumnWidth(int)：
int
```

### 项目代码

本文完整项目代码位于：[https://github.com/Jueee/blog-project/tree/main/alibaba-easyexcel](https://github.com/Jueee/blog-project/tree/main/alibaba-easyexcel)

### EasyExcel 导出示例

#### Bean 

```java
import com.alibaba.excel.annotation.ExcelIgnore;
import com.alibaba.excel.annotation.ExcelProperty;
import com.alibaba.excel.annotation.write.style.ColumnWidth;
import com.alibaba.excel.annotation.write.style.ContentRowHeight;
import com.alibaba.excel.annotation.write.style.HeadRowHeight;
import lombok.Data;

import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

@Data
@HeadRowHeight(40)
@ContentRowHeight(20)
@Table(name="book")
public class Book {
    @Id
    @GeneratedValue(generator = "JDBC")
    private Long id;

    @ColumnWidth(20)
    @ExcelProperty("书名")
    private String name;

    @ColumnWidth(20)
    @ExcelProperty("作者")
    private String author;

    @ColumnWidth(30)
    @ExcelProperty("出版社")
    private String publish;

    private Integer pages;

    private Double price;

    @ExcelIgnore
    private Integer bookcaseid;

    @ExcelIgnore
    private Integer abled;
}
```

#### Controller

```java
@GetMapping("downloadBooks")
public void downloadBooks(HttpServletResponse response) throws IOException {
    response.setContentType("application/vnd.ms-excel");
    response.setCharacterEncoding("utf-8");
    // 这里URLEncoder.encode可以防止中文乱码 当然和easyexcel没有关系
    String fileName = URLEncoder.encode("测试", "UTF-8").replaceAll("\\+", "%20");
    response.setHeader("Content-disposition", "attachment;filename*=utf-8''" + fileName + ".xlsx");
    List<Book> bookList = bookService.selectAll();
    EasyExcel.write(response.getOutputStream(), Book.class).sheet("模板").doWrite(bookList);
}
```

#### HTML

```html
<button type="button" class="btn btn-success" onclick="downloadBooks()">
    <i class="glyphicon glyphicon-circle-arrow-down"></i> 下载
</button>
```

#### JavaScript

```js
function downloadBooks(id){
    window.location="downloadBooks";
}
```

#### 下载效果

进行下载：

![image-20210120171826187](/images/2021/01/image-20210120171826187.png)

打开文件：

![image-20210120171748715](/images/2021/01/image-20210120171748715.png)