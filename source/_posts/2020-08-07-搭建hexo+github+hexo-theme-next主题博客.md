---
title: 搭建hexo+github+hexo-theme-next主题博客
layout: info
commentable: true
date: 2020-08-07
mathjax: true
mermaid: true
tags: [Blog,Node.js]
categories: 
-	Blog
description: Hexo是一款基于Node.js的静态博客框架，依赖少易于安装使用，可以方便的生成静态网页托管在GitHub和Coding上，是搭建博客的首选框架。
---

### 博客介绍

博客预览地址：[https://theme-next.js.org/](https://theme-next.js.org)

### 搭建博客

GitHub：[https://github.com/next-theme/theme-next-docs](https://github.com/next-theme/theme-next-docs)

在本地安装：

```shell
git clone https://github.com/next-theme/theme-next-docs
cd theme-next-docs
npm install
```

生成：

```
npx hexo generate
```

运行：

```
npx hexo server
```

### 博客主题

GitHub：[https://github.com/next-theme/hexo-theme-next](https://github.com/next-theme/hexo-theme-next)

### 博客设置

#### 创建categories

1. **新建一个页面，命名为categories。命令如下：**

   ```
   npx hexo new page categories
   ```

   在myBlog/source下会新生成一个新的文件夹categories
   ，在该文件夹下会有一个index.md文件。

2. **编辑categories文件夹下的index.md**

   ```
   ---
   title: categories
   date: 2020-08-07 10:29:47
   type: "categories"
   comments: false
   ---
   ```

3. **在菜单中添加链接。**

   编辑主题的 `_config.next.yml`，将menu中的 categories: /categories 注释去掉，如下:

   ```
   categories: /categories/ || fa fa-fw fa-th
   ```

#### 添加sitemap

站点地图是一种文件，您可以通过该文件列出您网站上的网页，从而将您网站内容的组织架构告知Google和其他搜索引擎。Googlebot等搜索引擎网页抓取工具会读取此文件，以便更加智能地抓取您的网站。

1. 安装插件：

   ```
   npm install hexo-generator-sitemap --save
   npm install hexo-generator-baidu-sitemap --save
   ```

2. 在博客目录的_config.yml中添加如下代码：

   ```
   # 自动生成sitemap
   sitemap:
       path: sitemap.xml
   baidusitemap:
       path: baidusitemap.xml
   ```

3. 编译博客

   ```
   npx hexo generate
   ```

4. 在你的博客根目录的public下面发现生成了sitemap.xml以及baidusitemap.xml就表示成功了。