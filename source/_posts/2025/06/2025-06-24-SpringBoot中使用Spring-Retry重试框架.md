---
title: SpringBoot中使用Spring-Retry重试框架
layout: info
commentable: true
date: 2025-06-24
mathjax: true
mermaid: true
tags: [SpringBoot]
categories: 
- [Java,JavaJar]
- [Java,SpringBoot]
description: 
---

-XX:G1HeapRegionSize=32M

### 引入依赖

确保在你的项目中添加了 Spring Retry 依赖：

```xml
<dependency>
    <groupId>org.springframework.retry</groupId>
    <artifactId>spring-retry</artifactId>
</dependency>
```

<!--more-->

### 启用配置

在你的 Spring 配置类中启用重试功能：

```java
@Configuration
@EnableRetry
public class RetryConfig {
}
```

### 为方法加入重试

为了在触发 JSONException 时暂停两分钟后重新请求，我们可以使用重试机制。以下是修改后的代码：

```java
import org.springframework.retry.annotation.Backoff;
import org.springframework.retry.annotation.Retryable;

public class FeatureOperate {

    @Retryable(value = {JSONException.class}, maxAttempts = 2, backoff = @Backoff(delay = 120000))
    private boolean insert(params……) {
        String res = null;
        try {
            res = HttpClient4Utils.httpPost(operateUrl, headerMap, paramJson.toJSONString(), Consts.UTF_8);
            JSONObject jsonObject = JSONObject.parseObject(res);
        } catch (JSONException e) {
            log.error("[res]{} [Message]{} [paramJson]{}", res, e.getMessage(), paramJson, e);
            throw e; // 重新抛出异常，触发重试
        } catch (Exception e) {
            log.error("[res]{} [Message]{} [paramJson]{}", res, e.getMessage(), paramJson, e);
        }
        return false;
    }
}
```

主要修改如下：

1. 添加了 `@Retryable` 注解到方法上：
   - `value = {JSONException.class}`: 指定要重试的异常类型。
   - `maxAttempts = 2`: 设置最大尝试次数为2（初始尝试 + 1次重试）。
   - `backoff = @Backoff(delay = 120000)`: 设置重试延迟为120000毫秒（2分钟）。

2. 在 catch JSONException 的块中，我们重新抛出异常，以触发重试机制。

3. 这样，当发生 JSONException 时，方法将等待2分钟后重新尝试。如果第二次尝试仍然失败，则方法将返回 false。

请注意，这种方法会增加方法的执行时间。如果这是一个对时间敏感的操作，你可能需要考虑其他的错误处理策略。
