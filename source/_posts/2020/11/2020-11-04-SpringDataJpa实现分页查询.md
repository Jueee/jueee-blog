---
title: Spring Data Jpa实现分页查询
layout: info
commentable: true
date: 2020-11-04
mathjax: true
mermaid: true
tags: [Java,JavaJar]
categories: [Java,JavaJar]
description: 
---

### Spring Data Jpa

#### 引入 Jar

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
```

<!--more-->

#### 配置文件

SpringBoot 配置文件 `application.yml`：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/vuedb?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Shanghai
    username: root
    password: jue
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true # 日志打印 SQL
    properties:
      hibernate:
        format_sql: true # 格式化日志 SQL
```

### 方法一：本地SQL查询

本地sql查询,注意表名啥的都用数据库中的名称，适用于特定数据库的查询。

缺点：无法识别参数为空的情况。

```java
public interface BookDAO extends JpaRepository<Book,Integer> {

    @Query(value = "SELECT * FROM Book WHERE name like %:name% and author like %:author%",
            countQuery = "SELECT count(*) FROM Book WHERE name like %:name% and author like %:author%",
            nativeQuery = true)
    Page<Book> findAll1(@Param("name") String name, @Param("author") String author, Pageable pageable);
}
```

```java
@Autowired
private BookDAO bookRepository;

@GetMapping("/findAll/{page}/{size}")
public Page<Book> findAll(@PathVariable("page") Integer page, @PathVariable("size") Integer size,Book book){
	Pageable  request = PageRequest.of(page,size);
	return bookRepository.findAll1(book.getName(),book.getAuthor(),request);
}
```

### 方法二：分页接口

jpa已经实现的分页接口，适用于简单的分页查询。

缺点，无法增加查询条件。

接口说明：

```java
public interface PagingAndSortingRepository<T, ID extends Serializable>
  extends CrudRepository<T, ID> {

  Iterable<T> findAll(Sort sort);

  Page<T> findAll(Pageable pageable);
}

Accessing the second page of User by a page size of 20 you could simply do something like this:

PagingAndSortingRepository<User, Long> repository = // … get access to a bean
Page<User> users = repository.findAll(new PageRequest(1, 20));
```

示例如下：

```java
@Autowired
private BookDAO bookRepository;

@GetMapping("/findAll/{page}/{size}")
public Page<Book> findAll(@PathVariable("page") Integer page, @PathVariable("size") Integer size){
	Pageable  request = PageRequest.of(page,size);
	return bookRepository.findAll(request);
}
```

### 方法三：动态sql查询

扩充findAll，适用于动态sql查询

```java
public interface BookDAO extends JpaRepository<Book,Integer> {
    Page<Book> findAll(Specification<Book> spec, Pageable pageable);
}
```

```java
@Autowired
private BookDAO bookRepository;

@GetMapping("/findAll/{page}/{size}")
public Page<Book> findAll(@PathVariable("page") Integer page, @PathVariable("size") Integer size,Book book){
	Specification<Book> specification = new Specification<Book>() {
		@Override
		public Predicate toPredicate(Root<Book> root, CriteriaQuery<?> query, CriteriaBuilder cb) {
			List<Predicate> predicates = new ArrayList<>(); //所有的断言
			if(StringUtils.isNotBlank(book.getName())){ //添加断言
				Predicate likeNickName = cb.like(root.get("name").as(String.class),"%"+book.getName()+"%");
				predicates.add(likeNickName);
			}
			if(StringUtils.isNotBlank(book.getAuthor())){ //添加断言
				Predicate likeNickName = cb.like(root.get("author").as(String.class),"%"+book.getAuthor()+"%");
				predicates.add(likeNickName);
			}
			return cb.and(predicates.toArray(new Predicate[0]));
		}
	};
	Pageable  request = PageRequest.of(page,size);
	return bookRepository.findAll(specification,request);
}
```

### 方法四：动态sql查询

使用entityManager，适用于动态sql查询

```java
@PersistenceContext
EntityManager entityManager;

@GetMapping("/findAll/{page}/{size}")
public Page<Book> findAll(@PathVariable("page") Integer page, @PathVariable("size") Integer size,Book book){
	Map<String,Object> params = new HashMap<>();
	StringBuilder whereSql = new StringBuilder();
	if(StringUtils.isNotBlank(book.getName())){
		whereSql.append(" and name like :name ");
		params.put("name","%"+book.getName()+"%");
	}
	if(StringUtils.isNotBlank(book.getAuthor())){
		whereSql.append(" and author like :author ");
		params.put("author","%"+book.getAuthor()+"%");
	}
	StringBuilder countSelectSql = new StringBuilder();
	countSelectSql.append("select count(*) from Book where 1=1 ");
	String countSql = new StringBuilder().append(countSelectSql).append(whereSql).toString();
	Query countQuery = this.entityManager.createQuery(countSql,Long.class);
	this.setParameters(countQuery,params);
	Long count = (Long) countQuery.getSingleResult();


	StringBuilder selectSql = new StringBuilder();
	selectSql.append("from Book where 1=1 ");
	String querySql = new StringBuilder().append(selectSql).append(whereSql).toString();
	Query query = this.entityManager.createQuery(querySql, Book.class);
	this.setParameters(query,params);
	PageRequest pageParam = PageRequest.of(page, size);
	query.setFirstResult(Integer.valueOf(String.valueOf(pageParam.getOffset())));
	query.setMaxResults(pageParam.getPageSize());

	List<Book> incomeDailyList = query.getResultList();
	Pageable pageable = PageRequest.of(page, size);
	Page<Book> incomeDailyPage = new PageImpl<Book>(incomeDailyList, pageable, count);
	return incomeDailyPage;
}
private void setParameters(Query query,Map<String,Object> params){
	for(Map.Entry<String,Object> entry:params.entrySet()){
		query.setParameter(entry.getKey(),entry.getValue());
	}
}
```

