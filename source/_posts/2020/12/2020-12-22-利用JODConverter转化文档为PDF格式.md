---
title: 利用JODConverter转化文档为PDF格式
layout: info
commentable: true
date: 2020-12-22
mathjax: true
mermaid: true
tags: [Apache,OpenOffice]
categories: 
- [Apache,OpenOffice]
- [Java,JavaJar]
description: 
---

### JODConverter 介绍

JODConverter，是一个Java的OpenDocument文件转换器，可以进行许多文件格式的转换。

JODConverter 依赖于OpenOffice.org 或者 LibreOffice 提供的服务来进行转换，它能将 Microsoft Office文档（Word，Excel，PowerPoint）转换为PDF格式。

<!--more-->

### 老版本转换

#### maven 引入

```xml
<dependency>
    <groupId>com.artofsolving</groupId>
    <artifactId>jodconverter</artifactId>
    <version>2.2.1</version>
</dependency>
```

#### 转换代码

参数分别表示：

- ip：OpenOffice服务的IP地址。
- port：OpenOffice 服务的端口地址。
- sourceFile：转换来源文档全路径。
- destFile：转换生成的 PDF 文档保存全路径。

```java
public static boolean office2PDF(String ip, int port, String sourceFile, String destFile) {
    try {
        File inputFile = new File(sourceFile);
        if (!inputFile.exists()) {
            log.info("找不到源文件");
            return false;// 找不到源文件, 则返回-1
        }
        // 如果目标路径不存在, 则新建该路径
        File outputFile = new File(destFile);
        if (!outputFile.getParentFile().exists()) {
            outputFile.getParentFile().mkdirs();

        }
        // connect to an OpenOffice.org instance running on port 8100
        OpenOfficeConnection connection = new SocketOpenOfficeConnection(ip, port);
        connection.connect();
        // convert
        DocumentConverter converter = new StreamOpenOfficeDocumentConverter(connection);
        converter.convert(inputFile, outputFile);
        // close the connection
        connection.disconnect();
        log.info("office2PDF path：" + destFile);
        return true;
    } catch (ConnectException e) {
        log.warn("ConnectException", e);
    }

    return true;
}
```

### 新版本转换

#### 前期准备

需要先在运行服务器，安装 OpenOffice。

#### maven引入

```xml
<dependency>
    <groupId>org.jodconverter</groupId>
    <artifactId>jodconverter-local</artifactId>
    <version>4.2.2</version>
</dependency>
```

#### 转换代码

```java
public static boolean office2PDF(String sourceFile, String destFile) {
    OfficeManager officeManager
            = LocalOfficeManager.builder().install()
            .officeHome("C:\\Program Files (x86)\\OpenOffice 4")
            .build();
    try {
        File inputFile = new File(sourceFile);
        if (!inputFile.exists()) {
            log.info("找不到源文件");
            return false;// 找不到源文件, 则返回-1
        }
        // 如果目标路径不存在, 则新建该路径
        File outputFile = new File(destFile);
        if (!outputFile.getParentFile().exists()) {
            outputFile.getParentFile().mkdirs();
        }
        officeManager.start(); // Start the office process
        JodConverter.convert(new File(sourceFile)).to(outputFile).execute();
    } catch (Exception e) {
        log.error(e.getMessage(), e);
    } finally {
        OfficeUtils.stopQuietly(officeManager); // Stop the office process
    }
    return true;
}
```

#### 配置信息

使用LocalOfficeManager需要设置一些参数。使用**JODConverter**时，会采用默认配置。虽然这些配置信息不一定是最好的，但是他们更有可能被选中使用。

- **protNumbers** 和 **pipeNames**
   OpenOffice  进程间的通信可以使用TCP sockets 或者 命名管道。命名管道具有不占用TCP端口的优势（存在安全隐患），并且可能会更快一些。然而命名管道需要由JVM加载本地库，这意味着必须在`java.library.path`中设置路径，这就是为什么`pipeNames`不是默认配置的原因了。
- **officeHome**
  该属性应该设置为 OpenOffice 的安装目录。若没有配置，则创建OfficeManager时会自动检测，从LibreOffice（优先于OpenOffice）的最新版本开始。
- **processManager**
  JODConverter开始处理一个office进程时，就需要使用到进程管理器。当它开始进行这项工作，就必须要检索该进程的PID，以便在需要时能够kill it。默认情况下，JODConverter会根据JODConverter运行的操作系统来选择最佳的进程管理器。但是，在`classpath`中发现的，且继承了`ProcessManager`接口的进程管理器均可以被使用。
- **workingDir**
  该属性用来设置office临时文件配置目录。每个office进程启动时，一个文件配置目录将会被创建。当使用`InputStream/OutputStream`来转换时，这个目录也会被创建。默认由指定的路径为`java.io.tmpdir`
- **templateProfileDir**
  为了避免进程被中断或者用户使用了另一个 OpenOffice 实例，LocalOfficeManager会为 OpenOffice 进程创建一个临时配置文件目录。使用这个属性，你可以提供一个包含个性化设置的临时配置文件目录。OfficeManager会将以其为模板，来生成临时配置文件目录。所以当我们创建新的 OpenOffice 实例时，都会使用相同的配置。默认情况虾，这个临时的配置文件由 OpenOffice 使用默认配置来创建，并且其依赖于 `-nofirststartwizard`这个命令选项。
- **killExistingProcess**
  该属性能够指定，当一个包含相同`connection string`的office进程启动，是否杀死一个已经存在的office进程。默认为`true`.
- **processTimeout**
  当尝试调用一个office进程时（开始/中止），该属性可以设置超时时间，单位为毫秒。默认为`120000`（2 minutes）
- **processRetryInterval**
  每当尝试调用一个office进程时（开始/中止）的间隙，可用该属性设置延迟，单位为毫秒。默认为`250`（0.25 seconds）
- **taskExecutionTimeout**
  该属性设置执行一个任务的最大时间，若超过这个时间任务仍未执行，则当前任务被中止且执行下个任务。默认为`12000`（两分钟）
- **maxTasksPerProcess**
  该属性设置一个office进程在重启之前所能执行的最大任务数。默认为`200`个。
- **disableOpengl**
  当启动一个新的office进程时（在LibreOffice的情况下），该属性能够指定是否禁止OpenGL。如果OpenGL已经根据office进程使用的用户配置禁用，那么将不会执行任何操作。如果该属性改变，那么office进程必须重启。如果LO进程奔溃，那么你可以尝试测试该属性。默认为`false`
- **taskQueueTimeout** 该属性用来设置一个任务在转换队列中的最大生存时间。如果等待时间超过最大生存时间或者有`OfficeException`异常抛出，则任务将会从队列中移除。默认为`30000`（30 seconds）

