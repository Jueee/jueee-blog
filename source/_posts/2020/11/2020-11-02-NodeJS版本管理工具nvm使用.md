---
title: NodeJS版本管理工具nvm使用
layout: info
commentable: true
date: 2020-11-02
mathjax: true
mermaid: true
tags: [Node.js,软件]
categories: 
- [Node.js]
- [软件,Windows]
description: 
---

### nvm 介绍

`nvm`是一个node的版本管理工具,通俗来讲就是多个项目开发的时候,可能不是用的同一个版本的`NodeJS`开发的,这个时候我们进行二次开发调试的时候,就需要使用不同`NodeJS`的版本来进行测试,为了方便版本之间的切换,就需要使用的`nvm`来操作。

- GitHub：https://github.com/coreybutler/nvm-windows

<!--more-->

### nvm 安装

GitHub下载地址: https://github.com/coreybutler/nvm-windows/releases

- nvm-noinstall.zip： 这个是绿色免安装版本，但是使用之前需要配置
- nvm-setup.zip：这是一个安装包，下载之后点击安装，无需配置就可以使用，方便。
- Source code(zip)：zip压缩的源码
- Sourc code(tar.gz)：tar.gz的源码，一般用于Linux系统

```bash
$ nvm version
1.1.7
```

### nvm 镜像修改

将npm镜像改为淘宝的镜像 **(此步骤可选,非必要)** 将镜像改为国内是为了,提高npm的下载速度,网速高有vpn者请忽略!

1. 找到安装目录下 `settings.txt` 文件并打开

2. 新建行,加入以下代码(切记:是新加2行,不要删除之前内容)

   ```ruby
   node_mirror: https://npm.taobao.org/mirrors/node/ 
   npm_mirror: https://npm.taobao.org/mirrors/npm/
   ```

```
> nvm install 22.5.1
Node.js v22.5.1 is not yet released or available.
PS E:\code\React\my-project> npm ls available
arco-design-pro@1.0.0 E:\code\React\my-project
`-- (empty)

 nvm list
  * 21.7.3 (Currently using 64-bit executable)
    18.16.0
    11.15.0
```



### nvm 使用

- `nvm version`可以简写为nvm v：查看`NVM`版本

- `nvm list`：查看已经安装`NodeJS`版本

- `nvm list available`：显示可下载版本

- `nvm install 版本号`：安装指定的版本

  示例: `nvm install 11.15.0`

  安装最新版：`nvm install latest`

- `nvm use [version] [arch]` [arch]可以指定32/64位：切换到指定版本

  示例: `nvm use 11.15.0`

- `nvm uninstall <version>`：卸载指定版本

  示例: `nvm uninstall 11.15.0`

- `nvm root [path]` ：设置各版本安装目录，如果未设置，将使用当前目录。

- `nvm on`： 启用node.js版本管理。

- `nvm off`： 禁用node.js版本管理(不卸载任何东西)

### 解决示例

element UI 命令et -I 出现primordials is not defined

> ReferenceError: primordials is not defined

这个问题的主要原因是node的版本过高
需要使用11.15.0以下版本

问题的解决方案

- nvm切换node版本
- 卸载node重新安装11.15.0

此时，可以通过 nvm 来解决。

```bash
$ nvm install 11.15.0
$ nvm use 11.15.0
$ node -v
v11.15.0
$ npx et -i
```



