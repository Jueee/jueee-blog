---
title: Element UI自定义CSS覆盖原生
layout: info
commentable: true
date: 2023-05-15
mathjax: true
mermaid: true
tags: [Vue,Element]
categories: Vue
description: 
---

在使用 Element UI 时，发现有时候可以在控制台利用内置的类来改变节点元素样式，但是当数据一多就无法利用了（即，无效利用），并且，在无效后在其上添加会发现，添加的样式处于所需要绑定的上层，故又无效。

<!--more-->

### 出现问题

自定义样式，无法覆盖原生样式：

```
<style scoped>
.el-collapse-item__content {
  padding-bottom: 5px;
}
</style>
```

### 问题原因

style 样式的优先度 > 类的优先度，故无法绑定所需，只能赋予其上层样式。

### 解决方案

在局部样式中，利用element-ui中内置样式设置自定义样式前加上  `/deep/`

```html
<style scoped>
/deep/ .el-collapse-item__content {
  padding-bottom: 5px;
}
</style>
```

![image-20230515101528210](assets/image-20230515101528210.png)

 将原有内置样式替换自定义样式，搞定 ！
