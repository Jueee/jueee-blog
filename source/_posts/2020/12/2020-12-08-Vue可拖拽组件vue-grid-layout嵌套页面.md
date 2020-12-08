---
title: Vue可拖拽组件vue-grid-layout嵌套页面
layout: info
commentable: true
date: 2020-12-08
mathjax: true
mermaid: true
tags: [Vue]
categories: Vue
description: 
---

### 嵌套页面方式

- 普通嵌套
- ifream 嵌套

<!--more-->

### 普通嵌套

1. vue-grid-layout 设置：

   ```html
   	<grid-layout
                :layout="layoutData"
                :col-num="6"
                :row-height="30"
                :is-draggable="true"
                :is-resizable="true"
                :is-mirrored="false"
                :vertical-compact="true"
                :auto-size="true"
                :margin="[10, 10]"
                :use-css-transforms="true"
                >
   
       <grid-item v-for="item in layoutData"
                  :x="item.x"
                  :y="item.y"
                  :w="item.w"
                  :h="item.h"
                  :i="item.i"
                  :key="item.i"
                  @resize="resizeEvent">
           <div v-if="item.i == 0"><indexGrid0></indexGrid0></div>
           <div v-if="item.i == 1"><indexGrid1></indexGrid1></div>
           <div v-if="item.i == 2"><indexGrid2></indexGrid2></div>
           <div v-if="item.i == 3"><indexGrid3></indexGrid3></div>
           <div v-if="item.i == 4"><indexGrid4></indexGrid4></div>
           <div v-if="item.i == 5"><indexGrid5></indexGrid5></div>
       </grid-item>
   ```

2. 引入页面

   ```js
   import VueGridLayout from 'vue-grid-layout';
   import indexGrid0 from '@/views/dashboard/index-grid0'
   import indexGrid1 from '@/views/dashboard/index-grid1'
   import indexGrid2 from '@/views/dashboard/index-grid2'
   import indexGrid3 from '@/views/dashboard/index-grid3'
   import indexGrid4 from '@/views/dashboard/index-grid4'
   import indexGrid5 from '@/views/dashboard/index-grid5'
   
   export default {
     components: {
         GridLayout: VueGridLayout.GridLayout,
         GridItem: VueGridLayout.GridItem,
         'indexGrid0': indexGrid0,
         'indexGrid1': indexGrid1,
         'indexGrid2': indexGrid2,
         'indexGrid3': indexGrid3,
         'indexGrid4': indexGrid4,
         'indexGrid5': indexGrid5
     },
   }
   ```

3. 页面示例

   ```html
    <template>
     <div>
       <h1>11111</h1>
     </div>
    </template>
    <script>
       export default {}
    </script>
    <style scoped>
    </style>
   ```

### ifream 嵌套

1. vue-grid-layout 设置：

   ```html
   <grid-layout
                :layout="layoutData"
                :col-num="6"
                :row-height="30"
                :is-draggable="true"
                :is-resizable="true"
                :is-mirrored="false"
                :vertical-compact="true"
                :auto-size="true"
                :margin="[10, 10]"
                :use-css-transforms="true"
                >
   
       <grid-item v-for="item in layoutData"
                  :x="item.x"
                  :y="item.y"
                  :w="item.w"
                  :h="item.h"
                  :i="item.i"
                  :key="item.i"
                  @resize="resizeEvent">
           <iframe v-if="item.i == 0" src="./indexGrid0" width="100%" height="100%" frameborder="0" scrolling="auto"></iframe>
           <iframe v-if="item.i == 1" src="./indexGrid1" width="100%" height="100%" frameborder="0" scrolling="auto"></iframe>
           <iframe v-if="item.i == 2" src="./indexGrid2" width="100%" height="100%" frameborder="0" scrolling="auto"></iframe>
           <iframe v-if="item.i == 3" src="./indexGrid3" width="100%" height="100%" frameborder="0" scrolling="auto"></iframe>
           <iframe v-if="item.i == 4" src="./indexGrid4" width="100%" height="100%" frameborder="0" scrolling="auto"></iframe>
           <iframe v-if="item.i == 5" src="https://www.baidu.com/" width="100%" height="100%" frameborder="0" scrolling="auto"></iframe>
       </grid-item>
   </grid-layout>  
   ```

   或者：

   ```html
   <grid-item v-for="item in layoutData"
                      :x="item.x"
                      :y="item.y"
                      :w="item.w"
                      :h="item.h"
                      :i="item.i"
                      :key="item.i"
                      @resize="resizeEvent">
       <span class="widget-title">{{ item.title }}</span> 
       <iframe :src="item.src" width="100%" height="100%" frameborder="0" scrolling="auto"></iframe>
   </grid-item>
   
   <script>
   export default {
     methods: {
       init() {
         this.layoutData = [
             {"x":0,"y":0,"w":2,"h":8,"i":"0","title":"System Information","src":"./indexGrid0"},
             {"x":2,"y":0,"w":2,"h":11,"i":"1","title":"System Resources","src":"./indexGrid1"},
             {"x":4,"y":0,"w":2,"h":8,"i":"2","title":"Scanning Statistics","src":"./indexGrid2"},
             {"x":0,"y":5,"w":2,"h":11,"i":"3","title":"Threats Distribution - Last 24 Hours","src":"./indexGrid3"},
             {"x":2,"y":5,"w":2,"h":8,"i":"4","title":"Pending Job Statistics","src":"./indexGrid4"},
             {"x":4,"y":5,"w":2,"h":11,"i":"5","title":"Baidu","src":"https://www.baidu.com/"}
         ];
       }
     },
     created() {
       this.init()
     }
   }
   </script>
   ```

2. 路由配置 `src\router\index.js`：

   ```js
   export const constantRouterMap = [
     {
       path: '/indexGrid0',
       component: () => import('@/views/dashboard/index-grid0'),
       hidden: true
     },
     {
       path: '/indexGrid1',
       component: () => import('@/views/dashboard/index-grid1'),
       hidden: true
     },
     {
       path: '/indexGrid2',
       component: () => import('@/views/dashboard/index-grid2'),
       hidden: true
     },
     {
       path: '/indexGrid3',
       component: () => import('@/views/dashboard/index-grid3'),
       hidden: true
     },
     {
       path: '/indexGrid4',
       component: () => import('@/views/dashboard/index-grid4'),
       hidden: true
     },
     {
       path: '/indexGrid5',
       component: () => import('@/views/dashboard/index-grid5'),
       hidden: true
     },
   ]
   ```

3. 页面效果：

   ![image-20201208155342443](/images/2020/12/image-20201208155342443.png)

#### iframe 按钮刷新

增加刷新按钮：

```html
<grid-item v-for="item in layoutData"
                   :x="item.x"
                   :y="item.y"
                   :w="item.w"
                   :h="item.h"
                   :i="item.i"
                   :key="item.i"
                   @resize="resizeEvent">

    <button class="refresh-button" @click="refreshPage(item.i)"><i class="el-icon-refresh" /></button>
    <iframe :src="item.src" :id="`iframe${(item.i)}`" width="100%" height="100%" frameborder="0" scrolling="auto"></iframe>
</grid-item>
```

对应 JS 方法：

```js
refreshPage(pageNum){
    var _iframe = document.getElementById('iframe'+pageNum);
    _iframe.contentWindow.location.reload(true);
}
```

{% note info %}

Vue的标签属性label中字符串拼接变量：

```html
<el-form-item :label="`参数${(index + 1)}类型`" v-for="(item, index,) in props.row.params">
    <span v-text="item"></span>
</el-form-item>
```

{% endnote %}