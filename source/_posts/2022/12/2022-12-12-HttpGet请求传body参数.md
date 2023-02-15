---
title: HttpGet请求传body参数
layout: info
commentable: true
date: 2022-12-12
mathjax: true
mermaid: true
tags: [Apache,HttpComponents]
categories: 
- [Apache,HttpComponents]
- [Java,JavaJar]
description: 
---

elastic search 的请求是一个Get请求，入参在Body 中（Json格式）。

<!--more-->

### 处理方法

#### 引入httpclient 依赖

```xml
<!-- https://mvnrepository.com/artifact/org.apache.httpcomponents/httpclient -->
 <dependency>
     <groupId>org.apache.httpcomponents</groupId>
     <artifactId>httpclient</artifactId>
     <version>4.5.6</version>
 </dependency>
```

#### 定义一个HttpGet实体类

```java
import org.apache.http.client.methods.HttpEntityEnclosingRequestBase;
import java.net.URI;
/**
 * @author xf
 * @version 1.0.0
 * @ClassName HttpGetWithEntity
 * @Description TODO 定义一个带body的GET请求 继承 HttpEntityEnclosingRequestBase
 */
public class HttpGetWithEntity extends HttpEntityEnclosingRequestBase {
    private final static String METHOD_NAME = "GET";

    @Override
    public String getMethod() {
        return METHOD_NAME;
    }
    public HttpGetWithEntity() {
        super();
    }
    public HttpGetWithEntity(final URI uri) {
        super();
        setURI(uri);
    }
    HttpGetWithEntity(final String uri) {
        super();
        setURI(URI.create(uri));
    }

}
```

#### HttpGet请求公共方法

```java
/**
  * 发送get请求，参数为json
  * @param url
  * @param param
  * @param encoding
  * @return
  * @throws Exception
  */
public static String sendJsonByGetReq(String url, String param, String encoding) throws Exception {
    String body = "";
    //创建httpclient对象
    CloseableHttpClient client = HttpClients.createDefault();
    HttpGetWithEntity httpGetWithEntity = new HttpGetWithEntity(url);
    HttpEntity httpEntity = new StringEntity(param, ContentType.APPLICATION_JSON);
    httpGetWithEntity.setEntity(httpEntity);
    //执行请求操作，并拿到结果（同步阻塞）
    CloseableHttpResponse response = client.execute(httpGetWithEntity);
    //获取结果实体
    HttpEntity entity = response.getEntity();
    if (entity != null) {
        //按指定编码转换结果实体为String类型
        body = EntityUtils.toString(entity, encoding);
    }
    //释放链接
    response.close();
    return body;
}
```
