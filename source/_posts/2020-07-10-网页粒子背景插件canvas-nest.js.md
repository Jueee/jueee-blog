---
title: 网页粒子背景插件canvas-nest.js
layout: info
commentable: true
date: 2020-07-09
mathjax: true
mermaid: true
tags: [Blog,HTML]
categories: Blog
description: Canvas-nest.js是一个非常好看的网页粒子背景插件，不需要依赖任何第三方库即可运行，提供额非常炫酷的背景。
---

**Canvas-nest.js是一个非常好看的网页粒子背景插件，不需要依赖任何第三方库即可运行，提供额非常炫酷的背景。**

### Canvas-nest.js

官网介绍

> [https://github.com/hustcc/canvas-nest.js](https://github.com/hustcc/canvas-nest.js)

#### 特征

- 它不依赖jQuery，并且使用原始的 javascrpit。
- 体积小巧，只有 2 Kb。
- 易于实现，配置简单。
- 您不必是Web开发人员即可使用它。
- 使用区域渲染进行模块化。

### 使用

使用非常简单，将下面的代码插入到 `<body>` 和 `</body>` 之间就行了。

```html
<script type="text/javascript" color="#34495e" opacity='0.5' zIndex="-2" count="99" src="canvas-nest.min.js"></script>
```

#### 组态

- **color**：线条颜色，默认值：`'0,0,0'`；RGB值：（R，G，B）。（注意：使用'，'分隔。）
- **pointColor**：点的颜色，默认值：`'0,0,0'`；RGB值：（R，G，B）。（注意：使用'，'分隔。）
- **opacity**：线的不透明度（0〜1），默认值：`0.5`。
- **count**：线条数量，默认值：`99`。
- **zIndex**：背景的 z-index 属性，默认值：`-1`。