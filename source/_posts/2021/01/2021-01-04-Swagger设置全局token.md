---
title: Swagger设置全局token
layout: info
commentable: true
date: 2021-01-04
mathjax: true
mermaid: true
tags: [Java,JavaJar,RESTful]
categories: [Java,JavaJar]
description: 
---

swagger是一个很使用的工具，但正常使用时，我们的接口需要登陆才能访问的。即登陆时，要传一个登陆后的token才能访问的。 

那这个怎么设置，才可以让所有接口都允许登陆后访问呢?

<!--more-->

### 出现问题

![image-20210106113200793](/images/2021/01/image-20210106113200793.png)

### 解决问题

`SwaggerConfig` 配置类中增加方法：

```java
    private List<ApiKey> securitySchemes() {
        List<ApiKey> apiKeyList= new ArrayList();
        apiKeyList.add(new ApiKey("Authorization", "Authorization", "header"));
        return apiKeyList;
    }
```

注册方法：

```java
@Bean
public Docket docket(){
    return new Docket(DocumentationType.SWAGGER_2)
            .apiInfo(apiInfo())
            .groupName("System") // 配置分组
            .select()
            .apis(RequestHandlerSelectors.basePackage("com.test.system"))
            .paths(PathSelectors.any())
            .build()
            .securitySchemes(securitySchemes())
            .pathMapping("/");
}
```

### 解决效果

访问：http://127.0.0.1:8181/swagger-ui.html，进行登录。

![image-20210106113515400](/images/2021/01/image-20210106113515400.png)

插入 token 字符串。

![image-20210106113342562](/images/2021/01/image-20210106113342562.png)

传入成功的效果图：

![image-20210106113255981](/images/2021/01/image-20210106113255981.png)

接口访问成功效果图：

![image-20210106113224686](/images/2021/01/image-20210106113224686.png)