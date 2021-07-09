---
title: Bootstrap多层modal弹窗同时关闭的解决办法
layout: info
commentable: true
date: 2021-07-06
mathjax: true
mermaid: true
tags: [HTML]
categories: HTML
description: 
---

Bootstrap多层modal弹窗时。当子窗口关闭时，所有父窗口会一起关闭。

<!--more-->

原因是Bootstrap在窗口关闭事件委托时，委托给所有窗口。

如源码（位于 `bootstrap.js` 或者 `bootstrap.min.js` ）：

```js
this.$element.on('click.dismiss.bs.modal', '[data-dismiss="modal"]', $.proxy(this.hide, this))
```

改进为：

```js
this.$element.on('click.dismiss.bs.modal', '[data-dismiss="modal"]:first', $.proxy(this.hide, this))
this.$element.on('click.dismiss.bs.modal', '[data-dismiss="modal"]:last', $.proxy(this.hide, this))
```

这样在多层窗口关闭时只会关闭自窗口，不再关闭父窗口。