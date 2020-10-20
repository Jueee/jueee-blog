---
title: Apache集合工具commons-collections4的使用
layout: info
commentable: true
date: 2020-10-20
mathjax: true
mermaid: true
tags: [Apache,Java,JavaJar]
categories: [Java,JavaJar]
description: 
---

### Jar引入

```xml
		<dependency>
			<groupId>org.apache.commons</groupId>
			<artifactId>commons-collections4</artifactId>
			<version>4.4</version>
		</dependency>
```

### Jar介绍

Commons Collections 增强了Java集合框架。 它提供了几个功能来简化收集处理。 它提供了许多新的接口，实现和实用程序。 

<!--more-->

Commons Collections的主要特点如下 -

- **Bag** - `Bag`接口简化了每个对象具有多个副本的集合。
- **BidiMap**- `BidiMap`接口提供双向映射，可用于使用键或键使用的值来查找值。
- **MapIterator** - `MapIterator`接口为映射提供了简单和易于迭代方法。
- **转换装饰器** - 转换装饰器(`Transforming Decorators`)可以在集合添加到集合时改变集合的每个对象。
- **复合集合** - 复合集合用于要求统一处理多个集合的情况。
- **有序映射** - 有序映射保留元素添加的顺序。
- **有序集** - 有序集保留元素添加的顺序。
- **参考映射** - 参考映射允许在密切控制下对键/值进行垃圾收集。
- **比较器实现** - 许多比较器实现都可用。
- **迭代器实现** - 许多迭代器实现都可用。
- **适配器类** - 适配器类可用于将数组和枚举转换为集合。
- **实用程序** - 实用程序可用于测试测试或创建集合的典型集合理论属性，如联合，交集。 支持关闭。

### 通用集合Bag

`Bag`接口定义了一个集合，它可以计算一个对象出现在集合中的次数。

```java
import org.apache.commons.collections4.Bag;
import org.apache.commons.collections4.bag.HashBag;

public class BagTester {
   public static void main(String[] args) {
      Bag<String> bag = new HashBag<>();

      bag.add("a" , 2);
      bag.add("b");
      bag.add("c");
      bag.add("c");
      bag.add("d",3);

      System.out.println(bag.getCount("d"));	// 3
      System.out.println(bag);	// [2:a,1:b,2:c,3:d]

      System.out.println(bag.uniqueSet());	// [a, b, c, d]

      bag.remove("d",2);
      System.out.println(bag);	// [2:a,1:b,2:c,1:d]
      System.out.println(bag.getCount("d"));	// 1
      System.out.println(bag);	// [2:a,1:b,2:c,1:d]
      System.out.println(bag.uniqueSet());	// [a, b, c, d]
   }
}
```

### 通用集合BidiMap

BidiMap 接口被添加到支持双向映射。 使用双向映射，可以使用值查找键，并且可以使用键轻松查找值。

```java
import org.apache.commons.collections4.BidiMap;
import org.apache.commons.collections4.bidimap.TreeBidiMap;

public class BidiMapTester {
   public static void main(String[] args) {
      BidiMap<String, String> bidi = new TreeBidiMap<>();

      bidi.put("One", "1");
      bidi.put("Two", "2");
      bidi.put("Three", "3");

      System.out.println(bidi.get("One")); // 1
      System.out.println(bidi.getKey("1")); // One
      System.out.println(bidi); // {One=1, Three=3, Two=2}

      bidi.removeValue("1"); 
      System.out.println(bidi); // {Three=3, Two=2}
      BidiMap<String, String> inversedMap = bidi.inverseBidiMap();  
      System.out.println(inversedMap); // {2=Two, 3=Three}
   }
}
```

### 通用集合MapIterator

JDK Map接口很难作为迭代在`EntrySet`或`KeySet`对象上迭代。 `MapIterator`提供了对`Map`的简单迭代。

```java
import org.apache.commons.collections4.IterableMap;
import org.apache.commons.collections4.MapIterator;
import org.apache.commons.collections4.map.HashedMap;

public class MapIteratorTester {
   public static void main(String[] args) {
      IterableMap<String, String> map = new HashedMap<>();

      map.put("1", "One");
      map.put("2", "Two");
      map.put("3", "Three");
      map.put("4", "Four");
      map.put("5", "Five");

      MapIterator<String, String> iterator = map.mapIterator();
      while (iterator.hasNext()) {
         Object key = iterator.next();
         Object value = iterator.getValue();

         System.out.println("key: " + key);
         System.out.println("Value: " + value);

         iterator.setValue(value + "_");
      }

      System.out.println(map);	// {3=Three_, 5=Five_, 2=Two_, 4=Four_, 1=One_}
   }
}
```

### 通用集合OrderedMap

`OrderedMap`是映射的新接口，用于保留添加元素的顺序。 `LinkedMap`和`ListOrderedMap`是两种可用的实现。 此接口支持`Map`的迭代器，并允许在Map中向前或向后两个方向进行迭代。

```java
import org.apache.commons.collections4.OrderedMap;
import org.apache.commons.collections4.map.LinkedMap;

public class OrderedMapTester {
	public static void main(String[] args) {
		OrderedMap<String, String> map = new LinkedMap<String, String>();
		map.put("One", "1");
		map.put("Two", "2");
		map.put("Three", "3");

		System.out.println(map.firstKey()); // One
		System.out.println(map.lastKey()); // Three
		
		System.out.println(map.nextKey("One")); // Two
		System.out.println(map.nextKey("Two")); // Three
		
		System.out.println(map.previousKey("One")); // null
		System.out.println(map.previousKey("Two")); // One
	}
}
```

### 集合工具类CollectionUtils

Apache Commons Collections库的`CollectionUtils`类提供各种实用方法，用于覆盖广泛用例的常见操作。 它有助于避免编写样板代码。 这个库在jdk 8之前是非常有用的，但现在Java 8的Stream API提供了类似的功能。

#### 检查是否为空元素

CollectionUtils的`addIgnoreNull()`方法可用于确保只有非空(`null`)值被添加到集合中。

**返回值**：如果集合已更改，则返回为`True`。

```java
List<String> list = new LinkedList<String>();

boolean result1 = CollectionUtils.addIgnoreNull(list, null);
System.out.println(result1); // false
boolean result2 = CollectionUtils.addIgnoreNull(list, "a");
System.out.println(result2); // true
System.out.println(list); // [a]
System.out.println(list.contains(null)); // false

list.add(null);
System.out.println(list); // [a, null]
System.out.println(list.contains(null)); // true
```

#### 合并两个排序列表

CollectionUtils的`collate()`方法可用于合并两个已排序的列表。

**返回值**：一个新的排序列表，其中包含集合`a`和`b`的元素。

```java
List<String> sortedList1 = Arrays.asList("A", "C", "E");
List<String> sortedList2 = Arrays.asList("B", "D", "F");
List<String> mergedList = CollectionUtils.collate(sortedList1, sortedList2);
System.out.println(mergedList); // [A, B, C, D, E, F]
```

#### 转换列表

`CollectionUtils`的`collect()`方法可用于将一种类型的对象列表转换为不同类型的对象列表。

**返回值**：转换结果(新列表)。

```java
List<String> stringList = Arrays.asList("1", "2", "3");

List<Integer> integerList = (List<Integer>) CollectionUtils.collect(stringList,
		new Transformer<String, Integer>() {
			@Override
			public Integer transform(String input) {
				return Integer.parseInt(input);
			}
		});

System.out.println(integerList); // [1, 2, 3]
```

#### 过滤列表

CollectionUtils的`filter()`方法可用于过滤列表以移除不满足由谓词传递提供的条件的对象。

**返回值**：如果通过此调用修改了集合，则返回`true`，否则返回`false`。

```java
List<Integer> integerList = new ArrayList<Integer>();
integerList.addAll(Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8));
System.out.println(integerList); // [1, 2, 3, 4, 5, 6, 7, 8]

CollectionUtils.filter(integerList, new Predicate<Integer>() {
	@Override
	public boolean evaluate(Integer input) {
		if (input.intValue() % 2 == 0) {
			return true;
		}
		return false;
	}
});

System.out.println(integerList); // [2, 4, 6, 8]
```

#### 检查非空列表

CollectionUtils的 `isNotEmpty()` 方法可用于检查列表是否为null而不用担心null列表。 因此，在检查列表大小之前，不需要将无效检查放在任何地方。

**返回值**：如果非空且非null，则返回为:true。

#### 检查空的列表

CollectionUtils的`isEmpty()`方法可用于检查列表是否为空。

**返回值**：如果为空或为`null`，则返回为`true`。

#### 检查子列表

CollectionUtils的isSubCollection()方法可用于检查集合是否包含给定集合。

**参数**

- `a` - 第一个(子)集合不能为空。
- `b` - 第二个(超集)集合不能为空。

当且仅当`a`是`b`的子集合时才为`true`。

#### 检查相交

CollectionUtils的`intersection()`方法可用于获取两个集合(交集)之间的公共对象部分。

**参数**

- `a` - 第一个(子)集合不能为`null`。
- `b` - 第二个(超集)集合不能为`null`。

**返回值**：两个集合的交集。

#### 求差集

CollectionUtils的`subtract()`方法可用于通过从其他集合中减去一个集合的对象来获取新集合。

**参数**

- `a` - 要从中减去的集合，不能为`null`。
- `b` - 要减去的集合，不能为`null`。

**返回值**：两个集合的差集(新集合)。

#### 求联合集

CollectionUtils的`union()`方法可用于获取两个集合的联合。

**参数**

- `a` - 第一个集合，不能为`null`。
- `b` - 第二个集合，不能为`null`。

**返回值**：两个集合的联合。

### 参考资料

- https://www.yiibai.com/commons_collections