---
title: 为 GitLab 代码库配置 Specific Runner
layout: info
commentable: true
date: 2020-07-25
mathjax: true
mermaid: true
tags: GitLab
categories: GitLab
description: 在 GitLab 的 CI/CD 流程。
---

### 添加 k8s 集群

单击**添加现有集群**选项卡，然后填写详细信息：

- **Kubernetes集群名称**（必填）-您希望为**集群指定**的名称。

- **环境范围**（必需）-  [与](index.md#setting-the-environment-scope-premium)此集群[相关的环境](index.md#setting-the-environment-scope-premium)。

- **API URL**（必填）-这是GitLab用于访问Kubernetes API的URL。Kubernetes公开了几个API，我们希望所有API都具有通用的“基本” URL，例如，`https://kubernetes.example.com`而不是`https://kubernetes.example.com/api/v1`。

  通过运行以下命令获取API URL：

  ```
  kubectl cluster-info | grep 'Kubernetes master' | awk '/http/ {print $NF}'
  ```

- **CA证书**（必需）-需要有效的Kubernetes证书才能对集群进行身份验证。我们将使用默认创建的证书。

  - 用列出秘密`kubectl get secrets`，并命名类似  `default-token-xxxxx`。复制该令牌名称以在下面使用。

  - 通过运行以下命令获取证书：

    ```
    kubectl get secret <secret name> -o jsonpath="{['data']['ca\.crt']}" | base64 --decode
    ```

    注意：**注意：**  如果命令返回整个证书链，则需要在证书链 底部复制*root ca*证书。

- **令牌** -GitLab使用服务令牌对Kubernetes进行身份验证，该服务令牌的范围仅限于特定的`namespace`。 **使用的令牌应属于具有cluster-admin 特权的服务帐户  。**要创建此服务帐户：

  1. 创建一个`gitlab-admin-service-account.yaml`包含内容的文件：

     ```
     apiVersion: v1
     kind: ServiceAccount
     metadata:
       name: gitlab-admin
       namespace: kube-system
     ---
     apiVersion: rbac.authorization.k8s.io/v1beta1
     kind: ClusterRoleBinding
     metadata:
       name: gitlab-admin
     roleRef:
       apiGroup: rbac.authorization.k8s.io
       kind: ClusterRole
       name: cluster-admin
     subjects:
     - kind: ServiceAccount
       name: gitlab-admin
       namespace: kube-system
     ```

  2. 将服务帐户和群集角色绑定应用于您的群集：

     ```
     kubectl apply -f gitlab-admin-service-account.yaml
     ```

     您将需要`container.clusterRoleBindings.create`许可权才能创建集群级角色。如果您没有此权限，则可以选择启用基本身份验证，然后`kubectl apply`以管理员身份运行  命令：

     ```
     kubectl apply -f gitlab-admin-service-account.yaml --username=admin --password=<password>
     ```

     注意：**注意：**  可以打开基本身份验证，并可以使用Google Cloud Console获取密码凭据。

     输出：

     ```
     serviceaccount "gitlab-admin" created
     clusterrolebinding "gitlab-admin" created
     ```

  3. 检索`gitlab-admin`服务帐户的令牌：

     ```
     kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep gitlab-admin | awk '{print $1}')
     ```

     复制`<authentication_token>`输出中的值：

     ```
     Name:         gitlab-admin-token-b5zv4
     Namespace:    kube-system
     Labels:       <none>
     Annotations:  kubernetes.io/service-account.name=gitlab-admin
                   kubernetes.io/service-account.uid=bcfe66ac-39be-11e8-97e8-026dce96b6e8
     
     Type:  kubernetes.io/service-account-token
     
     Data
     ====
     ca.crt:     1025 bytes
     namespace:  11 bytes
     token:      <authentication_token>
     ```

### 配置 Specific Runner

在 GitLab 的 CI/CD 流程中具体执行任务的节点叫做 [runner](https://docs.gitlab.com/runner/)。GitLab 中有两种类型的 runner：

- **Shared Runners** 由 GitLab 管理员配置的公有 runner。多个项目公用。作为开发人员无需配置，可以直接使用。
- **Specific Runners** 开发人员为每个代码库单独配置的专属 runner。只能执行所属代码库的任务。需要开发人员手动搭建。

由于我厂的 GitLab 并没有配置任何 Shared Runner。所以只能选择在自己的台式机上手动搭建。

### 下载 runner 可执行文件

根据你的环境下载 [x86](https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-windows-386.exe) 或者 [amd64](https://gitlab-runner-downloads.s3.amazonaws.com/latest/binaries/gitlab-runner-windows-amd64.exe) 版本。

创建 `D:\GitLab-Runner` 目录，将刚刚下载好的文件复制到该目录并重命名为 `gitlab-runner.exe`。

### 获取配置信息

进入代码库主页，依次点击 `Settings` => `CI / CD` => `Runners settings`。

![1595562311495](/images/2020/07/1595562311495.png)

这里展开的信息中有两个字段需要我们记下来。分别是一个 URL 和一个 Token。

![1595562367478](/images/2020/07/1595562367478.png)

### 注册 runner

#### Linux

```
k exec -it runner-gitlab-runner-74cf6f794b-22vln gitlab-runner register -n gitlab-managed-apps
```

#### Windows

进入 `D:\GitLab-Runner` 目录执行命令：

```yml
./gitlab-runner.exe register
```

#### 进行注册

执行完后会进入一个交互式的配置流程，你需要回答以下问题：

- `Please enter the gitlab-ci coordinator URL`：填入上一步获取的 URL
- `Please enter the gitlab-ci token for this runner`：填入上一步获取的 Token
- `Please enter the gitlab-ci description for this runner`：给你的 runner 起一个名字
- `Please enter the gitlab-ci tags for this runner (comma separated)`：GitLab 允许我们给 runner 设置标签，设置好后该 runner 只会执行拥有相同标签的任务。由于我们的 runner 只为我们自己的代码库服务，所以此处不做过多配置。留空即可。
- `Whether to lock Runner to current project`：该 runner 是否应该锁定在当前项目上。由于我们是自己用，选 `true` 即可。
- `Please enter the executor: ssh, docker+machine, docker-ssh+machine, kubernetes, docker, parallels, virtualbox, docker-ssh, shell: docker`：选择任务执行环境，我们选择最简单的 `shell`。

### 验证服务已启动

进入代码库主页，依次点击 `Settings` => `CI / CD` => `Runners settings`。

![1595562200358](/images/2020/07/1595562200358.png)


