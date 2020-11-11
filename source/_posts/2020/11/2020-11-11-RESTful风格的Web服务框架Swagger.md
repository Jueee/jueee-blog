---
title: RESTful风格的Web服务框架Swagger
layout: info
commentable: true
date: 2020-11-11
mathjax: true
mermaid: true
tags: [Java,JavaJar,RESTful]
categories: [Java,JavaJar]
description: 
---

### Swagger 介绍

Swagger 是一个规范和完整的框架，用于生成、描述、调用和可视化 RESTful 风格的 Web 服务。

总体目标是使客户端和文件系统作为服务器以同样的速度来更新。文件的方法、参数和模型紧密集成到服务器端的代码，允许 API 来始终保持同步。

- 官网：https://swagger.io/
- GitHub：https://github.com/swagger-api

<!--more-->

#### Swagger 依赖

```xml
<dependency>
	<groupId>io.springfox</groupId>
	<artifactId>springfox-swagger2</artifactId>
	<version>2.6.1</version>
</dependency>
<dependency>
	<groupId>io.springfox</groupId>
	<artifactId>springfox-swagger-ui</artifactId>
	<version>2.6.1</version>
</dependency>
```

### Swagger UI

添加依赖 `springfox-swagger-ui` 之后，该文档将在此处自动提供：

> http://localhost:8080/swagger-ui.html

Swagger布局分为四部分：

1. **API分组**：如果没有配置分组默认是default。通过Swagger实例Docket的`groupName()`方法即可配置分组。
2. **基本描述**：可以通过Swagger实例Docket的`apiInfo()`方法中的ApiInfo实例参数配置文档信息。
3. **请求接口列表**：在组范围内，只要被Swagger2扫描匹配到的请求都会在这里出现。
4. **实体列表**：只要实体在请求接口的返回值上（即使是泛型），都能映射到实体项中！

> 实体列表部分注意：并不是因为@ApiModel注解让实体显示在Models列表里，而是只要出现在接口方法的返回值上的实体都会显示在这里，而@ApiModel和@ApiModelProperty这两个注解只是为实体添加注释的。前者为类添加注释，后者为类属性添加注释。

### swagger2 注解

#### 注解整体说明

**用于controller类上：**

| 注解 | 说明           |
| ---- | -------------- |
| @Api | 对请求类的说明 |

**用于方法上面（说明参数的含义）：**

| 注解                                  | 说明                                                        |
| ------------------------------------- | ----------------------------------------------------------- |
| @ApiOperation                         | 方法的说明                                                  |
| @ApiImplicitParams、@ApiImplicitParam | 方法的参数的说明；@ApiImplicitParams 用于指定单个参数的说明 |

**用于方法上面（返回参数或对象的说明）：**

| 注解                        | 说明                                                    |
| --------------------------- | ------------------------------------------------------- |
| @ApiResponses、@ApiResponse | 方法返回值的说明 ；@ApiResponses 用于指定单个参数的说明 |

**对象类：**

| 注解              | 说明                                         |
| ----------------- | -------------------------------------------- |
| @ApiModel         | 用在JavaBean类上，说明JavaBean的 用途        |
| @ApiModelProperty | 用在JavaBean类的属性上面，说明此属性的的含议 |

#### @Api

@Api：请求类的说明

```java
@Api：放在 请求的类上，与 @Controller 并列，说明类的作用，如用户模块，订单类等。
	tags="说明该类的作用"
	value="该参数没什么意义，所以不需要配置"
```

`@Api` 其它属性配置：

| 属性名称       | 备注                                    |
| -------------- | --------------------------------------- |
| value          | url的路径值                             |
| tags           | 如果设置这个值、value的值会被覆盖       |
| description    | 对api资源的描述                         |
| basePath       | 基本路径                                |
| position       | 如果配置多个Api 想改变显示的顺序位置    |
| produces       | 如, “application/json, application/xml” |
| consumes       | 如, “application/json, application/xml” |
| protocols      | 协议类型，如: http, https, ws, wss.     |
| authorizations | 高级特性认证时配置                      |
| hidden         | 配置为true ，将在文档中隐藏             |

#### @ApiOperation

@ApiOperation：方法的说明

```java
@ApiOperation："用在请求的方法上，说明方法的作用"
	value="说明方法的作用"
	notes="方法的备注说明"
```

@ApiImplicitParams、@ApiImplicitParam：方法参数的说明

```java
@ApiImplicitParams：用在请求的方法上，包含一组参数说明
	@ApiImplicitParam：对单个参数的说明	    
	    name：参数名
	    value：参数的说明、描述
	    required：参数是否必须必填
	    paramType：参数放在哪个地方
	        · query --> 请求参数的获取：@RequestParam
	        · header --> 请求参数的获取：@RequestHeader	      
	        · path（用于restful接口）--> 请求参数的获取：@PathVariable
	        · body（请求体）-->  @RequestBody User user
	        · form（普通表单提交）	   
	    dataType：参数类型，默认String，其它值dataType="Integer"	   
	    defaultValue：参数的默认值
```

#### @ApiResponses

@ApiResponses、@ApiResponse：方法返回值的状态码说明

```java
@ApiResponses：方法返回对象的说明
	@ApiResponse：每个参数的说明
	    code：数字，例如400
	    message：信息，例如"请求参数没填好"
	    response：抛出异常的类
```

#### @ApiModel

@ApiModel：用于JavaBean上面，表示对JavaBean 的功能描述

`@ApiModel`的用途有2个：

1. 当请求数据描述，即 `@RequestBody` 时， 用于封装请求（包括数据的各种校验）数据；
2. 当响应值是对象时，即 `@ResponseBody` 时，用于返回值对象的描述。

#### @ApiModelProperty

@ApiModelProperty：用在JavaBean类的属性上面，说明属性的含义

### Swagger 示例

#### API基本信息配置类

要想使用Swagger，必须编写一个配置类来配置 Swagger，这里的配置类如下：

```java
@Configuration
@EnableSwagger2
public class SwaggerConfig {

    @Bean
    public Docket docket(){
        // 构造函数传入初始化规范，这是swagger2规范
        return new Docket(DocumentationType.SWAGGER_2)
                .apiInfo(apiInfo()) //apiInfo： 添加api详情信息，参数为ApiInfo类型的参数
                .groupName("System") // 配置分组
                .enable(true) // 配置是否启用Swagger，如果是false，在浏览器将无法访问，默认是true
                .select()
                .apis(RequestHandlerSelectors.basePackage("com.system.controller")) //apis： 添加过滤条件,
                .paths(PathSelectors.any()) //paths： 这里是控制哪些路径的api会被显示出来
                .build().pathMapping("/"); 
    }
    public ApiInfo apiInfo(){
        Contact contact=new Contact("xiaojue","http://localhost:8181","hellojue@foxmail.com");
        return new ApiInfoBuilder()
                .contact(contact)
                .title("API文档")
                .description("系统API文档")
                .termsOfServiceUrl("")
                .version("1.0")
                .build();
    }
}
```

效果如下：

![image-20201111113952683](/images/2020/11/image-20201111113952683.png)

##### 配置API分组

通过Swagger实例Docket的`groupName()`方法即可配置分组，如果没有配置分组默认是default，代码如下：

```javascript
@Bean
public Docket docket2(Environment environment) {
   return new Docket(DocumentationType.SWAGGER_2)
      .apiInfo(apiInfo()) // 配置基本API信息
      .groupName("hello") // 配置分组
       // 省略配置....
}
```

##### 配置多个分组

很简单，配置多个分组只需要配置多个docket即可，代码如下：

```javascript
@Bean
public Docket docket1(){
   return new Docket(DocumentationType.SWAGGER_2)
      .groupName("组一")
      // 省略配置....
}
@Bean
public Docket docket2(){
   return new Docket(DocumentationType.SWAGGER_2)
     .groupName("组二")
     // 省略配置....
}
@Bean
public Docket docket3(){
   return new Docket(DocumentationType.SWAGGER_2)
     .groupName("组三")
     // 省略配置....
}
```

#### 接口注解

```java
@Api(tags = "菜单权限接口")
@RequestMapping("/menu")
@RestController
public class MenuController {

    @Autowired
    private MenuService menuService;
    
    @ApiOperation(value = "新增菜单")
    @PostMapping("/add")
    public ResponseBean add(@RequestBody @Validated MenuVO menuVO) {
        Menu node = menuService.add(menuVO);
        Map<String, Object> map = new HashMap<>();
        map.put("id", node.getId());
        map.put("menuName", node.getMenuName());
        map.put("children", new ArrayList<>());
        map.put("icon", node.getIcon());
        return ResponseBean.success(map);
    }
}
```

效果如下：

![image-20201111141157829](/images/2020/11/image-20201111141157829.png)

![image-20201111113642972](/images/2020/11/image-20201111113642972.png)

#### 模型类注解

```java
@ApiModel("菜单实体类")
@Data
public class MenuVO {

    @ApiModelProperty("编号")
    private Long id;

    @ApiModelProperty("父级id")
    private Long parentId;

    @ApiModelProperty("菜单名称")
    private String menuName;
}
```

效果如下：

![image-20201111140618878](/images/2020/11/image-20201111140618878.png)