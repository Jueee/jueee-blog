---
title: SpringBoot 配置多个 Elasticsearch 集群
layout: info
commentable: true
date: 2022-01-18
mathjax: true
mermaid: true
tags: [SpringBoot,Database,ElasticSearch]
categories: 
- [Database,ElasticSearch]
- [Java,SpringBoot]
description: 
---

通过两种方式介绍配置多个 Elasticsearch 集群：

- SpringBoot 项目
- 普通 maven 项目

<!--more-->

### SpringBoot 项目

#### 引入依赖

在 pom.xml 中添加 ES 客户端依赖：

```xml
<dependency>
    <groupId>org.elasticsearch.client</groupId>
    <artifactId>elasticsearch-rest-client</artifactId>
    <version>${elasticsearch.version}</version>
</dependency>
<dependency>
    <groupId>org.elasticsearch.client</groupId>
    <artifactId>elasticsearch-rest-high-level-client</artifactId>
    <version>${elasticsearch.version}</version>
</dependency>
```

#### 配置文件

在 application.properties 配置文件中添加相关 ES 集群连接信息：

```properties
spring.data.elasticsearch.connect1.hosts=xxx.xxx.xxx.xxx:7000,xxx.xxx.xxx.xxx:7000,xxx.xxx.xxx.xxx:7000
spring.data.elasticsearch.connect1.username=xxx
spring.data.elasticsearch.connect1.password=xxx

spring.data.elasticsearch.connect2.hosts=xxx.xxx.xxx.org:9200,xxx.xxx.xxx.org:9200,xxx.xxx.xxx.org:9200
spring.data.elasticsearch.connect2.username=xxx
spring.data.elasticsearch.connect2.password=xxx
```

#### 配置类

提供一个配置类：

```java
import lombok.Getter;
import lombok.Setter;
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestClientBuilder;
import org.elasticsearch.client.RestHighLevelClient;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * ES集群配置
 */
@Setter
@Configuration
@ConfigurationProperties(prefix = "spring.data.elasticsearch")
public class ElasticsearchConfig {

    public static final String ES_CLIENT_1 = "es_client_1";
    public static final String ES_CLIENT_2 = "es_client_2";

    private Connect connect1;
    private Connect connect2;

    /**
     * 客户端1
     */
    @Bean(name = ES_CLIENT_1, destroyMethod = "close")
    public RestHighLevelClient restHighLevelClient1() {
        return getRestHighLevelClient(connect1);
    }

    /**
     * 客户端2
     */
    @Bean(name = ES_CLIENT_2, destroyMethod = "close")
    public RestHighLevelClient restHighLevelClient2() {
        return getRestHighLevelClient(connect2);
    }

    private RestHighLevelClient getRestHighLevelClient(Connect connect) {
        String[] hosts = connect.getHosts().split(",");
        HttpHost[] httpHosts = new HttpHost[hosts.length];
        for (int i = 0; i < hosts.length; i++) {
            httpHosts[i] = HttpHost.create(hosts[i]);
        }
        RestClientBuilder restClientBuilder = RestClient.builder(httpHosts);
        //配置身份验证
        final CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
        credentialsProvider.setCredentials(AuthScope.ANY, new UsernamePasswordCredentials(connect.getUsername(), connect.getPassword()));
        restClientBuilder.setHttpClientConfigCallback(httpClientBuilder -> httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider));
        return new RestHighLevelClient(restClientBuilder);
    }

    @Setter
    @Getter
    public static class Connect {
        private String hosts;
        private String username;
        private String password;
    }

}

```

#### 使用方法

使用方法示例：

```java
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.elasticsearch.client.RestHighLevelClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;

@Slf4j
@Service
public class SearchServiceImpl implements SearchService {

    @Autowired
    @Qualifier(ElasticsearchConfig.ES_CLIENT_1)
    private RestHighLevelClient esClient1;

    @Autowired
    @Qualifier(ElasticsearchConfig.ES_CLIENT_2)
    private RestHighLevelClient esClient2;
    
}

```

### 普通 Maven 项目

#### 配置文件

提供一个 elasticsearch.properties 配置文件，添加相关 ES 集群连接信息：

```properties
spring.data.elasticsearch.connect1.hosts=xxx.xxx.xxx.xxx:7000,xxx.xxx.xxx.xxx:7000,xxx.xxx.xxx.xxx:7000
spring.data.elasticsearch.connect1.username=xxx
spring.data.elasticsearch.connect1.password=xxx

spring.data.elasticsearch.connect2.hosts=xxx.xxx.xxx.org:9200,xxx.xxx.xxx.org:9200,xxx.xxx.xxx.org:9200
spring.data.elasticsearch.connect2.username=xxx
spring.data.elasticsearch.connect2.password=xxx
```

#### 配置类

提供一个配置类：

```java
import lombok.Getter;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestClientBuilder;
import org.elasticsearch.client.RestHighLevelClient;

import java.io.IOException;
import java.util.Properties;

/**
 * ES集群配置
 */
@Slf4j
public class ElasticsearchConfig {

    @Setter
    private static Connect connect1Connect = new Connect();
    @Setter
    private static Connect connect2Connect = new Connect();

    private static volatile RestHighLevelClient connect1EsClient;
    private static volatile RestHighLevelClient connect2EsClient;

    private static final byte[] CONNECT1_LOCK = new byte[0];
    private static final byte[] CONNECT2_LOCK = new byte[0];

    static {
        Properties props = new Properties();
        try {
            props.load(ElasticsearchConfig.class.getResourceAsStream("/elasticsearch.properties"));
        } catch (IOException e) {
            log.error("load elasticsearch config properties exception", e);
        }
        String connect1Host = props.getProperty("spring.data.elasticsearch.connect1.hosts");
        String connect1UserName = props.getProperty("spring.data.elasticsearch.connect1.username");
        String connect1Password = props.getProperty("spring.data.elasticsearch.connect1.password");
        connect1Connect.setHosts(connect1Host);
        connect1Connect.setUsername(connect1UserName);
        connect1Connect.setPassword(connect1Password);
        connect1EsClient = init(connect1Connect);
        String connect2Host = props.getProperty("spring.data.elasticsearch.connect2.hosts");
        String connect2UserName = props.getProperty("spring.data.elasticsearch.connect2.username");
        String connect2Password = props.getProperty("spring.data.elasticsearch.connect2.password");
        connect2Connect.setHosts(connect2Host);
        connect2Connect.setUsername(connect2UserName);
        connect2Connect.setPassword(connect2Password);
        connect2EsClient = init(connect2Connect);
    }

    /**
     * 初始化客户端
     */
    private static RestHighLevelClient init(Connect connect) {
        String[] hosts = connect.getHosts().split(",");
        HttpHost[] httpHosts = new HttpHost[hosts.length];
        for (int i = 0; i < hosts.length; i++) {
            httpHosts[i] = HttpHost.create(hosts[i]);
        }
        RestClientBuilder restClientBuilder = RestClient.builder(httpHosts);
        //配置身份验证
        final CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
        credentialsProvider.setCredentials(AuthScope.ANY, new UsernamePasswordCredentials(connect.getUsername(), connect.getPassword()));
        restClientBuilder.setHttpClientConfigCallback(httpClientBuilder -> httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider));
        return new RestHighLevelClient(restClientBuilder);
    }

    @Setter
    @Getter
    public static class Connect {
        private String hosts;
        private String username;
        private String password;
    }

    /**
     * 获取connect1集群客户端
     */
    public static RestHighLevelClient getConnect1EsClient() {
        if (connect1EsClient == null) {
            synchronized (CONNECT1_LOCK) {
                if (connect1EsClient == null) {
                    connect1EsClient = init(connect1Connect);
                    return connect1EsClient;
                }
            }
        }
        return connect1EsClient;
    }

    /**
     * 获取connect2集群客户端
     */
    public static RestHighLevelClient getConnect2EsClient() {
        if (connect2EsClient == null) {
            synchronized (CONNECT2_LOCK) {
                if (connect2EsClient == null) {
                    connect2EsClient = init(connect2Connect);
                    return connect2EsClient;
                }
            }
        }
        return connect2EsClient;
    }

}

```

#### 使用方式

```java
RestHighLevelClient connect1EsClient = ElasticsearchConfig.getConnect1EsClient();
RestHighLevelClient connect2EsClient = ElasticsearchConfig.getConnect2EsClient();
```

