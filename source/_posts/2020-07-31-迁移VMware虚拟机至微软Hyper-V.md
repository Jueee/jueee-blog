---
title: 迁移VMware虚拟机至微软Hyper-V
layout: info
commentable: true
date: 2020-07-31
mathjax: true
mermaid: true
tags: [Windows,软件]
categories: [软件,Windows]
description: 介绍微软 Hyper-V 虚拟机的使用。
---

###  Hyper-V 虚拟机

Hyper-V是微软的一款虚拟化产品，是微软第一个采用类似Vmware ESXi和Citrix Xen的基于hypervisor的技术。

### 开启 Hyper-V

进入电脑的控制面板->程序->启用或关闭Windows功能->把Hyper-v勾上，启用后电脑会重启。

![1595925972986](/images/2020/07/1595925972986.png)

### 迁移VMware虚拟机

#### 使用微软MVMC工具实现迁移

MVMC工具可以直接由微软官网下载

> [下载链接](http://www.microsoft.com/en-us/download/details.aspx?id=42497)

下载完成后，将安装文件拷贝到要安装MVMC的服务器上。

#### 安装StarWind V2V Converter

下载StarWind V2V Converter安装文件并执行安装，安装过程按照引导进行即可。

安装完成后，打开 `StarWind V2V Image Converter`。

选择 Local file：

![1596174987682](/images/2020/07/1596174987682.png)

Next，选择 VMware虚拟机的 vmdk 文件：

![1596175078239](/images/2020/07/1596175078239.png)

再点击 Next，等待转换完成，即可。



![1596174902166](/images/2020/07/1596174902166.png)

#### 导入 vhd 文件

打开 Hyper-V，新建虚拟机。

指定名称和存储位置。

![1596175210979](/images/2020/07/1596175210979.png)

指定虚拟机的代数，选择第一代。

> Windows10 Hyper-V支持的虚拟机文件格式有两代，第一代的文件后缀为.vhd；第二代的文件后缀为.vhdx。

![1596175283830](/images/2020/07/1596175283830.png)

分配内存：

![1596175352095](/images/2020/07/1596175352095.png)

配置网络：

![1596175380895](/images/2020/07/1596175380895.png)

选择指定刚刚生成的.vhd文件：

![1596175428931](/images/2020/07/1596175428931.png)

转换导入成功，接下来，虚拟机就可以运行了。

### Hyper-v虚拟机联网配置

#### 新建虚拟交换机

选择：

![1596175872059](/images/2020/07/1596175872059.png)

输入交换机名称和选择外部网络，可以看到外部网络的下拉框的选项，这里选择当前计算机的联网方式。

如何知道当前使用什么方式联网呢？---查看网络适配器。

![1596176082370](/images/2020/07/1596176082370.png)

**如果主机切换了联网方式，只要去虚拟机里改下对应的下拉选项即可。**

![1596175973333](/images/2020/07/1596175973333.png)

点击确定，建立虚拟交换机。

#### 更改虚拟机的网络适配器

右键---设置---网络适配器：

![1596176189357](/images/2020/07/1596176189357.png)

### debian 设置网络

问题描述：

配置完/etc/networking/interfaces后，使用 /etc/init.d/networking restart 出现启动失败，根据提示输入systemctl status networking.service 发现不认识/etc/networking/interfaces中配置的虚拟网卡(或者是因为虚拟机的重新移动导致的设备不匹配问题等)

解决方法：

首先可以查看etc/udev/rules.d/70-persistent-net.rules 是否存在，如果存在，则删除 rm etc/udev/rules.d/70-persistent-net.rules，重启即可

如果etc/udev/rules.d/70-persistent-net.rules 不存在，则ifconfig -a查看全部网卡，修改/etc/networking/interfaces中的网卡名和ifconfig -a命令显示的网卡名匹配，重启网络即可。

