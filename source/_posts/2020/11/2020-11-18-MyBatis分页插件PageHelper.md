---
title: MyBatis 分页插件 PageHelper
layout: info
commentable: true
date: 2020-11-18
mathjax: true
mermaid: true
tags: [Java,JavaJar,MyBatis]
categories: [Java,JavaJar]
description: 
---

### PageHelper 介绍

PageHelper是Github上开源的MyBatis分页插件，使用起来非常的简单，方便，并且支持任何复杂的单表、多表分页。

- 官网：https://pagehelper.github.io/
- 文档：https://pagehelper.github.io/docs/howtouse/

<!--more-->

#### 普通 maven

- GitHub：https://github.com/pagehelper/Mybatis-PageHelper
- Gitee：https://gitee.com/free/Mybatis_PageHelper

引入 PageHelper 

```xml
<!-- https://mvnrepository.com/artifact/com.github.pagehelper/pagehelper -->
<dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper</artifactId>
    <version>5.2.0</version>
</dependency>
```

#### Springboot 

- GitHub：https://github.com/pagehelper/pagehelper-spring-boot

引入 PageHelper 

```xml
<dependency>
    <groupId>com.github.pagehelper</groupId>
    <artifactId>pagehelper-spring-boot-starter</artifactId>
    <version>1.3.0</version>
</dependency>
```

### 类说明

[com.github.pagehelper.PageInfo](https://github.com/pagehelper/Mybatis-PageHelper/blob/master/src/main/java/com/github/pagehelper/PageInfo.java) 类的常用属性：

- pageNum：当前为第几页
- pageSize：每页的数据行数
- startRow：当前页数据从第几条开始
- endRow：当前页数据从第几条结束
- pages：总页数
- prePage：上一页页数
- nextPage：下一页页数
- isFirstPage：是否第一页
- isLastPage：是否最后一页
- hasPreviousPage：是否有上一页
- hasNextPage：是否有下一页
- navigatePages：导航页码数
- navigatepageNums：所有页码的数组
- navigateFirstPage：导航条上的第一页
- navigateLastPage：导航条上的最后一页

示例如下：

![image-20201118172445823](/images/2020/11/image-20201118172445823.png)

### 调用方式

```java
//第一种，RowBounds方式的调用
List<Country> list = sqlSession.selectList("x.y.selectIf", null, new RowBounds(0, 10));

//第二种，Mapper接口方式的调用，推荐这种使用方式。
PageHelper.startPage(1, 10);
List<Country> list = countryMapper.selectIf(1);

//第三种，Mapper接口方式的调用，推荐这种使用方式。
PageHelper.offsetPage(1, 10);
List<Country> list = countryMapper.selectIf(1);

//第四种，参数方法调用
//存在以下 Mapper 接口方法，你不需要在 xml 处理后两个参数
public interface CountryMapper {
    List<Country> selectByPageNumSize(
            @Param("user") User user,
            @Param("pageNum") int pageNum,
            @Param("pageSize") int pageSize);
}
//配置supportMethodsArguments=true
//在代码中直接调用：
List<Country> list = countryMapper.selectByPageNumSize(user, 1, 10);

//第五种，参数对象
//如果 pageNum 和 pageSize 存在于 User 对象中，只要参数有值，也会被分页
//有如下 User 对象
public class User {
    //其他fields
    //下面两个参数名和 params 配置的名字一致
    private Integer pageNum;
    private Integer pageSize;
}
//存在以下 Mapper 接口方法，你不需要在 xml 处理后两个参数
public interface CountryMapper {
    List<Country> selectByPageNumSize(User user);
}
//当 user 中的 pageNum!= null && pageSize!= null 时，会自动分页
List<Country> list = countryMapper.selectByPageNumSize(user);

//第六种，ISelect 接口方式
//jdk6,7用法，创建接口
Page<Country> page = PageHelper.startPage(1, 10).doSelectPage(new ISelect() {
    @Override
    public void doSelect() {
        countryMapper.selectGroupBy();
    }
});
//jdk8 lambda用法
Page<Country> page = PageHelper.startPage(1, 10).doSelectPage(()-> countryMapper.selectGroupBy());

//也可以直接返回PageInfo，注意doSelectPageInfo方法和doSelectPage
pageInfo = PageHelper.startPage(1, 10).doSelectPageInfo(new ISelect() {
    @Override
    public void doSelect() {
        countryMapper.selectGroupBy();
    }
});
//对应的lambda用法
pageInfo = PageHelper.startPage(1, 10).doSelectPageInfo(() -> countryMapper.selectGroupBy());

//count查询，返回一个查询语句的count数
long total = PageHelper.count(new ISelect() {
    @Override
    public void doSelect() {
        countryMapper.selectLike(country);
    }
});
//lambda
total = PageHelper.count(()->countryMapper.selectLike(country));
```

### 代码示例

简单分页

```java
// 获取第pageNum页，pageSize条内容
PageHelper.startPage(pageNum,pageSize);
// 条件查询相关
Example o = new Example(User.class);
Example.Criteria criteria = o.createCriteria();
o.setOrderByClause("id desc");
if(StringUtils.isNoneBlank(userVO.getUsername())){
    criteria.andLike("username","%"+userVO.getUsername()+"%");
}
// 紧跟着的第一个select方法会被分页
List<User> userList = userMapper.selectAll(o);
//分页时，实际返回的结果list类型是Page<E>
PageInfo<User> info=new PageInfo<>(userList);
```

{% note info %} **重要提示**

只有紧跟在`PageHelper.startPage`方法后的 **第一个** Mybatis的 **查询（Select）**方法会被分页。

{% endnote %}