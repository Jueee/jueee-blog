---
title: java中排序报：Comparison method violates its general contract异常的解决
layout: info
commentable: true
date: 2022-06-08
mathjax: true
mermaid: true
tags: [Java,JavaError]
categories: [Java,JavaError]
description: 
---

使用 `Collections.sort` 排序时，可能出现如下报错：

![image-20220608142210621](/images/2022/06/image-20220608142210621.png)

### 问题复现

```java
Integer[] array = {0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 2, 30, 0, 3};
List<Integer> list = Arrays.asList(array);
Collections.sort(list, new Comparator<Integer>() {
    @Override
    public int compare(Integer o1, Integer o2) {
        return o1 > o2 ? 1 : -1;	// 错误的方式
    }
});
System.out.println(list);
```

### 问题原因

Collections.sort() 在 JDK6 和 JDK7 中实现的底层排序算法变了，在 JDK6 中使用的时 MergeSort 排序，而在 JDK7 中使用的是 TimSort。

Timsort 结合了归并排序和插入排序。这个算法在实现过程中明确需要：严格的单调递增或者递减来保证算法的稳定性。

![image-20220608142704366](/images/2022/06/image-20220608142704366.png)

- `sgn(compare(x, y)) == -sgn(compare(y, x))`
- `((compare(x, y)>0) && (compare(y, z)>0)) implies compare(x, z)>0`
- `compare(x, y)==0 implies that sgn(compare(x, z))==sgn(compare(y, z)) for all z`

说明：

- 自反性：x，y 的比较结果和 y，x 的比较结果相反。
- 传递性：x>y,y>z,则 x>z。
- 对称性：x=y,则 x,z 比较结果和 y，z 比较结果相同。（也叫可逆比较）

### 问题解决

#### 方式一：使用 compareTo

官方推荐使用该方式。

```java
Collections.sort(list, new Comparator<Integer>() {
    @Override
    public int compare(Integer o1, Integer o2) {
        return o1.compareTo(o2);
    }
});
```

#### 方式二：判断相等

```java
Collections.sort(list, new Comparator<Integer>() {
    @Override
    public int compare(Integer o1, Integer o2) {
        if (o1 > o2) {
            return 1;
        } else if (o1 < o2) {
            return -1;
        } else {
            return 0;
        }
    }
});
```

#### 方式三：增加 JVM 参数

给jvm添加启动参数：

```
 -Djava.util.Arrays.useLegacyMergeSort=true
```

但是不建议使用这种方式。这种的弊端在于会导致无法使用 jdk1.7里面的新特性，对后期的升级是有不可知的影响的。

### 需要注意

并不一定你的集合中存在相等的元素，并且比较函数不符合上面的严谨定义，就一定会稳定浮现此异常。

实际上我们在生产环境出现此异常的概率很小，毕竟java并不会蠢到先去把整个数组都校验一遍，实际上它是在排序的过程中发现你不符合此条件的。

所以有可能某种集合顺序让你刚好绕过了此判断。

一个会引发该异常的Case：

```java
Integer[] array = {0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 2, 30, 0, 3};
```

