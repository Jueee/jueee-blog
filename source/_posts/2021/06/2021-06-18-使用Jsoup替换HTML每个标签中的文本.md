---
title: 使用Jsoup替换HTML每个标签中的文本
layout: info
commentable: true
date: 2021-06-18
mathjax: true
mermaid: true
tags: [Java,JavaJar,HTML]
categories: 
- [Java,JavaJar]
- [HTML]
description: 
---

### 背景

为了对 HTML  进行文本翻译，需要提取 HTML 中每个标签中的文本。

如果使用传统方式进行提取，可能会效率低下，而且由于 HTML 结构复杂，非常不便。

在此介绍使用Jsoup替换HTML每个标签中的文本的方式。

<!--more-->

### 实现

Jsoup替换HTML每个标签中的文本：

```java
Element entry = doc.select("body").first();
Elements tags = entry.getAllElements();
for (Element tag : tags) {
    for (Node child : tag.childNodes()) {
        if (child instanceof TextNode && !((TextNode) child).isBlank()) {
            System.out.println(child); //text
            ((TextNode) child).text("word"); //replace to word
        }
    }
}
```

### 应用

翻译 HTML 步骤：

1. 使用 Jsoup 遍历，提取每个文本加入 Map 键值对。
2. 对 Map 键值对中的内容进行批量翻译。
3. 

```java
public static String translateHTML(String html){	// 参数为待翻译的HTML
    Document doc = Jsoup.parse(html);
    Element entry = doc.select("body").first();
    Elements tags = entry.getAllElements();
    Map<String,String> map = new HashMap<>();
    for (Element tag : tags) {
        for (Node child : tag.childNodes()) {
            if (child instanceof TextNode && !((TextNode) child).isBlank()) {
                if (StringUtils.isNotBlank(child.toString())) {
                    map.put(child.toString(), child.toString()); // 将文本注入 map
                }
            }
        }
    }
    translateText(map); // 批量翻译 map 中的键值对
    for (Element tag : tags) {
        for (Node child : tag.childNodes()) {
            if (child instanceof TextNode && !((TextNode) child).isBlank()) {
                if (StringUtils.isNotBlank(child.toString()) && map.containsKey(child.toString())) {
                    ((TextNode)child ).text(map.get(child.toString())); // 文本替换
                }
            }
        }
    }
    return doc.html();	// 返回新 HTML
}
```

