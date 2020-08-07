---
title: 博客添加 Fork me on GitHub
layout: info
commentable: true
date: 2020-07-09
mathjax: true
mermaid: true
tags: [Blog,HTML]
categories: Blog
description: 在网上浏览博客时经常看到页面的右上角或左上角有一个fork me on github的按钮，本文将介绍如何实现。
---

**在网上浏览博客时经常看到页面的右上角或左上角有一个fork me on github的按钮，本文将介绍如何实现。**

### Fork me on GitHub

GitHub 获取 css 文件：

> [https://github.com/simonwhitaker/github-fork-ribbon-css/](https://github.com/simonwhitaker/github-fork-ribbon-css/)

效果演示：

> [https://simonwhitaker.github.io/github-fork-ribbon-css/](https://simonwhitaker.github.io/github-fork-ribbon-css/)

### 使用

将以下代码复制到`<head>`页面的中，引入 css：

```
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-fork-ribbon-css/0.2.3/gh-fork-ribbon.min.css" />
```

使用非常简单，将下面的代码插入到 `<body>` 和 `</body>` 之间就行了。

```html
<a class="github-fork-ribbon" href="https://github.com/Jueee" target="_blank" 
   	data-ribbon="Fork me on GitHub" title="Fork me on GitHub">
    Fork me on GitHub
</a>
```

默认是在页面右上角。

### 其他样式

- 固定标签：`class="github-fork-ribbon fixed"`

- 更换位置：

  - 右上角：`class="github-fork-ribbon right-top"`
  - 右下角：`class="github-fork-ribbon right-bottom"`
  - 左上角：`class="github-fork-ribbon left-top"`
  - 左下角：`class="github-fork-ribbon left-bottom fixed"`

- 更换背景颜色：

  ```css
  .github-fork-ribbon.left-bottom:before {
      background-color: #333;
  }
  ```

### 小屏幕不显示

按照上面的步骤当屏幕缩小后还会显示fork me on github图标，但这不是我想要的，如果希望在大屏下显示，小屏后就不显示了。方法如下：

新增样式：

```css
.forkme{
  display: none;
}
@media (min-width: 1350px) {
  .forkme{
    display: inline;
  }
}
```

代码块上套上div加上class就行了，如下：

```html
<div class="forkme">
	<a class="github-fork-ribbon fixed"	href="https://github.com/Jueee" >
		Fork me on GitHub
	</a>
</div>
```

