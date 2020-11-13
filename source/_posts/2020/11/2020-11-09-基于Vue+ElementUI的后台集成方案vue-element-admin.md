---
title: 基于Vue+ElementUI的后台集成方案vue-element-admin
layout: info
commentable: true
date: 2020-11-09
mathjax: true
mermaid: true
tags: [Vue,Element]
categories: Vue
description: 
---

### vue-element-admin

vue-element-admin 是一个后台前端解决方案，它基于 [vue](https://github.com/vuejs/vue) 和 [element-ui](https://github.com/ElemeFE/element) 实现。

它使用了最新的前端技术栈，内置了 i18n 国际化解决方案，动态路由，权限验证，提炼了典型的业务模型，提供了丰富的功能组件，它可以帮助你快速搭建企业级中后台产品原型。

- [GitHub](https://github.com/PanJiaChen/vue-element-admin)，[在线预览](https://panjiachen.github.io/vue-element-admin/)，[Wiki](https://github.com/PanJiaChen/vue-element-admin/wiki)
- [Gitee](https://gitee.com/panjiachen/vue-element-admin)，[在线预览](https://panjiachen.gitee.io/vue-element-admin/)，[使用文档](https://panjiachen.gitee.io/vue-element-admin-site/zh/guide/)
- [OSChina](https://www.oschina.net/p/vue-element-admin)

<!--more-->

vue-element-admin 的定位是后台集成方案，不适合当基础模板来开发。

#### 目录结构

```bash
├── build                      // 构建相关  
├── config                     // 配置相关
├── src                        // 源代码
│   ├── api                    // 所有请求
│   ├── assets                 // 主题 字体等静态资源
│   ├── components             // 全局公用组件
│   ├── directive              // 全局指令
│   ├── filtres                // 全局 filter
│   ├── icons                  // 项目所有 svg icons
│   ├── lang                   // 国际化 language
│   ├── mock                   // 项目mock 模拟数据
│   ├── router                 // 路由
│   ├── store                  // 全局 store管理
│   ├── styles                 // 全局样式
│   ├── utils                  // 全局公用方法
│   ├── vendor                 // 公用vendor
│   ├── views                   // view
│   ├── App.vue                // 入口页面
│   ├── main.js                // 入口 加载组件 初始化等
│   └── permission.js          // 权限管理
├── static                     // 第三方不打包资源
│   └── Tinymce                // 富文本
├── .babelrc                   // babel-loader 配置
├── eslintrc.js                // eslint 配置项
├── .gitignore                 // git 忽略项
├── favicon.ico                // favicon图标
├── index.html                 // html模板
└── package.json               // package.json
```

#### 关联项目

- 基础模板： [vueAdmin-template](https://gitee.com/panjiachen/vue-admin-template) 
- 桌面终端： [electron-vue-admin](https://github.com/PanJiaChen/electron-vue-admin)

### vue-admin-template

- GitHub：https://github.com/PanJiaChen/vue-admin-template
- 演示地址：https://panjiachen.github.io/vue-admin-template

**vueAdmin-template** 主要是基于vue-cli webpack模板为基础开发的，引入了如下dependencies:

- element-ui 饿了么出品的vue2.0 pc UI框架
- axios 一个现在主流并且很好用的请求库 支持Promise
- js-cookie 一个轻量的JavaScript库来处理cookie
- normalize.css 格式化css
- nprogress 轻量的全局进度条控制
- vuex 官方状态管理
- vue-router 官方路由


