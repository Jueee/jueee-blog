---
title: vue-admin-template开启顶部导航
layout: info
commentable: true
date: 2020-11-11
mathjax: true
mermaid: true
tags: [Vue,Element]
categories: Vue
description: 
---

vue-admin-template 默认没有开启 [顶部导航](https://panjiachen.gitee.io/vue-element-admin-site/zh/guide/essentials/tags-view.html)，可通过如下步骤进行开启。

<!--more-->

### 开启步骤

1. 复制vue-element-admin必要组件，到template对应的目录下。

   @/layout/components/TagsView 文件夹

   @/store/modules/tagsView.js
   文件

2. 添加标签
   @/layout/components/AppMain.vue添加：

   ```html
   <template>
    <section class="app-main">
      <transition name="fade-transform" mode="out-in">
        <keep-alive :include="cachedViews">   <!-- 新增  -->
          <router-view :key="key" />
        </keep-alive>           <!-- 新增 -->
      </transition>
    </section>
   </template>
   ```
   
3. 修改 @store/index.js

   ```js
   import Vue from 'vue'
   import Vuex from 'vuex'
   import getters from './getters'
   import app from './modules/app'
   import settings from './modules/settings'
   import user from './modules/user'
   import tagsView from './modules/tagsView'  //新增
   
   Vue.use(Vuex)
   
   const store = new Vuex.Store({
     modules: {
       app,
       settings,
       user,
       tagsView  //新增
     },
     getters
   })
   
   export default store
   ```

4. 修改/src/store/getters.js

   ```js
   const getters = {
     sidebar: state => state.app.sidebar,
     device: state => state.app.device,
     token: state => state.user.token,
     avatar: state => state.user.avatar,
     name: state => state.user.name,
     visitedViews: state => state.tagsView.visitedViews,  //新增
     cachedViews: state => state.tagsView.cachedViews  //新增
   }
   export default getters
   ```

5. 修改 /src/layout/components/index.js

   ```js
   export { default as Navbar } from './Navbar'
   export { default as Sidebar } from './Sidebar'
   export { default as AppMain } from './AppMain'
   export { default as TagsView } from './TagsView/index.vue'   //新增
   ```

6. 修改 /src/store/modules/setting.js

   ```js
   const { showSettings, tagsView, fixedHeader, sidebarLogo } = defaultSettings   //新增tagsView
   
   const state = {
     tagsView: tagsView,   //新增
     showSettings: showSettings,
     fixedHeader: fixedHeader,
     sidebarLogo: sidebarLogo
   }
   ```

7. 修改 /src/layout/index.vue

   ```html
   <template>
     <div :class="classObj" class="app-wrapper">
       <div v-if="device==='mobile'&&sidebar.opened" class="drawer-bg" @click="handleClickOutside" />
       <sidebar class="sidebar-container" />
       <div class="main-container">
         <div :class="{'fixed-header':fixedHeader}">
           <navbar />
           <tags-view v-if="needTagsView"/>   <!-- 新增 -->
         </div>
         <app-main />
       </div>
     </div>
   </template>
   
   <script>
   import { Navbar, Sidebar, AppMain , TagsView} from './components'   //新增 TagsView
   import ResizeMixin from './mixin/ResizeHandler'
   
   export default {
     name: 'Layout',
     components: {
       Navbar,
       Sidebar,
       AppMain,
       TagsView   //新增
     },
     mixins: [ResizeMixin],
     computed: {
       sidebar() {
         return this.$store.state.app.sidebar
       },
       device() {
         return this.$store.state.app.device
       },
       fixedHeader() {
         return this.$store.state.settings.fixedHeader
       },
       needTagsView() {   //新增
         return this.$store.state.settings.tagsView   //新增
       },
       classObj() {
         return {
           hideSidebar: !this.sidebar.opened,
           openSidebar: this.sidebar.opened,
           withoutAnimation: this.sidebar.withoutAnimation,
           mobile: this.device === 'mobile'
         }
       }
     },
     methods: {
       handleClickOutside() {
         this.$store.dispatch('app/closeSideBar', { withoutAnimation: false })
       }
     }
   }
   </script>
   ```

8. 修改 /src/setting.js

   ```js
   module.exports = {
   
     title: 'Vue Admin Template',
   
     /**
      * @type {boolean} true | false
      * @description Whether fix the header
      */
     fixedHeader: false,
   
     /**
      * @type {boolean} true | false
      * @description Whether show the logo in sidebar
      */
     sidebarLogo: false,
   
     /**
      * @type {boolean} true | false
      * @description Whether need tagsView
      */
     tagsView: true   //新增
   }
   
   ```

此时，配置完成。效果如下：

![image-20201111152609312](/images/2020/11/image-20201111152609312.png)   

### 控制台报错

按照如下操作后，控制台报错如下：

![image-20201111152702537](/images/2020/11/image-20201111152702537.png)

这是因为拷贝的TagsView组件默认开启了权限
/src/layout/components/TagsView/index.js

修改如下，即可解决报错。

   ![image-20201111152858682](/images/2020/11/image-20201111152858682.png)

### Affix 固钉

当在声明路由上 添加了 Affix 属性，则当前`tag`会被固定在 `tags-view`中（不可被删除）。

修改文件：@src\router\index.js

![image-20201111153454783](/images/2020/11/image-20201111153454783.png)

效果如下：

![image-20201111153535548](/images/2020/11/image-20201111153535548.png)   

   

   



