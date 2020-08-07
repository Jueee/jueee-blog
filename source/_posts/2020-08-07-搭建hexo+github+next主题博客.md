---
title: 搭建hexo+github+next主题博客
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

### 发布到github.io

在 hexo下的_config.yml文件中配置：

```yml
deploy:
  type: git
  repository: git@github.com:Jueee/jueee.github.io.git
  branch: master
```

安装插件：

```
npm install hexo-deployer-git --save
```

打开你的git bash，输入`hexo d`就会将本次有改动的代码全部提交，没有改动的不会：

```
$ npx hexo g -d
```

【注】部署这个命令一定要用git bash，否则会提示`Permission denied (publickey).`

此时，会在项目中生成 `.deploy_git` 文件夹。

打开git bash，切换到hexo/.deploy_git，执行

```
git init
```

再绑定远程仓库

```
git remote add origin git@github.com:jueee/jueee.github.io.git
```

回到cmd命令行

```
$ npx hexo g -d
```

搞定了，成功提交了正确的博客内容。

### 常用hexo命令

常见命令

```
hexo new "postName" #新建文章
hexo new page "pageName" #新建页面
hexo generate #生成静态页面至public目录
hexo server #开启预览访问端口（默认端口4000，'ctrl + c'关闭server）
hexo deploy #部署到GitHub
hexo help  # 查看帮助
hexo version  #查看Hexo的版本
```

缩写：

```
hexo n == hexo new
hexo g == hexo generate
hexo s == hexo server
hexo d == hexo deploy
```

组合命令：

```
hexo s -g #生成并本地预览
hexo d -g #生成并上传
```