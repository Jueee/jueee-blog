---
title: Java中Tuple类的创建使用
layout: info
commentable: true
date: 2022-04-11
mathjax: true
mermaid: true
tags: [Java,JavaClass]
categories: [Java,JavaClass]
description: 
---

Scala 中的 Tuple 相关类是非常实用的，但是在 Java 中并没有原生支持。

下面介绍如何简单创建 Tuple 相关类并使用。

<!--more-->

### Tuple2

```java
import java.io.Serializable;
import java.util.*;
import java.util.function.Function;

public class Tuple2 <T1, T2> implements Iterable<Object>, Serializable {
    final T1 t1;
    final T2 t2;

    public Tuple2(T1 t1, T2 t2) {
        this.t1 = Objects.requireNonNull(t1, "t1");
        this.t2 = Objects.requireNonNull(t2, "t2");
    }

    public T1 getT1() {
        return this.t1;
    }

    public T2 getT2() {
        return this.t2;
    }

    public <R> Tuple2<R, T2> mapT1(Function<T1, R> mapper) {
        return new Tuple2(mapper.apply(this.t1), this.t2);
    }

    public <R> Tuple2<T1, R> mapT2(Function<T2, R> mapper) {
        return new Tuple2(this.t1, mapper.apply(this.t2));
    }

    public Object get(int index) {
        switch(index) {
            case 0:
                return this.t1;
            case 1:
                return this.t2;
            default:
                return null;
        }
    }

    public List<Object> toList() {
        return Arrays.asList(this.toArray());
    }

    public Object[] toArray() {
        return new Object[]{this.t1, this.t2};
    }

    @Override
    public Iterator<Object> iterator() {
        return Collections.unmodifiableList(this.toList()).iterator();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        } else if (o != null && this.getClass() == o.getClass()) {
            Tuple2<?, ?> tuple2 = (Tuple2)o;
            return this.t1.equals(tuple2.t1) && this.t2.equals(tuple2.t2);
        } else {
            return false;
        }
    }

    @Override
    public int hashCode() {
        int result = this.size();
        result = 31 * result + this.t1.hashCode();
        result = 31 * result + this.t2.hashCode();
        return result;
    }

    public int size() {
        return 2;
    }

    @Override
    public final String toString() {
        return "[t1]"+t1.toString()+"[t2]"+t2.toString();
    }
}
```

### Tuple3

```java
import java.util.Objects;
import java.util.function.Function;

public class Tuple3<T1, T2, T3> extends Tuple2<T1, T2> {

    final T3 t3;

    public Tuple3(T1 t1, T2 t2, T3 t3) {
        super(t1, t2);
        this.t3 = Objects.requireNonNull(t3, "t3");
    }

    public T3 getT3() {
        return this.t3;
    }

    @Override
    public <R> Tuple3<R, T2, T3> mapT1(Function<T1, R> mapper) {
        return new Tuple3(mapper.apply(this.t1), this.t2, this.t3);
    }

    @Override
    public <R> Tuple3<T1, R, T3> mapT2(Function<T2, R> mapper) {
        return new Tuple3(this.t1, mapper.apply(this.t2), this.t3);
    }

    public <R> Tuple3<T1, T2, R> mapT3(Function<T3, R> mapper) {
        return new Tuple3(this.t1, this.t2, mapper.apply(this.t3));
    }

    @Override
    public Object get(int index) {
        switch(index) {
            case 0:
                return this.t1;
            case 1:
                return this.t2;
            case 2:
                return this.t3;
            default:
                return null;
        }
    }

    @Override
    public Object[] toArray() {
        return new Object[]{this.t1, this.t2, this.t3};
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        } else if (!(o instanceof Tuple3)) {
            return false;
        } else if (!super.equals(o)) {
            return false;
        } else {
            Tuple3 tuple3 = (Tuple3)o;
            return this.t3.equals(tuple3.t3);
        }
    }

    @Override
    public int size() {
        return 3;
    }

    @Override
    public int hashCode() {
        int result = super.hashCode();
        result = 31 * result + this.t3.hashCode();
        return result;
    }
}
```
