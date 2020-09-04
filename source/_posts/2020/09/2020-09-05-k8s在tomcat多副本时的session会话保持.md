---
title: k8s在tomcat多副本时的session会话保持
layout: info
commentable: true
date: 2020-09-05
mathjax: true
mermaid: true
tags: [k8s]
categories: k8s
description: 
---

### 出现问题

通过kubernetes部署了tomcat+mysql服务，设置tomcat多副本时发现首页登陆无法跳转的情况，经排查是由于session问题引起的。

kubernetes 上可以多实例（pod）高负载运行，但是如果应用如果没有做session 同步的话，就会导致 session 不一致。
kubernetes 有session 亲和性的功能（每个client每次访问，都会匹配到对应session的后端）。

<!--more-->

### 解决方案

此时，在service的配置文件中加入 `sessionAffinity: ClientIP`，功能是选择与请求来源ip更接近的pod，这样就会固定同一个session。

如下图所示：

![1599216595277](/images/2020/09/1599216595277.png)

备注：这种方法目前只适用使用nodeport暴露服务的情况。

`spec.sessionAffinity` 字段用于定义要使用的粘性会话的类型，它仅支持使用“ None” 和“ ClientIP” 两种属性值。

也可以使用打补丁的方式进行修改yaml内的内容，如下：

```powershell
# session保持，同一ip访问同一个pod
kubectl patch svc myapp -p '{"spec":{"sessionAffinity":"ClusterIP"}}'  
# 取消session 
kubectl patch svc myapp -p '{"spec":{"sessionAffinity":"None"}}'    
```

### Session 超时时间

Service affinity 的效果仅仅在一段时间内生效，默认值为10800秒，超出时长，客户端再次访问会重新调度。

该机制仅能基于客户端IP地址识别客户端身份，它会将经由同一个NAT服务器进行原地址转换的所有客户端识别为同一个客户端，由此可知，其调度的效果并不理想。

Service 资源 通过 `.spec.sessionAffinity` 和 `.spec.sessionAffinityConfig` 两个字段配置粘性会话。

如果您还想指定时间，则需要添加以下内容：

```yaml
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10
```

### Session Affinity

会话保持(Session Affinity),有时又称粘滞会话(Sticky Sessions), 是负载均衡领域设计需要着力解决的重要问题之一，也是一个相对比较复杂的问题。

会话保持是指在负载均衡器上的一种机制，在完成负载均衡任务的同时，还负责一系列相关连的访问请求会分配到一台服务器上｡

当用户向服务器发起请求，服务器创建一个session，并把session id以cookie的形式写回给客户。