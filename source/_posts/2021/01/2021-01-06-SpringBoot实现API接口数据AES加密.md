---
title: SpringBoot实现API接口数据AES加密
layout: info
commentable: true
date: 2021-01-06
mathjax: true
mermaid: true
tags: [Java,SpringBoot,AES]
categories: [Java,SpringBoot]
description: 
---

### 接口安全

放到互联网上的接口数据，直接采用明文的话，就很容易被抓包，然后进行修改或者被恶意植入木马，本文研究一下怎么样对接口进行数据加密。

接口加密的作用：

1. 防止恶意调用攻击
2. 防止篡改信息攻击
3. 防拦截攻击，数据被截取后进行修改后重新放回去
4. 防止数据泄漏攻击

<!--more-->

{% note info %}

抓包（packet capture）就是将网络传输发送与接收的数据包进行截获、重发、编辑、转存等操作，也用来检查网络安全。抓包也经常被用来进行数据截取等。

{% endnote %}

### 项目代码

本文完整项目代码位于：[https://github.com/Jueee/blog-project/tree/main/java-web-secret](https://github.com/Jueee/blog-project/tree/main/java-web-secret)

### 编写代码

#### POM文件

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <optional>true</optional>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>
```

#### 加密解密工具类

```java
import lombok.extern.slf4j.Slf4j;
import org.apache.tomcat.util.codec.binary.Base64;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;

/**
 * AES加密解密
 */
@Slf4j
public class AesUtils {

    private static final String KEY_ALGORITHM = "AES";

    private static final String DEFAULT_CIPHER_ALGORITHM = "AES/ECB/PKCS5Padding";// 默认的加密算法

    /**
     * AES 加密操作
     * @param content  待加密内容
     * @param password 加密密码
     * @return String 返回Base64转码后的加密数据
     */
    public static String encrypt(String content, String password) {
        try {
            // 创建密码器
            final Cipher cipher = Cipher.getInstance(DEFAULT_CIPHER_ALGORITHM);
            // 设置为UTF-8编码
            final byte[] byteContent = content.getBytes("utf-8");
            // 初始化为加密模式的密码器
            cipher.init(Cipher.ENCRYPT_MODE, getSecretKey(password));
            // 加密
            final byte[] result = cipher.doFinal(byteContent);
            // 通过Base64转码返回
            return Base64.encodeBase64String(result);
        } catch (Exception ex) {
            log.error(ex.getMessage(), ex);
        }
        return "";
    }

    /**
     * AES 解密操作
     *
     * @param content
     * @param password
     * @return String
     */
    public static String decrypt(String content, String password) {
        try {
            // 实例化
            final Cipher cipher = Cipher.getInstance(DEFAULT_CIPHER_ALGORITHM);
            // 使用密钥初始化，设置为解密模式
            cipher.init(Cipher.DECRYPT_MODE, getSecretKey(password));
            // 执行操作
            final byte[] result = cipher.doFinal(Base64.decodeBase64(content));
            // 采用UTF-8编码转化为字符串
            return new String(result, "utf-8");
        } catch (final Exception ex) {
            log.error(ex.getMessage(), ex);
        }
        return "";
    }

    /**
     * 生成加密秘钥
     *
     * @param password 加密的密码
     * @return SecretKeySpec
     */
    private static SecretKeySpec getSecretKey(final String password) {
        // 返回生成指定算法密钥生成器的 KeyGenerator 对象
        KeyGenerator kg = null;
        try {
            kg = KeyGenerator.getInstance(KEY_ALGORITHM);
            // AES 要求密钥长度为 128
            kg.init(128, new SecureRandom(password.getBytes()));
            // 生成一个密钥
            final SecretKey secretKey = kg.generateKey();
            // 转换为AES专用密钥
            return new SecretKeySpec(secretKey.getEncoded(), KEY_ALGORITHM);
        } catch (final NoSuchAlgorithmException ex) {
            log.error(ex.getMessage(), ex);
        }
        return null;
    }

    /**
     * 根据密钥，生成 aes.key
     * @param password
     * @return
     */
    public static String getKeyByPass(String password) {
        SecretKeySpec keySpec = getSecretKey(password);
        byte[] b = keySpec.getEncoded();
        return byteToHexString(b);
    }
    /**
     * byte数组转化为16进制字符串
     * @param bytes
     * @return
     */
    public static String byteToHexString(byte[] bytes) {
        StringBuffer sb = new StringBuffer();
        for (int i = 0; i < bytes.length; i++) {
            String strHex=Integer.toHexString(bytes[i]);
            if(strHex.length() > 3) {
                sb.append(strHex.substring(6));
            } else {
                if(strHex.length() < 2) {
                    sb.append("0" + strHex);
                } else {
                    sb.append(strHex);
                }
            }
        }
        return sb.toString();
    }

}
```

#### 加密注解

```java
import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * 返回对body加密,针对类跟方法
 */
@Target({ ElementType.METHOD, ElementType.TYPE })
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface ResponseEncrypt {

    /**
     * 返回对body加密，默认是true
     * @return boolean
     */
    boolean value() default true;
}
```

#### 加密判断类

```java
import com.jueee.annotations.ResponseEncrypt;
import org.springframework.core.MethodParameter;

/**
 * 是否需要加密解密
 */
public class NeedDecrypt {

    /**
     * 判断是否需要加密
     *
     * @param returnType
     * @return boolean
     */
    public static boolean needEncrypt(MethodParameter returnType) {
        boolean encrypt = false;
        // 获取类上的注解
        final boolean classPresentAnno = returnType.getContainingClass().isAnnotationPresent(ResponseEncrypt.class);
        // 获取方法上的注解
        final boolean methodPresentAnno = returnType.getMethod().isAnnotationPresent(ResponseEncrypt.class);
        if (classPresentAnno) {
            // 类上标注的是否需要加密
            encrypt = returnType.getContainingClass().getAnnotation(ResponseEncrypt.class).value();
            // 类不加密，所有都不加密
            if (!encrypt) {
                return false;
            }
        }
        if (methodPresentAnno) {
            // 方法上标注的是否需要加密
            encrypt = returnType.getMethod().getAnnotation(ResponseEncrypt.class).value();
        }
        return encrypt;
    }

}
```

#### 加密拦截

```java
import com.jueee.bean.ResponseBean;
import com.jueee.utils.AesUtils;
import com.jueee.utils.NeedDecrypt;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.MethodParameter;
import org.springframework.http.MediaType;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.http.server.ServerHttpRequest;
import org.springframework.http.server.ServerHttpResponse;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.servlet.mvc.method.annotation.ResponseBodyAdvice;

/**
 * 对接口数据进行加密
 */
@ControllerAdvice
public class ResponseEncryptAdvice implements ResponseBodyAdvice<Object> {

    @Value("${module.boots.response.aes.key}")
    private String key;

    @Override
    public boolean supports(MethodParameter returnType, Class<? extends HttpMessageConverter<?>> converterType) {
        return true;
    }

    /**
     * 在写入之前更改body的值
     * @param body
     * @param returnType
     * @param selectedContentType
     * @param selectedConverterType
     * @param request
     * @param response
     * @return
     * @return
     */
    @SuppressWarnings({ "unchecked", "rawtypes" })
    @Override
    public Object beforeBodyWrite(Object body, MethodParameter returnType, MediaType selectedContentType,
                                  Class<? extends HttpMessageConverter<?>> selectedConverterType, ServerHttpRequest request,
                                  ServerHttpResponse response) {
        // 判断是否需要加密
        final boolean encrypt = NeedDecrypt.needEncrypt(returnType);
        if (!encrypt) {
            return body;
        } else {
            // 如果body是属于ResponseBean类型,只需要对data里面的数据进行加密即可
            if (body instanceof ResponseBean) {
                final ResponseBean responseBean = (ResponseBean) body;
                final Object data = responseBean.getData();
                if (data == null) {
                    return body;
                } else {
                    responseBean.setData(AesUtils.encrypt(data.toString(), key));
                    return responseBean;
                }
            } else {
                return body;
            }
        }
    }

}
```

#### 配置密钥

```properties
module.boots.response.aes.key: 6162382d323fb399fc202a5aca55336a
```

### 测试代码

#### 数据接口

```java
import com.jueee.annotations.ResponseEncrypt;
import com.jueee.bean.GetEncryptVO;
import com.jueee.bean.ResponseBean;
import com.jueee.utils.AesUtils;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * 加密数据接口
 */
@Slf4j
@SuppressWarnings("deprecation")
@RestController
@RequestMapping("test")
public class SecretController {

    @Value("${module.boots.response.aes.key}")
    private String key;

    /**
     * 获取加密数据
     */
    @GetMapping(value = "/getEncrypt", produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    @ResponseEncrypt
    public ResponseBean getEncrypt() {
        final GetEncryptVO vo = new GetEncryptVO();
        vo.setId("123456");
        vo.setUserName("Jueee");
        return ResponseBean.success(vo);
    }

    /**
     * 获取解密数据
     */
    @GetMapping(value = "/getDecrypt", produces = MediaType.APPLICATION_JSON_UTF8_VALUE)
    public ResponseBean getDecrypt(@RequestParam(value = "content") String content) {
        log.info("content:"+content);
        final String str = AesUtils.decrypt(content, key);
        log.info("decrypt:"+str);
        return ResponseBean.success(str);
    }

}
```

#### 测试接口

```java
import com.jueee.utils.HttpClient4;
import lombok.extern.slf4j.Slf4j;
import org.json.JSONObject;
import org.junit.jupiter.api.Test;

import java.net.URLEncoder;

@Slf4j
class SecretControllerTest {

    @Test
    public void test() throws Exception {
        String encrypt = HttpClient4.doGet("http://127.0.0.1:8080/test/getEncrypt");
        log.info(encrypt);
        JSONObject jsonObject = new JSONObject(encrypt);
        log.info(jsonObject.getString("data"));
        String data = jsonObject.getString("data");
        String decrypt = HttpClient4.doGet("http://127.0.0.1:8080/test/getDecrypt?content="+ URLEncoder.encode(data, "UTF-8"));
        log.info(decrypt);
    }
}
```

输出：

```
- {"code":200,"msg":"成功","data":"FJscqvyWFReJftsv9WxkIFpHq8Y/GLBAi4tbv/qyAqLMeCAr8fpaJBQ83F4Owe1S"}
- FJscqvyWFReJftsv9WxkIFpHq8Y/GLBAi4tbv/qyAqLMeCAr8fpaJBQ83F4Owe1S
- {"code":200,"msg":"GetEncryptVO(id=123456, userName=Jueee)","data":null}
```

#### 测试工具类

```java
import org.junit.jupiter.api.Test;

class AesUtilsTest {

    private String aesKey = "6162382d323fb399fc202a5aca55336a";

    @Test // 生成 AES Key
    public void test(){
        System.out.println(AesUtils.getKeyByPass("Jueee"));
    }
    
    @Test // AES 解密
    public void testDecrypt(){
        final String str = "FJscqvyWFReJftsv9WxkIFpHq8Y/GLBAi4tbv/qyAqLMeCAr8fpaJBQ83F4Owe1S";
        System.out.println(AesUtils.decrypt(str, aesKey));
    }
}
```

输出：

```
6162382d323fb399fc202a5aca55336a
GetEncryptVO(id=123456, userName=Jueee)
```

