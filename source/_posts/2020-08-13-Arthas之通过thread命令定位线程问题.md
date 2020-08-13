---
title: Arthas之通过thread命令定位线程问题
layout: info
commentable: true
date: 2020-08-13
mathjax: true
mermaid: true
tags: [Java诊断,Arthas]
categories: [Java,Java诊断]
description: 通过Arthas中的thread命令，可以查看当前线程信息及线程的堆栈。从而可以定位线程问题。
---

通过Arthas中的thread命令，可以查看当前线程信息及线程的堆栈。从而可以定位线程问题。

### thread 命令介绍

官方文档：

> [https://alibaba.github.io/arthas/thread.html](https://alibaba.github.io/arthas/thread.html)

#### 参数说明

使用 `thread --help` 获取 thread 命令的帮助信息：

![1597314852787](/images/2020/08/1597314852787.png)

主要参数说明如下：

| 参数名称      | 参数说明                              |
| ------------- | ------------------------------------- |
| *id*          | 线程id                                |
| [n:]          | 指定最忙的前N个线程并打印堆栈         |
| [b]           | 找出当前阻塞其他线程的线程            |
| [i `<value>`] | 指定cpu占比统计的采样间隔，单位为毫秒 |

#### 线程常见状态

定位线程问题之前，先回顾一下线程的几种常见状态：

- **RUNNABLE** 运行中
- **TIMED_WAITIN** 调用了以下方法的线程会进入**TIMED_WAITING**：
  1. Thread#sleep()
  2. Object#wait() 并加了超时参数
  3. Thread#join() 并加了超时参数
  4. LockSupport#parkNanos()
  5. LockSupport#parkUntil()

- **WAITING** 当线程调用以下方法时会进入WAITING状态：
  1. Object#wait() 而且不加超时参数
  2. Thread#join() 而且不加超时参数
  3. LockSupport#park()

- **BLOCKED** 阻塞，等待锁

#### cpu占比的统计

> 这里的cpu统计的是，一段采样间隔内，当前JVM里各个线程所占用的cpu时间占总cpu时间的百分比。
>
> 其计算方法为： 首先进行一次采样，获得所有线程的cpu的使用时间(调用的是`java.lang.management.ThreadMXBean#getThreadCpuTime`这个接口)，然后睡眠一段时间，默认100ms，可以通过`-i`参数指定，然后再采样一次，最后得出这段时间内各个线程消耗的cpu时间情况，最后算出百分比。

> 注意： 这个统计也会产生一定的开销（JDK这个接口本身开销比较大），因此会看到as的线程占用一定的百分比，为了降低统计自身的开销带来的影响，可以把采样间隔拉长一些，比如5000毫秒。

> 如果想看从Java进程启动开始到现在的cpu占比情况：可以使用[show-busy-java-threads](https://github.com/oldratlee/useful-scripts/blob/master/docs/java.md#-show-busy-java-threads)这个脚本

### 示例代码

首先编写一个有各种情况的测试类运行起来，再使用 **Arthas** 进行问题定位：

```java
@Slf4j
public class ThreadDemo {

	private static HashSet<String> hashSet = new HashSet<String>();

	private static ExecutorService executorService = Executors.newFixedThreadPool(1);

	public static void main(String[] args) {
		
		addHashSetThread();	// 不断的向 hashSet 集合增加数据
		
		cpuHigh();		// 模拟 CPU 过高
		cpuNormal();
		
		thread();	// 模拟线程阻塞
		
		deadThread();	// 模拟线程死锁
	}

	/**
	 * 极度消耗CPU的线程
	 */
	private static void cpuHigh() {
		Thread thread = new Thread(() -> {
			while (true) {
				log.info("cpu start 100");
			}
		});
		// 添加到线程
		executorService.submit(thread);
	}

	/**
	 * 普通消耗CPU的线程
	 */
	private static void cpuNormal() {
		for (int i = 0; i < 10; i++) {
			new Thread(() -> {
				while (true) {
					log.info("cpu start");
					try {
						Thread.sleep(3000);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
				}
			}).start();
		}
	}

	/**
	 * 模拟线程阻塞,向已经满了的线程池提交线程
	 */
	private static void thread() {
		Thread thread = new Thread(() -> {
			while (true) {
				log.debug("thread start");
				try {
					Thread.sleep(3000);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
		});
		// 添加到线程
		executorService.submit(thread);
	}

	/**
	 * 死锁
	 */
	private static void deadThread() {
		/** 创建资源 */
		Object resourceA = new Object();
		Object resourceB = new Object();
		// 创建线程
		Thread threadA = new Thread(() -> {
			synchronized (resourceA) {
				log.info(Thread.currentThread() + " get ResourceA");
				try {
					Thread.sleep(1000);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				log.info(Thread.currentThread() + "waiting get resourceB");
				synchronized (resourceB) {
					log.info(Thread.currentThread() + " get resourceB");
				}
			}
		});

		Thread threadB = new Thread(() -> {
			synchronized (resourceB) {
				log.info(Thread.currentThread() + " get ResourceB");
				try {
					Thread.sleep(1000);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				log.info(Thread.currentThread() + "waiting get resourceA");
				synchronized (resourceA) {
					log.info(Thread.currentThread() + " get resourceA");
				}
			}
		});
		threadA.start();
		threadB.start();
	}

	/**
	 * 不断的向 hashSet 集合添加数据
	 */
	public static void addHashSetThread() {
		// 初始化常量
		new Thread(() -> {
			int count = 0;
			while (true) {
				try {
					hashSet.add("count" + count);
					Thread.sleep(10000);
					count++;
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			}
		}).start();
	}
}
```

### 定位 CPU 使用较高的线程

上面的代码例子有一个 `CPU` 空转的死循环，非常的消耗 `CPU性能`，那么怎么找出来呢？

使用 **thread**查看**所有**线程信息，同时会列出每个线程的 `CPU` 使用率，可以看到图里 ID 为12 的线程 CPU 使用100%。

![1597314558126](/images/2020/08/1597314558126.png)

使用命令 **thread 12** 查看 CPU 消耗较高的 12 号线程信息，可以看到 CPU 使用较高的方法和行数。

![1597314597613](/images/2020/08/1597314597613.png)

如果只是为了寻找 CPU 使用较高的线程，可以直接使用命令 **thread -n [显示的线程个数]** ，就可以排列出 CPU 使用率 **Top N** 的线程。

![1597314636547](/images/2020/08/1597314636547.png)

定位到的 CPU 使用最高的方法：

![1597314662083](/images/2020/08/1597314662083.png)

### 定位线程阻塞

上面的模拟代码里，定义了线程池大小为1 的线程池，然后在 `cpuHigh` 方法里提交了一个线程，在 `thread`方法再次提交了一个线程，后面的这个线程因为线程池已满，会阻塞下来。

使用 **thread | grep pool** 命令查看线程池里线程信息。

![1597314720720](/images/2020/08/1597314720720.png)

可以看到线程池有 **WAITING** 的线程：

![1597314739701](/images/2020/08/1597314739701.png)

### 定位线程死锁

上面的模拟代码里 `deadThread`方法实现了一个死锁，使用 **thread -b** 命令查看直接定位到死锁信息。

![1597314791433](/images/2020/08/1597314791433.png)