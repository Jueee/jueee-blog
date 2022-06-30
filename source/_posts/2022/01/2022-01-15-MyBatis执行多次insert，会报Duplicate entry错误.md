---
title: MyBatis执行多次insert，会报Duplicate entry错误
layout: info
commentable: true
date: 2022-01-15
mathjax: true
mermaid: true
tags: [Java,JavaJar,MyBatis]
categories: [Java,JavaError]
description: 
---

MyBatis 执行多次 insert，会报 Duplicate entry 错误。

<!--more-->

### 问题复现

我的实体为：

```java
public class Book implements Serializable {
    @Id
    @GeneratedValue(generator = "JDBC")
    private Long id;
}
```

现在已经有BookMapper

```java
@Mapper
public interface BookMapper extends tk.mybatis.mapper.common.Mapper<Book> {
}
```

当通过该BookMapper执行多次insert方法的时候，会报Duplicate entry错误。

```java
public Book createBook(BookDto bookDto) {
    Book book = new Book();
    book.setAuthor(bookDto.getAuthor());
    book.setDescription(bookDto.getDescription());
    book.setIsbn(bookDto.getIsbn());
    book.setTitle(bookDto.getTitle());
    book.setReader(bookDto.getReader());
    //下面多次执行insert操作，此时会报重复的主键错误
    bookRepository.insert(book);
    bookRepository.insert(book);
}
```

错误信息如下：

```java
### Error updating database.  Cause: com.mysql.jdbc.exceptions.jdbc4.MySQLIntegrityConstraintViolationException: Duplicate entry '40' for key 'PRIMARY'
### The error may involve com.test.repository.BookMapper.insert-Inline
### The error occurred while setting parameters
### SQL: INSERT INTO book  ( id,reader,isbn,title,author,description ) VALUES( ?,?,?,?,?,? )
### Cause: com.mysql.jdbc.exceptions.jdbc4.MySQLIntegrityConstraintViolationException: Duplicate entry '40' for key 'PRIMARY'
; SQL []; Duplicate entry '40' for key 'PRIMARY'; nested exception is com.mysql.jdbc.exceptions.jdbc4.MySQLIntegrityConstraintViolationException: Duplicate entry '40' for key 'PRIMARY'] with root cause

com.mysql.jdbc.exceptions.jdbc4.MySQLIntegrityConstraintViolationException: Duplicate entry '40' for key 'PRIMARY'
	at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method) ~[na:1.8.0_121]
	at sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62) ~[na:1.8.0_121]
	at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45) ~[na:1.8.0_121]
	at java.lang.reflect.Constructor.newInstance(Constructor.java:423) ~[na:1.8.0_121]
	at com.mysql.jdbc.Util.handleNewInstance(Util.java:425) ~[mysql-connector-java-5.1.43.jar:5.1.43]
```

如果不是使用tk的通用Mapper,而是手动书写mapper

```
 <insert id="createBook" parameterType="com.test.domain.Book" useGeneratedKeys="true" keyProperty="id">
        insert into book(
            author,
            description, isbn, reader,
            title
        ) values(
            #{author},
            #{description}, #{isbn}, #{reader},
            #{title}
        )
    </insert>
```

多次调用上面的方法，入库成功。

### 问题原因

区别在于你手写的里面没有主键字段。

通用 Mapper优先使用赋的主键值，没有值时和你手写的一样。

但是第一次插入回写后就有值了，所以应该set null 再 insert。

### 问题解决

```java
public Book createBook(BookDto bookDto) {
    Book book = new Book();
    book.setAuthor(bookDto.getAuthor());
    book.setDescription(bookDto.getDescription());
    book.setIsbn(bookDto.getIsbn());
    book.setTitle(bookDto.getTitle());
    book.setReader(bookDto.getReader());
    book.setId(null);  // 主键先 set null 再 insert
    bookRepository.insert(book);
    bookRepository.insert(book);
}
```

### 参考链接

> https://github.com/abel533/Mapper/issues/150
