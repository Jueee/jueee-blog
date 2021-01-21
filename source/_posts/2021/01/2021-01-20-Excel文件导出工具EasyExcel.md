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

### EasyExcel 导入示例

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
@PostMapping("uploadBooks")
@ResponseBody
public String uploadBooks(HttpServletRequest request, @RequestParam(value = "file") MultipartFile file) throws IOException {
    log.info("init uploadBooks...");
    log.info(file.getOriginalFilename());
    EasyExcel.read(file.getInputStream(), Book.class, new BookListener(bookMapper)).sheet().doRead();
    return "success";
}
```

#### Listener

```java
import com.alibaba.excel.context.AnalysisContext;
import com.alibaba.excel.event.AnalysisEventListener;
import com.jueee.domain.Book;
import com.jueee.mapper.BookMapper;
import lombok.extern.slf4j.Slf4j;

import java.util.ArrayList;
import java.util.List;

/**
 * 模板的读取类
 * 有个很重要的点 DemoDataListener 不能被spring管理，要每次读取excel都要new,然后里面用到spring可以构造方法传进去
 */
@Slf4j
public class BookListener extends AnalysisEventListener<Book> {
    /**
     * 每隔5条存储数据库，实际使用中可以3000条，然后清理list ，方便内存回收
     */
    private static final int BATCH_COUNT = 5;
    List<Book> list = new ArrayList<Book>();
    /**
     * 假设这个是一个DAO，当然有业务逻辑这个也可以是一个service。当然如果不用存储这个对象没用。
     */
    private BookMapper bookMapper;

    /**
     * 如果使用了spring,请使用这个构造方法。每次创建Listener的时候需要把spring管理的类传进来
     * @param bookMapper
     */
    public BookListener(BookMapper bookMapper) {
        this.bookMapper = bookMapper;
    }

    /**
     * 这个每一条数据解析都会来调用
     * @param data
     *            one row value. Is is same as {@link AnalysisContext#readRowHolder()}
     * @param context
     */
    @Override
    public void invoke(Book data, AnalysisContext context) {
        log.info("解析到一条数据:{}", data.toString());
        list.add(data);
        // 达到BATCH_COUNT了，需要去存储一次数据库，防止数据几万条数据在内存，容易OOM
        if (list.size() >= BATCH_COUNT) {
            saveData();
            // 存储完成清理 list
            list.clear();
        }
    }

    /**
     * 所有数据解析完成了 都会来调用
     *
     * @param context
     */
    @Override
    public void doAfterAllAnalysed(AnalysisContext context) {
        // 这里也要保存数据，确保最后遗留的数据也存储到数据库
        saveData();
        log.info("所有数据解析完成！");
    }

    /**
     * 加上存储数据库
     */
    private void saveData() {
        log.info("{}条数据，开始存储数据库！", list.size());
        list.forEach(t->{
            t.setId(null);
            bookMapper.insert(t);
        });
        log.info("存储数据库成功！");
    }
}
```

#### HTML

```html
<form class="form-horizontal" role="form" id="uploadBooksForm" method="post" action="uploadBooks" enctype="multipart/form-data">
    <input id="input-b2" name="file" type="file" class="file" data-show-preview="false">
    <button type="submit" class="btn btn-success"><i class="glyphicon glyphicon-plus"></i> 上传</button>
</form>
```

使用 bootstrap 美化：

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-fileinput/5.1.4/css/fileinput.min.css" media="all" rel="stylesheet" type="text/css" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-fileinput/5.1.4/js/fileinput.min.js"></script>
    
<form class="form-horizontal" role="form" id="uploadBooksForm" method="post" action="uploadBooks" enctype="multipart/form-data">
    <div style="width:500px">
        <input id="input-b2" name="file" type="file" class="file" data-show-preview="false">
    </div>
    <button type="submit" class="btn btn-success"><i class="glyphicon glyphicon-plus"></i> 上传</button>
</form>
```

![image-20210121104627269](/images/2021/01/image-20210121104627269.png)

#### 上传效果

![image-20210121104901268](/images/2021/01/image-20210121104901268.png)