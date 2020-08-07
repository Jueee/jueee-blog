---
title: 使用 Arthas 热更新 Java 代码
layout: info
commentable: true
date: 2020-07-16
mathjax: true
mermaid: true
tags: [Java诊断,Arthas]
categories: [Java,Java诊断]
description: 所谓的 Java 热更新是指在不重启项目的情况下实现代码的更新与替换。使用它可以实现不停机更新 Java 程序，尤其是对那些启动非常耗时的 Java 项目来说，更是效果显著。

---

Arthas（阿尔萨斯）是 Alibaba 开源的一款 Java 诊断工具，使用它我们可以监控和排查 Java 程序，然而它还提供了非常实用的 Java 热更新功能。

所谓的 Java 热更新是指在不重启项目的情况下实现代码的更新与替换。使用它可以实现不停机更新 Java 程序，尤其是对那些启动非常耗时的 Java 项目来说，更是效果显著。

### Arthas 使用

#### Arthas资料

Github 地址：

> [ https://github.com/alibaba/arthas](https://github.com/alibaba/arthas)

Arthas
用户文档：

> [https://alibaba.github.io/arthas/](https://alibaba.github.io/arthas/)

#### 下载 Arthas

首先，我们先把 Arthas 的 Jar 包下载到本地，它的下载地址是：

> https://alibaba.github.io/arthas/arthas-boot.jar

#### 启动 Arthas

我们只需要使用普通的 jar 包启动命令：`java -jar arthas-boot.jar` 来启动 Arthas 即可。

#### Windows 运行

Windows 需要以管理员方式运行，bat 脚本如下：

```bat
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /d "%~dp0"
java -jar arthas-boot.jar
```

### 热更新 Java 代码

假如我们原来的代码是这样的：

```java
package sample.redefine;

import java.util.concurrent.TimeUnit;

public class RedefineSuccess {

	public static void main(String[] args) throws InterruptedException {
        while (true) {
            TimeUnit.SECONDS.sleep(3);
            printFlag();
        }
    }

    private static void printFlag() {
        boolean flag = true;
        if (flag) {
            System.out.println("flag is true.");
        } else {
            System.out.println("flag is false.");
        }
    }
}
```

我们现在想要把 `flag` 变量改为 `false` 就可以这样来做：

1. 使用 Arthas 的内存编译工具将新的 Java 代码编译为字节码；
2. 使用 Arthas 的 `redefine` 命令实现热更新。

#### 编译字节码

首先，我们需要将新的 Java 代码编译为字节码，我们可以通过 Arthas 提供的 `mc` 命令实现，`mc` 是 Memory Compiler（内存编译器）的缩写。

实现示例如下：

```java
[arthas@10200]$ mc C:/arthas-demo/src/main/java/sample/redefine/RedefineSuccess.java -d  E:
Memory compiler output:
E:\sample\redefine\RedefineSuccess.class
Affect(row-cnt:1) cost in 500 ms.
```

其中 `-d` 表示编译文件的存放位置。

> 小贴士：我们也可以使用 javac App.java 生成的字节码，它与此步骤执行的结果相同。

#### 执行热更新

有了字节码文件之后，我们就可以使用 `redefine` 命令来实现热更新了，实现示例如下：

```
[arthas@10200]$ redefine e:/sample/redefine/RedefineSuccess.class
redefine success, size: 1
```

从上述结果可以看出，热更新执行成功，此时我们去控制台查看执行结果，如下图所示：

![1594883244673](/images/2020/07/1594883244673.png)

这说明热更新执行确实成功了。

### 结合 jad/mc 命令使用

```
jad --source-only com.example.demo.arthas.user.UserController > /tmp/UserController.java
mc /tmp/UserController.java -d /tmp
redefine /tmp/com/example/demo/arthas/user/UserController.class
```

- jad命令反编译，然后可以用其它编译器，比如vim来修改源码
- mc命令来内存编译修改过的代码
- 用redefine命令加载新的字节码

### 热更新注意事项

#### redefine 特别说明

`redefine`命令和`jad`/`watch`/`trace`/`monitor`/`tt`等命令会冲突。

执行完`redefine`之后，如果再执行上面提到的命令，则会把`redefine`的字节码重置。 

原因是jdk本身redefine和Retransform是不同的机制，同时使用两种机制来更新字节码，只有最后修改的会生效。

#### 条件限制

使用热更新功能有一些条件限制，我们只能用它来修改方法内部的一些业务代码，如果我们出现了以下任意一种情况，那么热更新就会执行失败：

1. 增加类属性（类字段）；
2. 增加或删除方法；
3. 替换正在运行的方法。

最后一条我们需要单独说明一下，假如我们把上面的示例改为如下代码：


 ```java
package sample.redefine;

import java.util.concurrent.TimeUnit;

public class RedefineError {

	public static void main(String[] args) throws InterruptedException {
		while (true) {
			TimeUnit.SECONDS.sleep(3);
			boolean flag = false;
	        if (flag) {
	            System.out.println("flag is true.");
	        } else {
	            System.out.println("flag is false.");
	        }
		}
	}
}

 ```

那么此时我们再进行热更新操作修改 `flag` 的值，那么就会执行失败，因为我们替换的是正在运行中的方法，而我们正常示例中的代码之所以能成功，是因为我们在 `while` 无线循环中调用了另一个方法，而那个方法是被间歇性使用的，因此可以替换成功。