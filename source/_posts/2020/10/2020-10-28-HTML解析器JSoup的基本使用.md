---
title: HTML解析器JSoup的基本使用
layout: info
commentable: true
date: 2020-10-28
mathjax: true
mermaid: true
tags: [Java,JavaJar,HTML]
categories: 
- [Java,JavaJar]
- [HTML]
description: 
---

### JSoup介绍

JSoup是一个用于处理HTML的Java库，它提供了一个非常方便类似于使用DOM，CSS和jquery的方法的API来提取和操作数据。

- 官网：https://jsoup.org/
- GitHub：https://github.com/jhy/jsoup/

<!--more-->

#### JSoup 功能

jsoup实现WHATWG HTML5规范，并将HTML解析为与现代浏览器相同的DOM。

- 从URL，文件或字符串中提取并解析HTML。
- 查找和提取数据，使用DOM遍历或CSS选择器。
- 操纵HTML元素，属性和文本。
- 根据安全的白名单清理用户提交的内容，以防止XSS攻击。
- 输出整洁的HTML。

#### JSoup 引入

```xml
<!-- https://mvnrepository.com/artifact/org.jsoup/jsoup -->
<dependency>
    <groupId>org.jsoup</groupId>
    <artifactId>jsoup</artifactId>
    <version>1.13.1</version>
</dependency>
```

### JSoup 主要类

大多数情况下，下面给出`3`个类是我们需要重点了解的。

#### Jsoup类

Jsoup类是任何Jsoup程序的入口点，并将提供从各种来源加载和解析HTML文档的方法。

Jsoup类的一些重要方法如下：

| 方法                                                        | 描述                                                         |
| ----------------------------------------------------------- | ------------------------------------------------------------ |
| `static Connection connect(String url)`                     | 创建并返回URL的连接。                                        |
| `static Document parse(File in, String charsetName)`        | 将指定的字符集文件解析成文档。                               |
| `static Document parse(String html)`                        | 将给定的html代码解析成文档。                                 |
| `static String clean(String bodyHtml, Whitelist whitelist)` | 从输入HTML返回安全的HTML，通过解析输入HTML并通过允许的标签和属性的白名单进行过滤。 |

Jsoup类的其他重要方法可以参见 - https://jsoup.org/apidocs/org/jsoup/Jsoup.html

#### Document类

该类表示通过Jsoup库加载HTML文档。可以使用此类执行适用于整个HTML文档的操作。

Element类的重要方法可以参见 - http://jsoup.org/apidocs/org/jsoup/nodes/Document.html 。

#### Element类

HTML元素是由标签名称，属性和子节点组成。 使用Element类，您可以提取数据，遍历节点和操作HTML。

Element类的重要方法可参见 - http://jsoup.org/apidocs/org/jsoup/nodes/Element.html 。

### JSoup 应用实例

#### 加载文档

- **从URL加载文档**：使用`Jsoup.connect()`方法

  ```java
  Document doc1 = Jsoup.connect("https://www.baidu.com/").get();  
  ```

- **从文件加载文档**：使用`Jsoup.parse()`方法

  ```java
  Document doc2 = Jsoup.parse(new File("D:/test/jsontest.html"), "utf-8");
  ```

- **从String加载文档**：使用`Jsoup.parse()`方法

  ```java
  String html = "<html><head><title>First parse</title></head>"
                      + "<body><p>Parsed HTML into a doc.</p></body></html>";
  Document doc3 = Jsoup.parse(html);
  ```

#### 获取元素

以 百度首页为例：

```java
Document document = Jsoup.connect("https://www.baidu.com/").get();
```

- 获取标题

  ```java
  System.out.println(document.title());
  ```

- 获取页面的Fav图标

  假设`favicon`图像将是HTML文档的`<head>`部分中的第一个图像，可以使用下面的代码：

  ```java
  String favImage = "";
  Element element = document.head().select("link[href~=.*\\.(ico|png)]").first();
  if (element == null) {
      element = document.head().select("meta[itemprop=image]").first();
      if (element != null) {
          favImage = element.attr("content");
      }
  } else {
      favImage = element.attr("href");
  } 
  System.out.println(favImage); // /favicon.ico
  ```

- 获取页面中的所有链接

  Element类提供了attr()和text()方法来返回链接的链接和对应的文本。

  ```java
  Elements links = document.select("a[href]");
  for (Element link : links) {
  	System.out.println(link.text() + " - " + link.attr("href"));
  }
  ```

  结果如下：

  ![image-20201029193548876](/images/2020/10/image-20201029193548876.png)

- 获取页面中的所有图像

  调用`select()`方法传递 `"img[src~=(?i)\\.(png|jpe?g|gif)]"` 正则表达式作为参数，以便它可以打印`png`，`jpeg`或`gif`类型的图像。

  ```java
  Elements images = document.select("img[src~=(?i)\\.(png|jpe?g|gif)]");
  for (Element image : images) {
  	System.out.println(image.attr("alt") + " - " + image.attr("src"));
  }
  ```

  结果如下：

  ![image-20201029193832082](/images/2020/10/image-20201029193832082.png)

- 获取URL的元信息

  ```java
  String description = document.select("meta[name=description]").get(0).attr("content"); 
  System.out.println(description);
  // 全球最大的中文搜索引擎、致力于让网民更便捷地获取信息，找到所求。百度超过千亿的中文网页数据库，可以瞬间找到相关的搜索结果。
  ```

- 在HTML页面中获取表单属性

  ```java
  Element formElement = document.getElementById("form");
  Elements inputElements = formElement.getElementsByTag("input");
  for (Element inputElement : inputElements) {
  	String key = inputElement.attr("name");
  	String value = inputElement.attr("value");
  	System.out.println("Param name: " + key + ", Param value: " + value);
  }
  ```

  结果如下：

  ![image-20201029194221980](/images/2020/10/image-20201029194221980.png)

#### 更新元素

只要您使用上述方法找到您想要的元素; 可以使用Jsoup API来更新这些元素的属性或innerHTML。 

例如，想更新文档中存在的“`rel = nofollow`”的所有链接。

```java
Document document = Jsoup.parse(new File("D:/test/jsontest.html"), "utf-8");
Elements links = document.select("a[href]");  
links.attr("rel", "nofollow");
```

#### 消除不信任的HTML

假设在应用程序中，想显示用户提交的HTML片段。 例如 用户可以在评论框中放入HTML内容。 这可能会导致非常严重的问题，如果您允许直接显示此HTML。 用户可以在其中放入一些恶意脚本，并将用户重定向到另一个脏网站。

为了清理这个HTML，Jsoup提供`Jsoup.clean()`方法。 此方法期望HTML格式的字符串，并将返回清洁的HTML。 要执行此任务，Jsoup使用白名单过滤器。 jsoup白名单过滤器通过解析输入HTML(在安全的沙盒环境中)工作，然后遍历解析树，只允许将已知安全的标签和属性(和值)通过清理后输出。

它不使用正则表达式，这对于此任务是不合适的。

清洁器不仅用于避免XSS，还限制了用户可以提供的元素的范围：您可以使用文本，强元素，但不能构造`div`或表元素。

```java
String dirtyHTML = "<p><a href='https://www.baidu.com/' onclick='sendCookiesToMe()'>Link</a></p>";
String cleanHTML = Jsoup.clean(dirtyHTML, Whitelist.basic());
System.out.println(cleanHTML);
```

执行后输出结果如下：

```html
<p><a href="https://www.baidu.com/" rel="nofollow">Link</a></p>
```

