---
title: ElasticSearch集成Spring之RestHighLevelClient示例
layout: info
commentable: true
date: 2020-12-06
mathjax: true
mermaid: true
tags: [ElasticSearch,Java,JavaClass,Spring]
categories: 
- [Database,ElasticSearch]
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

引入 RestHighLevelClient

   ```java
   @Autowired
   private RestHighLevelClient restHighLevelClient;
   ```

### 索引相关

#### 判断索引是否存在

```java
GetIndexRequest request = new GetIndexRequest(indexName);
boolean exists = restHighLevelClient.indices().exists(request, RequestOptions.DEFAULT);
```

#### 列出所有索引

```java
GetAliasesRequest request = new GetAliasesRequest();
GetAliasesResponse getAliasesResponse =  restHighLevelClient.indices().getAlias(request,RequestOptions.DEFAULT);
Map<String, Set<AliasMetaData>> map = getAliasesResponse.getAliases();
Set<String> indices = map.keySet();
```

#### 创建索引

```java
CreateIndexRequest request = new CreateIndexRequest(indexName);
request.settings(Settings.builder()
                 .put("index.number_of_replicas", 1) // 有1个备份
                 .put("index.number_of_shards", 5)); // 有5个碎片
XContentBuilder mappingBuilder = JsonXContent.contentBuilder()
                    .startObject()
                    .startObject("properties")
                    .startObject("title").field("type", "text").field("index", "true").endObject()
                    .startObject("content").field("type", "text").field("index", "true").endObject()
                    .endObject()
                    .endObject();
request.mapping(mappingBuilder);
CreateIndexResponse response = restHighLevelClient.indices().create(request, RequestOptions.DEFAULT);
System.out.println(response.isAcknowledged());
```

查看索引 Mapping：

```bash
$ curl http://127.0.0.1:9200/wyqtest/_mapping?pretty
{
  "wyqtest" : {
    "mappings" : {
      "properties" : {
        "content" : {
          "type" : "text"
        },
        "title" : {
          "type" : "text"
        }
      }
    }
  }
}
```

#### 删除索引

```java
DeleteIndexRequest request = new DeleteIndexRequest(indexName);
request.indicesOptions(IndicesOptions.LENIENT_EXPAND_OPEN);
AcknowledgedResponse response = restHighLevelClient.indices().delete(request, RequestOptions.DEFAULT);
log.info("result: {}", response.isAcknowledged());
```

### 查询示例

#### 分页查询

1. 构建 BoolQueryBuilder

   ```java
   BoolQueryBuilder bool = new BoolQueryBuilder();
   bool.must(QueryBuilders.matchQuery("module", dto.getModule()).minimumShouldMatch("100%"));
   bool.must(QueryBuilders.termQuery("level", dto.getLevel().toLowerCase()));
   ```

2. 设置查询 SearchSourceBuilder

   ```java
   SearchSourceBuilder sourceBuilder = new SearchSourceBuilder().trackTotalHits(true);
   // 设置查询条件BoolQueryBuilder
   sourceBuilder.query(bool);
   // 设置分组，需注意 es 的分页是从 0 开始的
   sourceBuilder.from(page);
   sourceBuilder.size(perPage);
   // 设置排序
   sourceBuilder.sort("@timestamp", SortOrder.DESC);
   ```

3. 进行查询

   ```java
   SearchRequest searchRequest = new SearchRequest(index);
   searchRequest.source(sourceBuilder);
   SearchResponse response = restHighLevelClient.search(searchRequest, RequestOptions.DEFAULT);
   ```

4. 获取查询结果

   ```java
   // 获取结果集
   SearchHits hits = response.getHits();
   // 获取总条数
   paginator.setItems(Integer.valueOf(String.valueOf(hits.getTotalHits().value)));
   // 转换结果集
   for (SearchHit hit : response.getHits().getHits()) {
       PhishingLogDto mailServer = new PhishingLogDto();
       mailServer.jsonToDto(mailServer, JSONObject.parseObject(hit.getSourceAsString()));
       list.add(mailServer);
   }
   ```


#### 根据 IDs 查询数据集

```java
MultiGetRequest request = new MultiGetRequest();
for (int i = 0; i < indexArray.size(); i++) {
   request.add(new MultiGetRequest.Item(index, idArray.getString(i)));
}
MultiGetResponse response = restHighLevelClient.mget(request, RequestOptions.DEFAULT);
MultiGetItemResponse[] itemResponses = response.getResponses();
for (MultiGetItemResponse itemResponse : itemResponses) {
    GetResponse getResponse = itemResponse.getResponse();
    if (getResponse.isExists()) {
        Map<String, Object> sourceAsMap = getResponse.getSourceAsMap();
        for (String key : sourceAsMap.keySet()) {
            Object value = sourceAsMap.get(key);
            try {
                if (Constants.ONLINE_SUSPECT_DATE_COLUMN.contains(key)) { // 定义时间格式
                    value = Constants.ONLINE_SUSPECT_DATE_FORMAT.parse(value.toString()); // 将时间字符串解析为Date对象
                }
                BeanUtils.setProperty(onlineSuspect, key, value);
            } catch (Exception e) {
                log.error("[key]{} [Message]{}", key, e.getMessage(), e);
            }
        }
    }
}
```



