---
title: 优先级队列PriorityQueue应用汇总
layout: info
commentable: true
date: 2021-07-27
mathjax: true
mermaid: true
tags: [Java,JavaClass]
categories: [Java,JavaClass]
description: 
---

### 优先级队列

队列的核心思想就是先进先出，这个优先级队列有点不太一样。

优先级队列中，数据按关键词有序排列，插入新数据的时候，会自动插入到合适的位置保证队列有序。

<!--more-->

#### 升序

```java
PriorityQueue<Integer> queue = new PriorityQueue<>((a, b) -> a - b);
```

#### 降序

```java
PriorityQueue<Integer> queue = new PriorityQueue<>((a, b) -> b - a);
```

### 具体应用

#### 滑动窗口最大值

```java
public int[] maxSlidingWindow(int[] nums, int k) {
    PriorityQueue<int[]> queue = new PriorityQueue<>((a, b) -> b[0] != a[0] ? b[0] - a[0] : a[1] - b[1]);
    int len = nums.length;
    int[] data = new int[len + 1 - k];
    for (int i = 0; i < len; i++) {
        queue.add(new int[]{nums[i], i});
        if (i + 1 >= k) {
            int c = i + 1 - k;
            // 循环判断当前队首是否在窗口中，窗口的左边界为i-k
            while (queue.peek()[1] <= i - k) {
                queue.poll();
            }
            data[c] = queue.peek()[0];
        }
    }
    return data;
}
```

#### 数据流的中位数

```java
class MedianFinder {
    int count = 0;
    PriorityQueue<Integer> queueMin = new PriorityQueue<>((a, b) -> b - a);  // 小队列，降序
    PriorityQueue<Integer> queueMax = new PriorityQueue<>((a, b) -> a - b);  // 大队列，升序

    public MedianFinder() {

    }

    public void addNum(int num) {
        count++;
        queueMax.add(num);  // 先把数值放进大队列
        queueMin.add(queueMax.poll()); // 把大队列中的最小值，放进小队列
        if (count % 2 == 0) {
            queueMax.add(queueMin.poll()); // 如果是偶数，把小队列的最大值，放进大队列
        }
    }

    public double findMedian() {
        if (count % 2 == 0) {
            return (double) (queueMin.peek() + queueMax.peek()) / 2;
        } else {
            return queueMin.peek();
        }
    }
}
```