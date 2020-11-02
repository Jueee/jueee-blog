---
title: SpringBoot集成Druid
layout: info
commentable: true
date: 2020-10-30
mathjax: true
mermaid: true
tags: [Java,JavaJar,Alibaba]
categories: 
- [Java,JavaJar]
- [Java,SpringBoot]
description: 
---

Springboot集成Druid有两种方案：

- 在POM中直接配置druid-spring-boot-starter，不用写任何代码。
- 配置druid，写几行代码，可以加入。

<!--more-->

### 使用druid-spring-boot-starter

Druid Spring Boot Starter 用于帮助你在Spring Boot项目中轻松集成Druid数据库连接池和监控。

- GitHub：https://github.com/alibaba/druid/tree/master/druid-spring-boot-starter

#### 引入 Jar

```xml
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>druid-spring-boot-starter</artifactId>
    <version>1.2.1</version>
</dependency>
```

#### 配置文件

配置文件 application.properties：

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/test?serverTimezone=UTC
spring.datasource.username=xxx
spring.datasource.password=xxx
spring.datasource.driverClassName=com.mysql.cj.jdbc.Driver

#config druid
#连接池的设置
#初始化时建立物理连接的个数
spring.datasource.druid.initial-size=5
#最小连接池数量
spring.datasource.druid.min-idle=5
#最大连接池数量 maxIdle已经不再使用
spring.datasource.druid.max-active=20
#获取连接时最大等待时间，单位毫秒
spring.datasource.druid.max-wait=60000
#申请连接的时候检测，如果空闲时间大于timeBetweenEvictionRunsMillis，执行validationQuery检测连接是否有效。
spring.datasource.druid.test-while-idle=true
#既作为检测的间隔时间又作为testWhileIdel执行的依据
spring.datasource.druid.time-between-eviction-runs-millis=60000
#销毁线程时检测当前连接的最后活动时间和当前时间差大于该值时，关闭当前连接
spring.datasource.druid.min-evictable-idle-time-millis=30000
#用来检测连接是否有效的sql 必须是一个查询语句
#mysql中为 select 'x'
#oracle中为 select 1 from dual
spring.datasource.druid.validation-query=select 'x'
#申请连接时会执行validationQuery检测连接是否有效,开启会降低性能,默认为true
spring.datasource.druid.test-on-borrow=false
#归还连接时会执行validationQuery检测连接是否有效,开启会降低性能,默认为true
spring.datasource.druid.test-on-return=false
#当数据库抛出不可恢复的异常时,抛弃该连接
#spring.datasource.druid.exception-sorter=true
#是否缓存preparedStatement,mysql5.5+建议开启
#spring.datasource.druid.pool-prepared-statements=true
#当值大于0时poolPreparedStatements会自动修改为true
spring.datasource.druid.max-pool-prepared-statement-per-connection-size=20
#配置扩展插件
spring.datasource.druid.filters=stat,wall
#通过connectProperties属性来打开mergeSql功能；慢SQL记录
spring.datasource.druid.connection-properties=druid.stat.mergeSql=true;druid.stat.slowSqlMillis=500
#合并多个DruidDataSource的监控数据
spring.datasource.druid.use-global-data-source-stat=true

# 加入如下配置，实现验证登录
## Druid WebStatFilter配置，说明请参考Druid Wiki，配置_配置WebStatFilter
spring.datasource.druid.web-stat-filter.enabled=true
spring.datasource.druid.web-stat-filter.url-pattern=/*
spring.datasource.druid.web-stat-filter.exclusions=*.gif,*.png,*.jpg,*.html,*.js,*.css,*.ico,/druid/*
# Druid StatViewServlet配置，说明请参考Druid Wiki，配置_StatViewServlet配置
spring.datasource.druid.stat-view-servlet.enabled=true
spring.datasource.druid.stat-view-servlet.url-pattern=/druid/*
spring.datasource.druid.stat-view-servlet.reset-enable=true
#设置访问druid监控页的账号和密码,默认没有
spring.datasource.druid.stat-view-servlet.login-username=admin
spring.datasource.druid.stat-view-servlet.login-password=admin
spring.datasource.druid.stat-view-servlet.allow=
spring.datasource.druid.stat-view-servlet.deny=
```

#### 访问 druid

输入：[http://localhost:8080/druid/](http://localhost:8080/druid/)，查看Druid监控面板。

![image-20201030161817190](/images/2020/10/image-20201030161817190.png)

### 配置druid

#### 引入 Jar

```xml
<dependency>
	<groupId>com.alibaba</groupId>
	<artifactId>druid</artifactId>
	<version>1.2.1</version>
</dependency>
```

#### 配置文件

配置文件 application.properties：

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/test?serverTimezone=UTC
spring.datasource.username=xxx
spring.datasource.password=xxx
spring.datasource.driverClassName=com.mysql.cj.jdbc.Driver
```

#### 配置 druid

配置 druid 使其配置的参数生效。

新建一个类：DruidConfig，注意包的引入：

```java
import com.alibaba.druid.pool.DruidDataSource;
import com.alibaba.druid.support.http.StatViewServlet;
import com.alibaba.druid.support.http.WebStatFilter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.boot.web.servlet.ServletRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.sql.DataSource;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

@Configuration
public class DruidConfig {
    @Bean
    @ConfigurationProperties(prefix = "spring.datasource")
    public DataSource getDataSource(){
        return new DruidDataSource();
    }
    // 配置Druid监控
    // 配置一个管理后台的Servlet
    @Bean
    public ServletRegistrationBean statViewServlet(){
        ServletRegistrationBean bean = new ServletRegistrationBean(new StatViewServlet(), "/druid/*");
        Map<String,String> initParams=new HashMap<>();
        initParams.put("loginUsername","admin");
        initParams.put("loginPassword","admin");
        initParams.put("allow","");  // 默认就是允许所有访问
       // initParams.put("deny","127.0.0.1"); // 拒绝哪个网址访问，优先级大于allow
        bean.setInitParameters(initParams);
        return bean;
    }
    //2、配置一个web监控的filter
    @Bean
    public FilterRegistrationBean webStatFilter(){
        FilterRegistrationBean bean = new FilterRegistrationBean();
        bean.setFilter(new WebStatFilter());
        Map<String,String> initParams = new HashMap<>();
        // 配置不拦截哪些请求
        initParams.put("exclusions","*.js,*.css,/druid/*");
        bean.setInitParameters(initParams);
        // 配置拦截所有请求
        bean.setUrlPatterns(Arrays.asList("/*"));
        return  bean;
    }
}
```

#### 访问 druid

输入：[http://localhost:8080/druid/](http://localhost:8080/druid/)，观察Druid监控面板。

![image-20201030161817190](/images/2020/10/image-20201030161817190.png)