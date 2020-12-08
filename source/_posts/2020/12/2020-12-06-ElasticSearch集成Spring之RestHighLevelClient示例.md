---
title: ElasticSearch集成Spring之RestHighLevelClient示例
layout: info
commentable: true
date: 2020-12-06
mathjax: true
mermaid: true
tags: [ElasticSearch,Java,JavaClass,Spring]
categories: 
- [ElasticSearch]
- [Java,JavaClass]
description: 
---

### RestHighLevelClient

RestHighLevelClient 是官方指定的连接API。

另外一个是TransportClient，但是TransportClient这个是已经废弃不用的，所以会在ES8.0之后完全移除，也就是说8.0之后就无法使用了。

引入依赖：

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

<!--more-->

### 配置连接

配置文件 `application.properties`：

```properties
spring.data.elasticsearch.host=192.168.10.31:192.168.10.32:192.168.10.33:192.168.10.34
spring.data.elasticsearch.port=9200
spring.data.elasticsearch.username=elastic
spring.data.elasticsearch.password=123456
```

配置 Java 类：

```java
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestHighLevelClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.DisposableBean;
import org.springframework.beans.factory.FactoryBean;
import org.springframework.beans.factory.InitializingBean;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ElasticsearchConfiguration implements FactoryBean<RestHighLevelClient>, InitializingBean, DisposableBean {
    private static final Logger LOGGER = LoggerFactory.getLogger(ElasticsearchConfiguration.class);

    @Value("${spring.data.elasticsearch.host}")
    private String host;
    @Value("${spring.data.elasticsearch.port}")
    private int port;
    @Value("${spring.data.elasticsearch.username}")
    private String username;
    @Value("${spring.data.elasticsearch.password}")
    private String password;

    private RestHighLevelClient restHighLevelClient;

    @Override
    public void destroy() throws Exception {
        try {
            LOGGER.info("Closing elasticSearch client");
            if (restHighLevelClient != null) {
                restHighLevelClient.close();
            }
        } catch (final Exception e) {
            LOGGER.error("Error closing ElasticSearch client: ", e);
        }
    }

    @Override
    public RestHighLevelClient getObject() throws Exception {
        return restHighLevelClient;
    }

    @Override
    public Class<RestHighLevelClient> getObjectType() {
        return RestHighLevelClient.class;
    }

    @Override
    public boolean isSingleton() {
        return false;
    }

    @Override
    public void afterPropertiesSet() throws Exception {
        buildClient();
    }

    protected void buildClient() {
        final CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
        credentialsProvider.setCredentials(AuthScope.ANY, new UsernamePasswordCredentials(username, password));
        HttpHost[] hostArray = new HttpHost[host.split(":").length];
        int index = 0;
        for (String httpHost : host.split(":")) {
            hostArray[index] = new HttpHost(httpHost, port);
            index++;
        }
        restHighLevelClient = new RestHighLevelClient(RestClient.builder(hostArray).setHttpClientConfigCallback(
                httpClientBuilder -> httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider)));
        LOGGER.info("elasticSearch client buildClient...");
    }
}
```

### 索引相关

判断索引是否存在：

```java
GetIndexRequest request = new GetIndexRequest(indexName);
boolean exists = restHighLevelClient.indices().exists(request, RequestOptions.DEFAULT);
```

列出所有索引：

```java
GetAliasesRequest request = new GetAliasesRequest();
GetAliasesResponse getAliasesResponse =  restHighLevelClient.indices().getAlias(request,RequestOptions.DEFAULT);
Map<String, Set<AliasMetaData>> map = getAliasesResponse.getAliases();
Set<String> indices = map.keySet();
```

### 查询示例

#### 汇总查询

1. 引入 RestHighLevelClient

   ```java
   @Autowired
   private RestHighLevelClient restHighLevelClient;
   ```

2. 构建 BoolQueryBuilder

   ```java
   BoolQueryBuilder bool = new BoolQueryBuilder();
   bool.must(QueryBuilders.rangeQuery("@timestamp").from(start.getTime()));
   bool.must(QueryBuilders.rangeQuery("@timestamp").to(end.getTime()));
   ```

3. 设置分组 TermsAggregationBuilder

   ```java
   TermsAggregationBuilder aggregationBuilderGroupBy = AggregationBuilders.terms("agg_count").field("module.keyword").size(200);
   ```

4. 分组查询

   ```java
   SearchSourceBuilder sourceBuilder = new SearchSourceBuilder().trackTotalHits(true).query(bool).aggregation(aggregationBuilderGroupBy);
   SearchRequest searchRequest = new SearchRequest(esIndexName).source(sourceBuilder);
   SearchResponse response = restHighLevelClient.search(searchRequest, RequestOptions.DEFAULT);
   Aggregations aggregations = response.getAggregations();
   ```

5. 获取查询结果

   ```java
   Aggregation sourceType = aggregations.get("agg_count");
   for (Terms.Bucket bucket : ((Terms) sourceType).getBuckets()) {
       logger.info("[LogIndex]"+bucket.getKeyAsString()+"[Count]"+bucket.getDocCount());
   }
   ```

6. 执行结果：

   ```
   [LogIndex]nlp-model[Count]101520
   [LogIndex]web-admin[Count]1106
   ```

   