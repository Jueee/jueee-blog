---
title: Windows10找不到gpedit.msc组策略
layout: info
commentable: true
date: 2021-07-11
mathjax: true
mermaid: true
tags: [Windows]
categories: Windows
description: 
---

Windows 10 如果通过 **gpedit.msc** 无法找到组策略功能：

![image-20210711223013489](/images/2021/07/image-20210711223013489.png)

可以通过如下的批处理文件进行开启：

```bat
@echo off

pushd "%~dp0"

dir /b %systemroot%\Windows\servicing\Packages\Microsoft-Windows-GroupPolicy-ClientExtensions-Package~3*.mum >gp.txt

dir /b  %systemroot%\servicing\Packages\Microsoft-Windows-GroupPolicy-ClientTools-Package~3*.mum >>gp.txt

for /f %%i in ('findstr /i . gp.txt 2^>nul') do dism /online /norestart /add-package:"%systemroot%\servicing\Packages\%%i"

pause
```

右键管理员方式运行。

![image-20210711223155459](/images/2021/07/image-20210711223155459.png)

再次运行 **gpedit.msc**，即可正常打开组策略编辑器：

![image-20210711223243695](/images/2021/07/image-20210711223243695.png)