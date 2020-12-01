---
title: Vue可拖拽组件vue-grid-layout
layout: info
commentable: true
date: 2020-12-01
mathjax: true
mermaid: true
tags: [Vue]
categories: Vue
description: 
---

### 介绍

- 官网：https://jbaysolutions.github.io/vue-grid-layout/
- GitHub：https://github.com/jbaysolutions/vue-grid-layout
- npmjs：https://www.npmjs.com/package/vue-grid-layout

<!--more-->

### 特性

- 可拖拽
- 可调整大小
- 静态部件（不可拖拽、调整大小）
- 拖拽和调整大小时进行边界检查
- 增减部件时避免重建栅格
- 可序列化和还原的布局
- 自动化 RTL 支持
- 响应式

### 安装

```bash
npm install vue-grid-layout --save
```

### 属性

#### GridLayout

- **layout**

  数据源。值必须为 `Array`，其数据项为 `Object`。 每条数据项必须有 `i`, `x`, `y`, `w` 和 `h` 属性。 请参考下面的 `GridItem`。

- **responsiveLayouts**

  如果 `responsive` 设置为 `true`，该配置将作为栅格中每个断点的初始布局。键值是断点名称，每项的值都是类似 `layout` 属性定义的数据结构，值必须为 `Array`，其数据项为 `Object`。例如： `{lg: [layout items], md: [layout items]}`。需要注意的是，在创建栅格布局后设置该属性无效。

- **colNum**

  定义栅格系统的列数，其值需为自然数。

- **rowHeight**

  每行的高度，单位像素。

- **maxRows**

  定义最大行数。

- **margin**

  定义栅格中的元素边距。

  值必须是包含两个 `Number`的数组，数组中第一个元素表示水平边距，第二个表示垂直边距，单位为像素。

- **isDraggable**

  标识栅格中的元素是否可拖拽。

- **isResizable**

  标识栅格中的元素是否可调整大小。

- **isMirrored**

  标识栅格中的元素是否可镜像反转。

- **autoSize**

  标识容器是否自动调整大小。

- **verticalCompact**

  标识布局是否垂直压缩。

- **useCssTransforms**

  标识是否使用CSS属性 `transition-property: transform;`。

- **responsive**

  标识布局是否为响应式。

- **breakpoints**

  为响应式布局设置断点。

- **cols**

  设置每个断点对应的列数。

- **useStyleCursor**

  标识是否使用动态鼠标指针样式。当拖动出现卡顿时，将此值设为 `false`也许可以缓解布局问题。

#### GridItem

- **i**：栅格中元素的ID。

- **x**：标识栅格元素位于第几列，需为自然数。

- **y**：标识栅格元素位于第几行，需为自然数。

- **w**：标识栅格元素的初始宽度，值为`colWidth`的倍数。

- **h**：标识栅格元素的初始高度，值为`rowHeight`的倍数。

- **minW**：栅格元素的最小宽度，值为`colWidth`的倍数。如果`w`小于`minW`，则`minW`的值会被`w`覆盖。

- **minH**：栅格元素的最小高度，值为`rowHeight`的倍数。如果`h`小于`minH`，则`minH`的值会被`h`覆盖。

- **maxW**：栅格元素的最大宽度，值为`colWidth`的倍数。如果`w`大于`maxW`，则`maxW`的值会被`w`覆盖。

- **maxH**：栅格元素的最大高度，值为`rowHeight`的倍数。如果`h`大于`maxH`，则`maxH`的值会被`h`覆盖。

- **isDraggable**：标识栅格元素是否可拖拽。如果值为`null`则取决于父容器。

- **isResizable**：标识栅格元素是否可调整大小。如果值为`null`则取决于父容器。

- **static**：标识栅格元素是否为静态的（无法拖拽、调整大小或被其他元素移动）。

- **dragIgnoreFrom**：标识栅格元素中哪些子元素无法触发拖拽事件，值为`css-like`选择器。

  请参考 [interact.js docs](http://interactjs.io/docs/#ignorable-selectors)中的`ignoreFrom`。

- **dragAllowFrom**：标识栅格元素中哪些子元素可以触发拖拽事件，值为`css-like`选择器。如果值为`null`则表示所有子元素（`dragIgnoreFrom`的除外）。

  请参考 [interact.js docs](http://interactjs.io/docs/#ignorable-selectors)中的`allowFrom`。

- **resizeIgnoreFrom**：标识栅格元素中哪些子元素无法触发调整大小的事件，值为`css-like`选择器。

  请参考 [interact.js docs](http://interactjs.io/docs/#ignorable-selectors)中的`ignoreFrom`。

### 基础使用

1. 引入

   ```js
   import VueGridLayout from 'vue-grid-layout';
   ```

2. 加入到 Vue 组件

   ```js
   export default {
     components: {
         GridLayout: VueGridLayout.GridLayout,
         GridItem: VueGridLayout.GridItem
     },
     data() {
       return {
         layoutData: []
       };
     },
     methods: {
       init() {
         this.layoutData = [
             {"x":0,"y":0,"w":2,"h":2,"i":"0"},
             {"x":2,"y":0,"w":2,"h":4,"i":"1"},
             {"x":4,"y":0,"w":2,"h":5,"i":"2"},
             {"x":6,"y":0,"w":2,"h":3,"i":"3"},
             {"x":8,"y":0,"w":2,"h":3,"i":"4"},
             {"x":10,"y":0,"w":2,"h":3,"i":"5"},
             {"x":0,"y":5,"w":2,"h":5,"i":"6"},
             {"x":2,"y":5,"w":2,"h":5,"i":"7"},
             {"x":4,"y":5,"w":2,"h":5,"i":"8"},
             {"x":6,"y":3,"w":2,"h":4,"i":"9"},
             {"x":8,"y":4,"w":2,"h":4,"i":"10"},
             {"x":10,"y":4,"w":2,"h":4,"i":"11"},
             {"x":0,"y":10,"w":2,"h":5,"i":"12"},
             {"x":2,"y":10,"w":2,"h":5,"i":"13"},
             {"x":4,"y":8,"w":2,"h":4,"i":"14"},
             {"x":6,"y":8,"w":2,"h":4,"i":"15"},
             {"x":8,"y":10,"w":2,"h":5,"i":"16"},
             {"x":10,"y":4,"w":2,"h":2,"i":"17"},
             {"x":0,"y":9,"w":2,"h":3,"i":"18"},
             {"x":2,"y":6,"w":2,"h":2,"i":"19"}
         ];
       }
     },
     created() {
       this.init()
     }
   }
   ```

3. 加入网格

   ```html
   <template>
     <div class="dashboard-container">
       <grid-layout
               :layout="layoutData"
               :col-num="12"
               :row-height="30"
               :is-draggable="true"
               :is-resizable="true"
               :is-mirrored="false"
               :vertical-compact="true"
               :margin="[10, 10]"
               :use-css-transforms="true">
   
           <grid-item v-for="item in layoutData"
                      :x="item.x"
                      :y="item.y"
                      :w="item.w"
                      :h="item.h"
                      :i="item.i"
                      :key="item.i">
               {{item.i}}
           </grid-item>
       </grid-layout>  
     </div>
   </template>
   ```

4. 加上点背景颜色

   ```css
   .vue-grid-item {
     background: aquamarine;
   }
   ```

5. 预览效果

   ![image-20201201164548293](/images/2020/12/image-20201201164548293.png)

### 添加右键事件

在基础使用的基础上，增加如下配置：

1. 增加按钮

   ```html
   <template>
     <div class="dashboard-container">
         
       <ul class='contextmenu' v-show="menuConfig.visible" :style="{left:menuConfig.left+'px',top:menuConfig.top+'px'}">
         <li @click="test(1)">1</li>
         <li @click="test(2)">2</li>
         <li @click="test(3)">3</li>
       </ul>
         
       <grid-layout
               :layout="layoutData"
               :col-num="6"
               :row-height="30"
               :is-draggable="true"
               :is-resizable="true"
               :is-mirrored="false"
               :vertical-compact="true"
               :margin="[10, 10]"
               :use-css-transforms="true"
       >
   
           <grid-item v-for="item in layoutData"
                      :x="item.x"
                      :y="item.y"
                      :w="item.w"
                      :h="item.h"
                      :i="item.i"
                      :key="item.i">
             <div class="layout-Box" @contextmenu.prevent="openMenu(item, $event)">
               {{ item.i }}
             </div>
           </grid-item>
       </grid-layout>  
     </div>
   </template>
   ```

2. 增加 Data 相关配置

   ```js
     data() {
       return {
         menuConfig: { visible: false, left: 0, top: 0 }
       };
     },
     methods: {
       // 右键打开菜单
       openMenu(tag, e) {
         this.menuConfig.visible = true
         this.menuConfig.left = e.clientX
         this.menuConfig.top = e.clientY
       },
       // 关闭菜单
       closeMenu() {
         this.menuConfig.visible = false
       },
       // 测试方法
       test(i) {
         console.log(i)
       }
     },
     watch: {
       'menuConfig.visible':function(val,oldval){
         if (this.menuConfig.visible) {
           document.body.addEventListener('click', this.closeMenu)
         } else {
           document.body.removeEventListener('click', this.closeMenu)
         }
       }
     }
   ```

3. CSS

   ```css
   .layout-Box{
     width: 100%;
     height: 100%;
   }
   .contextmenu {
     margin: 0;
     background: #fff;
     z-index: 100;
     position: absolute;
     list-style-type: none;
     padding: 5px 0;
     border-radius: 4px;
     font-size: 12px;
     font-weight: 400;
     color: #333;
     box-shadow: 2px 2px 3px 0 rgba(0, 0, 0, .3);
     li {
       margin: 0;
       padding: 7px 16px;
       cursor: pointer;
       &:hover {
         background: #eee;
       }
     }
   }
   ```

4. 预览效果：

   ![image-20201201184914907](/images/2020/12/image-20201201184914907.png)

