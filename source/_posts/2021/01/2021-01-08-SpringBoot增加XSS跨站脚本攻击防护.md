---
title: SpringBoot增加XSS跨站脚本攻击防护
layout: info
commentable: true
date: 2021-01-08
mathjax: true
mermaid: true
tags: [Java,SpringBoot,XSS]
categories: [Java,SpringBoot]
description: 
---

### XSS原理

XSS攻击的原理是利用前后端校验不严格，用户将攻击代码植入到数据中提交到了后台，当这些数据在网页上被其他用户查看的时候触发攻击。

举例：用户提交表单时把地址写成：

```
杭州市<script>for(var i=0;i<9999;i++){alert(i)}</script>
```

上面的数据如果没有在后台做处理，当数据被展示到网页上的时候，会在网页上弹出N个alert框，当然实际攻击肯定是比这个要复杂的多的。

<!--more-->

### 项目代码

本文完整项目代码位于：[https://github.com/Jueee/blog-project/tree/main/java-web-xss](https://github.com/Jueee/blog-project/tree/main/java-web-xss)

### XSS 攻击示例

#### 代码示例

引入依赖：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
```

Controller 如下：

```java
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@Slf4j
@Controller
public class DemoController {

    @RequestMapping("/demo")
    public String demo(HttpServletRequest request, HttpServletResponse response, ModelMap m) {
        log.info("into demo page");
        return "demo";
    }

    @ResponseBody
    @RequestMapping("/demoAction")
    public String demoAction(@RequestParam(value = "name") String name,
                             HttpServletRequest request, HttpServletResponse response, ModelMap m) {
        log.info("name:"+name);
        return "name is:"+name;
    }
}
```

前端页面如下：

```html
<form action="demoAction" method="post" name="demoForm">
    Name: <input type="text" name="name" value="demo"/>
    <input type="submit" value="Submit" />
</form>
```

#### 正常效果

1. 访问 http://127.0.0.1:8080/demo

   ![image-20210108184256800](/images/2021/01/image-20210108184256800.png)

2. 点击提交：

   ![image-20210108184309976](/images/2021/01/image-20210108184309976.png)

#### 攻击效果

1. 访问 http://127.0.0.1:8080/demo，并输入 `test<script>alert('Attack!')</script>`

   ![image-20210108184403240](/images/2021/01/image-20210108184403240.png)

2. 点击提交：

   ![image-20210108184500891](/images/2021/01/image-20210108184500891.png)

### SpringBoot 防护

#### 添加依赖

```xml
<!-- https://mvnrepository.com/artifact/org.apache.commons/commons-lang3 -->
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-lang3</artifactId>
    <version>3.11</version>
</dependency>
<!-- https://mvnrepository.com/artifact/org.jsoup/jsoup -->
<dependency>
    <groupId>org.jsoup</groupId>
    <artifactId>jsoup</artifactId>
    <version>1.13.1</version>
</dependency>
```

#### Filter 类

```java
import org.apache.commons.lang3.StringUtils;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class XssFilter implements Filter {

    private List<String> excludes = new ArrayList<>();

    private boolean enabled = false;

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        String strExcludes = filterConfig.getInitParameter("excludes");
        String strEnabled = filterConfig.getInitParameter("enabled");
        //将不需要xss过滤的接口添加到列表中
        if(StringUtils.isNotEmpty(strExcludes)){
            String[] urls = strExcludes.split(",");
            for(String url:urls){
                excludes.add(url);
            }
        }
        if(StringUtils.isNotEmpty(strEnabled)){
            enabled = Boolean.valueOf(strEnabled);
        }
    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) servletRequest;

        //如果该访问接口在排除列表里面则不拦截
        if(isExcludeUrl(request.getServletPath())){
            filterChain.doFilter(servletRequest,servletResponse);
            return;
        }
        //拦截该url并进行xss过滤
        XssHttpServletRequestWrapper xssHttpServletRequestWrapper = new XssHttpServletRequestWrapper(request);
        filterChain.doFilter(xssHttpServletRequestWrapper,servletResponse);

    }

    @Override
    public void destroy() {

    }

    private boolean isExcludeUrl(String urlPath){
        if(!enabled){
            //如果xss开关关闭了，则所有url都不拦截
            return true;
        }
        if(excludes==null||excludes.isEmpty()){
            return false;
        }

        String url = urlPath;
        for(String pattern:excludes){
            Pattern p = Pattern.compile("^"+pattern);
            Matcher m = p.matcher(url);
            if(m.find()){
                return true;
            }
        }
        return false;
    }
}
```

#### XSS 过滤包装类

增加一个XssHttpServletRequestWrapper 类,这个类重写了获取参数的方法，在获取参数时做了XSS 替换处理

```java
import lombok.extern.slf4j.Slf4j;
        import org.apache.commons.lang3.StringUtils;
        import org.jsoup.Jsoup;
        import org.jsoup.safety.Whitelist;

        import javax.servlet.http.HttpServletRequest;
        import javax.servlet.http.HttpServletRequestWrapper;

/**
 * xss过滤包装类
 */
@Slf4j
public class XssHttpServletRequestWrapper extends HttpServletRequestWrapper {
    /**
     * Constructs a request object wrapping the given request.
     * @param request The request to wrap
     * @throws IllegalArgumentException if the request is null
     */
    public XssHttpServletRequestWrapper(HttpServletRequest request) {
        super(request);
    }

    @Override
    public String getHeader(String name) {
        String strHeader = super.getHeader(name);
        if(StringUtils.isEmpty(strHeader)){
            return strHeader;

        }
        return Jsoup.clean(super.getHeader(name),Whitelist.relaxed());
    }

    @Override
    public String getParameter(String name) {
        String strParameter = super.getParameter(name);
        if(StringUtils.isEmpty(strParameter)){
            return strParameter;
        }
        return Jsoup.clean(super.getParameter(name),Whitelist.relaxed());
    }


    @Override
    public String[] getParameterValues(String name) {
        String[] values = super.getParameterValues(name);
        if(values==null){
            return values;
        }
        int length = values.length;
        String[] escapseValues = new String[length];
        for(int i = 0;i<length;i++){
            //过滤一切可能的xss攻击字符串
            escapseValues[i] = Jsoup.clean(values[i], Whitelist.relaxed()).trim();
            if(!StringUtils.equals(escapseValues[i],values[i])){
                log.info("xss字符串过滤前："+values[i]+"\t"+"过滤后："+escapseValues[i]);
            }
        }
        return escapseValues;
    }
}
```

#### 配置加载类

SpringBoot里面增加一个configuration配置，把Filter类配置上去

```java
import com.jueee.utils.XssFilter;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.servlet.DispatcherType;
import java.util.HashMap;
import java.util.Map;

/**
 * 设置跨站脚本过滤
 */
@Configuration
public class FilterConfig {
    @Value("${xss.enabled}")
    private String enabled;

    @Value("${xss.excludes}")
    private String excludes;

    @Value("${xss.urlPatterns}")
    private String urlPatterns;

    @Bean
    public FilterRegistrationBean xssFilterRegistration(){
        FilterRegistrationBean registrationBean = new FilterRegistrationBean();
        registrationBean.setDispatcherTypes(DispatcherType.REQUEST);
        registrationBean.setFilter(new XssFilter());
        registrationBean.addUrlPatterns(StringUtils.split(urlPatterns,","));
        registrationBean.setName("XssFilter");
        registrationBean.setOrder(9999);
        Map<String,String> initParameters = new HashMap<>();
        initParameters.put("excludes",excludes);
        initParameters.put("enabled",enabled);
        registrationBean.setInitParameters(initParameters);
        return registrationBean;
    }
}
```

#### 配置文件

在application.properties或者application.yml里面增加一些开关配置，可以忽略某些接口提交的数据或者关闭xss过滤

```properties
#xss攻击拦截
xss.enabled=true
xss.excludes=
xss.urlPatterns=/*
```

#### 防护效果

访问 http://127.0.0.1:8080/demo，输入  `test<script>alert('Attack!')</script>` ，并提交：

![image-20210108185026725](/images/2021/01/image-20210108185026725.png)

日志：

```
: into demo page
: xss字符串过滤前：test<script>alert('Attack!')</script>	过滤后：test
: name:test
```

