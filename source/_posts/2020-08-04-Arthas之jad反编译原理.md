---
title: Arthas之jad反编译原理
layout: info
commentable: true
date: 2020-08-04
mathjax: true
mermaid: true
tags: [Java诊断,Arthas]
categories: [Java,Java诊断]
description: Arthas是阿里巴巴开源的Java应用诊断利器，本文介绍Arthas里jad命令的实现原理。

---

### jad 命令介绍

jad 即 java decompiler，把 JVM 已加载类的字节码反编译成Java代码。

> [https://alibaba.github.io/arthas/jad.html](https://alibaba.github.io/arthas/jad.html)

### 获取到类的字节码

反编译有两部分工作：

1. 获取到字节码
2. 反编译为Java代码

那么怎么从运行的JVM里获取到字节码？

最常见的思路是，在`classpaths`下面查找，比如 `ClassLoader.getResource("java/lang/String.class")`，但是这样子查找到的字节码不一定对。比如可能有多个冲突的jar，或者有Java Agent修改了字节码。

### ClassFileTransformer机制

从JDK 1.5起，有一套`ClassFileTransformer`的机制，Java Agent通过`Instrumentation`注册`ClassFileTransformer`，那么在类加载或者`retransform`时就可以回调修改字节码。

显然，在Arthas里，要增强的类是已经被加载的，所以它们的字节码都是在`retransform`时被修改的。
通过显式调用`Instrumentation.retransformClasses(Class<?>...)`可以触发回调。

Arthas里增强字节码的`watch`/`trace`/`stack`/`tt`等命令都是通过`ClassFileTransformer`来实现的。

`java.lang.instrument.ClassFileTransformer`的接口如下：

```java
public interface ClassFileTransformer {
    byte[]
    transform(  ClassLoader         loader,
                String              className,
                Class<?>            classBeingRedefined,
                ProtectionDomain    protectionDomain,
                byte[]              classfileBuffer)
        throws IllegalClassFormatException;
}
```

看到这里，读者应该猜到`jad`是怎么获取到字节码的了：

1. 注册一个`ClassFileTransformer`
2. 通过`Instrumentation.retransformClasses`触发回调
3. 在回调的`transform`函数里获取到字节码
4. 删掉注册的`ClassFileTransformer`

### 使用cfr来反编译

获取到字节码之后，怎样转换为Java代码呢？

以前大家使用比较多的反编译软件可能是`jd-gui`，但是它不支持JDK8的lambda语法和一些新版本JDK的特性。

后面比较成熟的反编译软件是`cfr`，它以前是不开源的。直到最近的`0.145`版本，作者终于开源了，可喜可贺。地址是

> [https://github.com/leibnitz27/cfr](https://github.com/leibnitz27/cfr)

在Arthas `jad`命令里，通过调用`cfr`来完成反编译。

### jad 命令的缺陷

99%的情况下，`jad`命令dump下来的字节码是准确的，除了一些极端情况。

1. 因为JVM里注册的`ClassFileTransformer`可能有多个，那么在JVM里运行的字节码里，可能是被多个`ClassFileTransformer`处理过的。
2. 触发了`retransformClasses`之后，这些注册的`ClassFileTransformer`会被依次回，上一个处理的字节码传递到下一个。
   所以不能保证这些`ClassFileTransformer`第二次执行会返回同样的结果。
3. 有可能一些`ClassFileTransformer`会被删掉，触发`retransformClasses`之后，之前的一些修改就会丢失掉。

所以目前在Arthas里，如果开两个窗口，一个窗口执行`watch`/`tt`等命令，另一个窗口对这个类执行`jad`，那么可以观察到`watch`/`tt`停止了输出，实际上是因为字节码在触发了`retransformClasses`之后，`watch`/`tt`所做的修改丢失了。

### 精确获取字节码

如果想精确获取到JVM内运行的Java字节码，可以使用这个`dumpclass`工具，它是通过`sa-jdi.jar`来实现的，保证dump下来的字节码是JVM内所运行的。

> [https://github.com/hengyunabc/dumpclass](https://github.com/hengyunabc/dumpclass)

### cfr反编译示例

参考Arthas代码：[com.taobao.arthas.core.util.Decompiler.java](https://github.com/alibaba/arthas/blob/master/core/src/main/java/com/taobao/arthas/core/util/Decompiler.java)

#### 引入依赖

首先，需要引入 maven 依赖：

```xml
<dependency>
	<groupId>org.benf</groupId>
	<artifactId>cfr</artifactId>
	<version>0.150</version>
</dependency>
```

#### 编写方法

编写反编译类 `sample.utils.Decompiler`：

```java

public static String decompile(String classFilePath, String methodName) {
	return decompile(classFilePath, methodName, false);
}

/**
 * @param classFilePath
 * @param methodName
 * @param hideUnicode
 * @return
 */
public static String decompile(String classFilePath, String methodName, boolean hideUnicode) {
	final StringBuilder result = new StringBuilder(8192);

	OutputSinkFactory mySink = new OutputSinkFactory() {
		@Override
		public List<SinkClass> getSupportedSinks(SinkType sinkType, Collection<SinkClass> collection) {
			return Arrays.asList(SinkClass.STRING, SinkClass.DECOMPILED, SinkClass.DECOMPILED_MULTIVER,
							SinkClass.EXCEPTION_MESSAGE);
		}

		@Override
		public <T> Sink<T> getSink(final SinkType sinkType, SinkClass sinkClass) {
			return new Sink<T>() {
				@Override
				public void write(T sinkable) {
					// skip message like: Analysing type demo.MathGame
					if (sinkType == SinkType.PROGRESS) {
						return;
					}
					result.append(sinkable);
				}
			};
		}
	};

	HashMap<String, String> options = new HashMap<String, String>();
	/**
	 * @see org.benf.cfr.reader.util.MiscConstants.Version.getVersion() Currently,
	 *      the cfr version is wrong. so disable show cfr version.
	 */
	options.put("showversion", "false");
	options.put("hideutf", String.valueOf(hideUnicode));
	if (!StringUtils.isBlank(methodName)) {
		options.put("methodname", methodName);
	}

	CfrDriver driver = new CfrDriver.Builder().withOptions(options).withOutputSink(mySink).build();
	List<String> toAnalyse = new ArrayList<String>();
	toAnalyse.add(classFilePath);
	driver.analyse(toAnalyse);

	return result.toString();
}
```

#### 测试

```
String className = "sample/redefine/RedefineSuccess.class";
String classPath = Thread.currentThread().getContextClassLoader().getResource(className).getFile();
System.out.println(classPath);

String result = decompile(classPath, null);
System.out.println(result);

String result2 = decompile(classPath, "printFlag");
System.out.println(result2);
```

#### 输出

```java
/C:/Codes/JavaWorkSpace/workspace48/arthas-demo/target/classes/sample/redefine/RedefineSuccess.class
/*
 * Decompiled with CFR.
 */
package sample.redefine;

import java.util.concurrent.TimeUnit;

public class RedefineSuccess {
    public static void main(String[] args) throws InterruptedException {
        while (true) {
            TimeUnit.SECONDS.sleep(3L);
            RedefineSuccess.printFlag();
        }
    }

    private static void printFlag() {
        boolean flag = false;
        if (flag) {
            System.out.println("flag is true.");
        } else {
            System.out.println("flag is false.");
        }
    }
}

private static void printFlag() {
    boolean flag = false;
    if (flag) {
        System.out.println("flag is true.");
    } else {
        System.out.println("flag is false.");
    }
}
```

### 参考文档

> [http://hengyunabc.github.io/arthas-jad/](http://hengyunabc.github.io/arthas-jad/)