---
title: 基于React搭建ArcoDesign管理模板
layout: info
commentable: true
date: 2024-07-29
mathjax: true
mermaid: true
tags: [React,ArcoDesign]
categories: [React,ArcoDesign]
description: 
---

### 异常处理

出现异常

```
husky - Git hooks installed
Usage:
  husky install [dir] (default: .husky)
  husky uninstall
  husky set|add <file> [cmd]
npm ERR! code 2
npm ERR! path E:\code\React\hello-arco
npm ERR! command failed
npm ERR! command C:\Windows\system32\cmd.exe /d /s /c husky install && husky add .husky/pre-commit 'npm run pre-commit'
```

处理方式

```
rm -rf .git/hooks  // 删除项目路径下的 .git/hooks 文件夹
npm install
```

For Husky v7 or greater, do the following:

```sh
# For NPM
 npm install husky@7 --save-dev \
      && npx husky-init \
      && npm exec -- github:typicode/husky-4-to-7 --remove-v4-config

# For Yarn
 yarn add husky@7 --dev \
  && npx husky-init \
  && npm exec -- github:typicode/husky-4-to-7 --remove-v4-config
# or
 yarn add husky@7 --dev \
  && yarn dlx husky-init --yarn2 \
  && npm exec -- github:typicode/husky-4-to-7 --remove-v4-config
```
https://stackoverflow.com/questions/66246587/how-to-fix-error-not-found-husky-run-when-committing-new-code
