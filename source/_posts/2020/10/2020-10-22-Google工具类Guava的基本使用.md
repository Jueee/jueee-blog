---
title: Google工具类Guava的基本使用
layout: info
commentable: true
date: 2020-10-22
mathjax: true
mermaid: true
tags: [Google,Java,JavaJar]
categories: [Java,JavaJar]
description: 
---

### Guava 介绍

Guava是一种基于开源的Java库，其中包含谷歌正在由他们很多项目使用的很多核心库。这个库是为了方便编码，并减少编码错误。这个库提供用于集合，缓存，支持原语，并发性，常见注解，字符串处理，I/O和验证的实用方法。

<!--more-->

#### Guava 优点

- 标准化 - Guava库是由谷歌托管。
- 高效 - 可靠，快速和有效的扩展JAVA标准库
- 优化 -Guava库经过高度的优化。
- 函数式编程 -增加JAVA功能和处理能力。
- 实用程序 - 提供了经常需要在应用程序开发的许多实用程序类。
- 验证 -提供标准的故障安全验证机制。
- 最佳实践 - 强调最佳的做法。

#### Guava 链接

- GitHub：https://github.com/google/guava
- 官网：https://guava.dev/

#### Guava 引入

```xml
<dependency>
    <groupId>com.google.guava</groupId>
    <artifactId>guava</artifactId>
    <version>30.0-jre</version>
</dependency>
```

### Guava 集合工具

- **`Multiset`**  
  一个扩展来设置界面，允许重复的元素。
- **`Multimap`**  
  一个扩展来映射接口，以便其键可一次被映射到多个值
- **`BiMap`**  
  一个扩展来映射接口，支持反向操作。
- **`Table`**  
  表代表一个特殊的图，其中两个键可以在组合的方式被指定为单个值。

### Guava 缓存工具

- **`LoadingCache`**

  LoadingCache提供了一个非常强大的基于内存的LoadingCache<K，V>。

  在缓存中自动加载值，它提供了许多实用的方法，在有缓存需求时非常有用。

### Guava 字符串工具

- **`Joiner`**  
  实用加入对象，字符串等。

- **`Spilter`**  
  实用程序用来分割字符串。

- **`CharMatcher`**  
  实用的字符操作。

- **`CaseFormat`**  
  实用程序，用于改变字符串格式。
  
  ```java
  CaseFormat.LOWER_HYPHEN.to(CaseFormat.LOWER_CAMEL, "test-data"); // testData
  CaseFormat.LOWER_UNDERSCORE.to(CaseFormat.LOWER_CAMEL, "test_data"); // testData
  CaseFormat.UPPER_UNDERSCORE.to(CaseFormat.UPPER_CAMEL, "test_data"); // TestData
  ```

### Guava 原语工具

作为Java的原语类型，不能用来传递在泛型或于类别作为输入。Guava提供大量包装工具类来处理原始类型的对象。

以下是有用的原始处理工具的列表：

- **`Bytes`**  
  实用程序的原始字节。
- **`Shorts`**  
  实用的原始short。
- **`Ints`**  
  实用为基本整型。
- **`Longs`**  
  实用的原始长整型。
- **`Floats`**  
  实用为基本float。
- **`Doubles`**  
  实用为基本的double。
- **`Chars`**  
  实用的原始字符。
- **`Booleans`**  
  实用为基本布尔。

### Guava 数学工具

- **`IntMath`**  
  数学工具为int类型。

- **`LongMath`**  
  数学工具为long类型。

- **`BigIntegerMath`**  
  数学实用程序处理BigInteger。

### Guava 其他类库

#### Optional

Optional用于包含非空对象的不可变对象。 Optional对象，用于不存在值表示null。这个类有各种实用的方法，以方便代码来处理为可用或不可用，而不是检查null值。

- **`static <T> Optional<T> absent()`**  
  返回没有包含的参考Optional的实例。
- **`abstract Set<T> asSet()`**  
  返回一个不可变的单集的唯一元素所包含的实例(如果存在);否则为一个空的不可变的集合。
- **`abstract boolean equals(Object object)`**  
  返回true如果对象是一个Optional实例，无论是包含引用彼此相等或两者都不存在。
- **`static <T> Optional<T> fromNullable(T nullableReference)`**  
  如果nullableReference非空，返回一个包含引用Optional实例;否则返回absent()。
- **`abstract T get()`**  
  返回所包含的实例，它必须存在。
- **`abstract int hashCode()`**  
  返回此实例的哈希码。
- **`abstract boolean isPresent()`**  
  返回true，如果这支架包含一个(非空)的实例。
- **`static <T> Optional<T> of(T reference)`**  
  返回包含给定的非空引用Optional实例。
- **`abstract Optional<T> or(Optional<? extends T> secondChoice)`**  
  返回此Optional，如果它有一个值存在; 否则返回secondChoice。
- **`abstract T or(Supplier<? extends T> supplier)`**  
  返回所包含的实例(如果存在); 否则supplier.get()。
- **`abstract T or(T defaultValue)`**  
  返回所包含的实例(如果存在);否则为默认值。
- **`abstract T orNull()`**  
  返回所包含的实例(如果存在);否则返回null。
- **`static <T> Iterable<T> presentInstances(Iterable<? extends Optional<? extends T>> optionals)`**  
  从提供的optionals返回每个实例的存在的值，从而跳过absent()。
- **`abstract String toString()`**  
  返回此实例的字符串表示。
- **`abstract <V> Optional<V> transform(Function<? super T,V> function)`**  
  如果实例存在，则它被转换给定的功能;否则absent()被返回。

示例代码：

```java
	public static void main(String args[]) {
		OptionalDemo guavaTester = new OptionalDemo();
		Integer value1 = null;
		Integer value2 = new Integer(10);
		Optional<Integer> a = Optional.fromNullable(value1);
		Optional<Integer> b = Optional.of(value2);
		System.out.println(guavaTester.sum(a, b)); // 10
	}

	public Integer sum(Optional<Integer> a, Optional<Integer> b) {
		System.out.println("First parameter is present: " + a.isPresent()); // false
		System.out.println("Second parameter is present: " + b.isPresent()); // true
		Integer value1 = a.or(new Integer(0));
		Integer value2 = b.get();
		return value1 + value2;
	}
```

#### Preconditions

Preconditions提供静态方法来检查方法或构造函数，被调用是否给定适当的参数。它检查的先决条件。其方法失败抛出IllegalArgumentException。

- **`static void checkArgument(boolean expression)`**  
  确保涉及的一个或多个参数来调用方法表达式的真相。
- **`static void checkArgument(boolean expression, Object errorMessage)`**  
  确保涉及的一个或多个参数来调用方法表达式的真相。
- **`static void checkArgument(boolean expression, String errorMessageTemplate, Object... errorMessageArgs)`**  
  确保涉及的一个或多个参数来调用方法表达式的真相。
- **`static int checkElementIndex(int index, int size)`**  
  确保索引指定一个数组，列表或尺寸大小的字符串有效的元素。
- **`static int checkElementIndex(int index, int size, String desc)`**  
  确保索引指定一个数组，列表或尺寸大小的字符串有效的元素。
- **`static <T> T checkNotNull(T reference)`**  
  确保对象引用作为参数传递给调用方法不为空。
- **`static <T> T checkNotNull(T reference, Object errorMessage)`**  
  确保对象引用作为参数传递给调用方法不为空。
- **`static <T> T checkNotNull(T reference, String errorMessageTemplate, Object... errorMessageArgs)`**  
  确保对象引用作为参数传递给调用方法不为空。
- **`static int checkPositionIndex(int index, int size)`**  
  确保索引指定一个数组，列表或尺寸大小的字符串的有效位置。
- **`static int checkPositionIndex(int index, int size, String desc)`**  
  确保索引指定一个数组，列表或尺寸大小的字符串的有效位置。
- **`static void checkPositionIndexes(int start, int end, int size)`**  
  确保开始和结束指定数组，列表或字符串大小有效的位置，并按照顺序。
- **`static void checkState(boolean expression)`**  
  确保涉及调用实例的状态，但不涉及任何参数来调用方法表达式的真相。
- **`static void checkState(boolean expression, Object errorMessage)`**  
  确保涉及调用实例的状态，但不涉及任何参数来调用方法表达式的真相。
- **`static void checkState(boolean expression, String errorMessageTemplate, Object... errorMessageArgs)`**  
  确保涉及调用实例的状态，但不涉及任何参数来调用方法表达式的真相。

示例代码：

```java
public static void main(String args[]) {
	PreconditionsDemo guavaTester = new PreconditionsDemo();
	try {
		System.out.println(guavaTester.sqrt(-3.0)); // Negative value -3.0.
	} catch (IllegalArgumentException e) {
		System.out.println(e.getMessage());
	}
	try {
		System.out.println(guavaTester.sum(null, 3));
	} catch (NullPointerException e) {
		System.out.println(e.getMessage()); // First parameter is Null.
	}
	try {
		System.out.println(guavaTester.getValue(6)); 
	} catch (IndexOutOfBoundsException e) {
		System.out.println(e.getMessage()); // Invalid index. (6) must be less than size (5)
	}
}

public double sqrt(double input) throws IllegalArgumentException {
	Preconditions.checkArgument(input > 0.0, "Negative value %s.", input);
	return Math.sqrt(input);
}

public int sum(Integer a, Integer b) {
	a = Preconditions.checkNotNull(a, "First parameter is Null.");
	b = Preconditions.checkNotNull(b, "Second parameter is Null.");
	return a + b;
}

public int getValue(int input) {
	int[] data = { 1, 2, 3, 4, 5 };
	Preconditions.checkElementIndex(input, data.length, "Invalid index.");
	return 0;
}
```

#### Ordering

Ordering(排序)可以被看作是一个丰富的比较具有增强功能的链接，多个实用方法，多类型排序功能等。

- **`static Ordering<Object> allEqual()`**  
  返回一个排序，它把所有的值相等，说明“没有顺序。”通过这个顺序以任何稳定的排序算法的结果，在改变没有顺序元素。
- **`static Ordering<Object> arbitrary()`**  
  返回一个任意顺序对所有对象，其中compare(a, b) == 0 意味着a == b（身份平等）。
- **`int binarySearch(List<? extends T> sortedList, T key)`**  
  搜索排序列表使用键的二进制搜索算法。
- **`abstract int compare(T left, T right)`**  
  比较两个参数的顺序。
- **`<U extends T> Ordering<U> compound(Comparator<? super U> secondaryComparator)`**  
  返回首先使用排序这一点，但它排序中的“tie”，然后委托给secondaryComparator事件。
- **`static <T> Ordering<T> compound(Iterable<? extends Comparator<? super T>> comparators)`**  
  返回一个排序它尝试每个给定的比较器，以便直到一个非零结果找到，返回该结果，并返回零仅当所有比较器返回零。
- **`static <T> Ordering<T> explicit(List<T> valuesInOrder)`**  
  返回根据它们出现的定列表中的顺序比较对象进行排序。
- **`static <T> Ordering<T> explicit(T leastValue, T... remainingValuesInOrder)`**  
  返回根据它们所赋予本方法的顺序进行比较的对象进行排序。
- **`static <T> Ordering<T> from(Comparator<T> comparator)`**  
  返回基于现有的比较实例进行排序。
- **`<E extends T> List<E> greatestOf(Iterable<E> iterable, int k)`**  
  返回根据这个顺序给出迭代，为了从最大到最小的k个最大的元素。
- **`<E extends T> List<E> greatestOf(Iterator<E> iterator, int k)`**  
  返回从给定的迭代器按照这个顺序，从最大到最小k个最大的元素。
- **`<E extends T> ImmutableList<E> immutableSortedCopy(Iterable<E> elements)`**  
  返回包含的元素排序这种排序的不可变列表。
- **`boolean isOrdered(Iterable<? extends T> iterable)`**  
  返回true如果在迭代后的第一个的每个元素是大于或等于在它之前，根据该排序的元素。
- **`boolean isStrictlyOrdered(Iterable<? extends T> iterable)`**  
  返回true如果在迭代后的第一个的每个元素是严格比在它之前，根据该排序的元素更大。
- **`<E extends T> List<E> leastOf(Iterable<E> iterable, int k)`**  
  返回根据这个顺序给出迭代，从而从低到最大的k个最低的元素。
- **`<E extends T> List<E> leastOf(Iterator<E> elements, int k)`**  
  返回第k从给定的迭代器，按照这个顺序从最低到最大至少元素。
- **`<S extends T> Ordering<Iterable<S>> lexicographical()`**  
  返回一个新的排序它通过比较对应元素两两直到非零结果发现排序迭代;规定“字典顺序”。
- **`<E extends T> E max(E a, E b)`**  
  返回两个值按照这个顺序的较大值。
- **`<E extends T> E max(E a, E b, E c, E... rest)`**  
  返回指定的值，根据这个顺序是最大的。
- **`<E extends T> E max(Iterable<E> iterable)`**  
  返回指定的值，根据这个顺序是最大的。
- **`<E extends T> E max(Iterator<E> iterator)`**  
  返回指定的值，根据这个顺序是最大的。
- **`<E extends T> E min(E a, E b)`**  
  返回两个值按照这个顺序的较小者。
- **`<E extends T> E min(E a, E b, E c, E... rest)`**  
  返回最少指定的值，根据这个顺序。
- **`<E extends T> E min(Iterable<E> iterable)`**  
  返回最少指定的值，根据这个顺序。
- **`<E extends T> E min(Iterator<E> iterator)`**  
  返回最少指定的值，根据这个顺序。
- **`static <C extends Comparable> Ordering<C> natural()`**  
  返回使用值的自然顺序排序序列化。
- **`<S extends T> Ordering<S> nullsFirst()`**  
  返回对待null小于所有其他值，并使用此来比较非空值排序。
- **`<S extends T> Ordering<S> nullsLast()`**  
  返回对待null作为大于所有其他值，并使用这个顺序来比较非空值排序。
- **`<F> Ordering<F> onResultOf(Function<F,? extends T> function)`**  
  返回一个新的排序在F上，首先应用功能给它们，然后比较使用此这些结果的顺序元素。
- **`<S extends T> Ordering<S> reverse()`**  
  返回相反顺序; 顺序相当于Collections.reverseOrder（Comparator）。
- **`<E extends T> List<E> sortedCopy(Iterable<E> elements)`**  
  返回包含的元素排序此排序可变列表;使用这个只有在结果列表可能需要进一步修改，或可能包含null。
- **`static Ordering<Object> usingToString()`**  
  返回由它们的字符串表示的自然顺序，toString()比较对象进行排序。

示例代码：

```java
List<Integer> numbers = new ArrayList<Integer>();
numbers.add(new Integer(5));
numbers.add(new Integer(2));
numbers.add(new Integer(15));
numbers.add(new Integer(51));
numbers.add(new Integer(53));
numbers.add(new Integer(35));
numbers.add(new Integer(45));
numbers.add(new Integer(32));
numbers.add(new Integer(43));
numbers.add(new Integer(16));

System.out.println(numbers); // [5, 2, 15, 51, 53, 35, 45, 32, 43, 16]

Ordering<Integer> ordering = Ordering.natural();
Collections.sort(numbers, ordering);
System.out.println(numbers); // [2, 5, 15, 16, 32, 35, 43, 45, 51, 53]

System.out.println(ordering.isOrdered(numbers)); // true
System.out.println("Minimum: " + ordering.min(numbers)); // 2
System.out.println("Maximum: " + ordering.max(numbers)); // 53

Collections.sort(numbers, ordering.reverse()); // 倒序
System.out.println(numbers); // [53, 51, 45, 43, 35, 32, 16, 15, 5, 2]

numbers.add(null);
System.out.println(numbers); // [53, 51, 45, 43, 35, 32, 16, 15, 5, 2, null]

Collections.sort(numbers, ordering.nullsFirst());
System.out.println(numbers); // [null, 2, 5, 15, 16, 32, 35, 43, 45, 51, 53]

List<String> names = new ArrayList<String>();
names.add("Ram");
names.add("Shyam");
names.add("Mohan");
names.add("Sohan");
names.add("Ramesh");
names.add("Suresh");
names.add("Naresh");
names.add("Mahesh");
names.add(null);
names.add("Vikas");
names.add("Deepak");

System.out.println("Another List: ");
System.out.println(names); // [Ram, Shyam, Mohan, Sohan, Ramesh, Suresh, Naresh, Mahesh, null, Vikas, Deepak]

Ordering<String> ordering2 = Ordering.natural();
Collections.sort(names, ordering2.nullsFirst().reverse());
System.out.println("Null first then reverse sorted list: ");
System.out.println(names); // [Vikas, Suresh, Sohan, Shyam, Ramesh, Ram, Naresh, Mohan, Mahesh, Deepak, null]
```

#### Range

Range 表示一个间隔或一个序列。它被用于获取一组数字/串在一个特定范围之内。

- **`static <C extends Comparable<?>> Range<C> all()`**  
  返回包含C型的每一个值范围
- **`boolean apply(C input)Deprecated.`**  
  只有提供满足谓词接口;使用包含(C)来代替。
- **`static <C extends Comparable<?>> Range<C> atLeast(C endpoint)`**  
  返回包含大于或等于终点(endpoint)的所有值的范围内。
- **`static <C extends Comparable<?>> Range<C> atMost(C endpoint)`**  
  返回包含的所有值小于或等于终点的范围内。
- **`Range<C> canonical(DiscreteDomain<C> domain)`**  
  返回此范围内，在给定域中的规范形式。
- **`static <C extends Comparable<?>> Range<C> closed(C lower, C upper)`**  
  返回包含大于所有值或等于降低且小于或等于上限的范围内。
- **`static <C extends Comparable<?>> Range<C> closedOpen(C lower, C upper)`**  
  返回包含大于或等于下限和所有值严格大于上限以下的范围内。
- **`boolean contains(C value)`**  
  返回true，如果值是这个范围的范围之内。
- **`boolean containsAll(Iterable<? extends C> values)`**  
  如果值每一个元素都包含在这个范围内，则返回 true。
- **`static <C extends Comparable<?>> Range<C> downTo(C endpoint, BoundType boundType)`**  
  返回的范围内的给定的端点，它可以是包容性（闭合）或专用（开），没有上限。
- **`static <C extends Comparable<?>> Range<C> encloseAll(Iterable<C> values)`**  
  返回包含所有给定值的最小范围内。
- **`boolean encloses(Range<C> other)`**  
  返回true，如果其他的边界不在该范围的边界之外延伸。
- **`boolean equals(Object object)`**  
  返回true，如果对象是具有相同端点和绑定类型，这个范围内的范围。
- **`static <C extends Comparable<?>> Range<C> greaterThan(C endpoint)`**  
  返回一个包含所有值严格大于端点的范围内。
- **`int hashCode()`**  
  返回此范围内的哈希码。
- **`boolean hasLowerBound()`**  
  如果此范围内具有更低的终点返回true。
- **`boolean hasUpperBound()`**  
  如果此范围内有上端点返回true。
- **`Range<C> intersection(Range<C> connectedRange)`**  
  返回由两者范围和connectedRange封闭，如果这样的范围存在的最大范围。
- **`boolean isConnected(Range<C> other)`**  
  如果存在这是由两者此范围和其他封闭（可能为空）的范围，则返回true。
- **`boolean isEmpty()`**  
  返回true，如果这个范围是形式 [v..v)  或 (v..v].
- **`static <C extends Comparable<?>> Range<C> lessThan(C endpoint)`**  
  返回一个包含所有值严格小于端点的范围内。
- **`BoundType lowerBoundType()`**  
  返回类型这个范围的下限：如果范围包括它的下端点BoundType.CLOSED，如果没有BoundType.OPEN。
- **`C lowerEndpoint()`**  
  返回该范围的较低端点。
- **`static <C extends Comparable<?>> Range<C> open(C lower, C upper)`**  
  返回一个包含所有值严格大于下限和严格比上端更小一个范围。
- **`static <C extends Comparable<?>> Range<C> openClosed(C lower, C upper)`**  
  返回包含所有值严格低于更大且小于或等于上限的范围内。
- **`static <C extends Comparable<?>> Range<C> range(C lower, BoundType lowerType, C upper, BoundType upperType)`**  
  返回包含任何值由下到上，每个端点可以是包容性（关闭）或专用（开）的范围。
- **`static <C extends Comparable<?>> Range<C> singleton(C value)`**  
  返回包含只在给定范围内的值。
- **`Range<C> span(Range<C> other)`**  
  返回最小的范围包围两者这个范围和other等。
- **`String toString()`**  
  返回该范围内的字符串表示，如“[3..5）”（其他实例列在类文档）。
- **`BoundType upperBoundType()`**  
  返回类型此范围的上限：如果范围包括其上的端点返回BoundType.CLOSED，如果没有返回BoundType.OPEN。
- **`C upperEndpoint()`**  
  返回此范围的上限端点。
- **`static <C extends Comparable<?>> Range<C> upTo(C endpoint, BoundType boundType)`**  
  返回一个范围，没有下限到给定的端点，它可以是包容性（闭合）或专用（开）。

示例代码：

```java
// 创建一个序列 [a,b] = { x | a <= x <= b}
Range<Integer> range1 = Range.closed(0, 9); // 0 1 2 3 4 5 6 7 8 9

// 创建一个序列 (a,b) = { x | a < x < b}
Range<Integer> range2 = Range.open(0, 9); // 1 2 3 4 5 6 7 8

// 创建一个序列 (a,b] = { x | a < x <= b}
Range<Integer> range3 = Range.openClosed(0, 9); // 1 2 3 4 5 6 7 8 9

// 创建一个序列 [a,b) = { x | a <= x < b}
Range<Integer> range4 = Range.closedOpen(0, 9); // 0 1 2 3 4 5 6 7 8
```



### 参考链接

- https://www.yiibai.com/guava