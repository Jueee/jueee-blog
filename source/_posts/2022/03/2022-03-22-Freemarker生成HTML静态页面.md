---
title: Freemarker生成HTML静态页面
layout: info
commentable: true
date: 2022-03-22
mathjax: true
mermaid: true
tags: [Apache,FreeMarker]
categories: [Apache,FreeMarker]
description: 
---

有时为了减轻了服务器的压力和提高页面的响应速度，需要静态页面。

下面介绍使用 Freemarker生成HTML静态页面的方法。

<!--more-->

### 引入依赖

```xml
<dependency>
   <groupId>org.springframework.boot</groupId>
   <artifactId>spring-boot-starter-freemarker</artifactId>
</dependency>
```

### 配置 Freemarker

```properties
spring.freemarker.enabled=true
spring.freemarker.cache=false
spring.freemarker.template-loader-path=classpath:/templates/
spring.freemarker.settings.template_update_delay=0
spring.freemarker.charset=UTF-8
spring.freemarker.check-template-location=true
spring.freemarker.content-type=text/html
spring.freemarker.expose-request-attributes=true
spring.freemarker.expose-session-attributes=true
spring.freemarker.request-context-attribute=request
spring.freemarker.suffix=.ftl
```

### 调试 HTML 方法

```java
@Controller
public class InfoController {

    @RequestMapping(value = "/")
    public  String main() {
        return "redirect:/info";
    }


    @RequestMapping(value = "/info")
    public  String info(HttpServletRequest request, HttpServletResponse response, ModelMap m) {
        Info info = // 获取注入对象值
        m.put("info", info);
        return "view/info";
    }

}
```

### 保存 HTML 方法

```java
public static void saveHtmlFile(File emlFile,String htmlIndex) {
    try {
        String ftlPath = "src\\main\\resources\\templates\\view";
        Configuration configuration = new Configuration();
        configuration.setDirectoryForTemplateLoading(new File(ftlPath));
        configuration.setDefaultEncoding("UTF-8");
        // 获取或创建一个模版。
        Template template = configuration.getTemplate("info.ftl");
        //设置文件输入流编码，不然生成的html文件会中文乱码
        FileWriterWithEncoding out = new FileWriterWithEncoding(htmlIndex, "UTF-8");
        // 将页面中要展示的数据放入一个map中
        HashMap<String, Object> dataMap = new HashMap<String, Object>();
        Info info = new Info(); // 获取对象值
        dataMap.put("info", info);
        //将map中的数据输入到个模板文件中并遍历出来，最后再将整个模板的数据写入到html中。
        template.process(dataMap, out);
        out.close();
    } catch (Exception e) {
        log.error(e.getMessage()+"--"+emlFile.getAbsolutePath());
    }
}
```

