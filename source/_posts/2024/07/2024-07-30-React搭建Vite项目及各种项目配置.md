---
title: React搭建Vite项目及各种项目配置
layout: info
commentable: true
date: 2024-07-30
mathjax: true
mermaid: true
tags: [React]
categories: [React]
description: 
---

### 配置文档

- https://vitejs.dev/config/

<!--more-->

### 设置项目访问前缀

在 `vite.config.js` 中，你可以按照以下方式配置：

```javascript
export default {
  base: '/my-prefix/',
}
```

或者：

```javascript
export default defineConfig(({ command, mode }) => {
  return {
    base: '/my-prefix/'
  }
});
```

### 引用环境变量

确保你在项目根目录下创建了正确的 `.env` 文件，并在其中定义了 `VITE_APP_BASE` 变量。在 `.env` 文件中应该有类似如下的内容：

   ```
   VITE_BASE_PATH=/my-prefix/
   ```

在 `vite.config.js` 中，你可以按照以下方式配置：

```javascript
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ command, mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  return {
    base: env.VITE_BASE_PATH
  }
});
```

修改访问路由：

```javascript
<BrowserRouter basename={import.meta.env.VITE_BASE_PATH}>
</BrowserRouter>
```

修改跳转页面：

```javascript
window.location.href = '/login';
// 修改为：
window.location.href = import.meta.env.VITE_BASE_PATH+'login';
```

### Windows运行编译的dist

全局安装serve模块：

```
npm i -g serve
```

进入到dist文件内，运行服务：

```
cd dist
serve
```



```
npm install --save jsencrypt
```









