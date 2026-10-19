---
title: "The Most Used Stream Operations in Java With Examples"
date: 2023-08-12
description: "Stream operations were introduced in Java 8 and they allow you to manipulate collections of data in a concise and functional way. A stream can be seen..."
categories: [Java]
tags: [java, streams]
draft: false
---

Stream operations were introduced in Java 8 and they allow you to manipulate collections of data in a concise and functional way. A stream can be seen as a sequence of elements that you can perform various operations on, such as filtering, mapping, or reducing.  

This article serves as a comprehensive guide to the most commonly used stream operations, with clear explanations and practical examples.

## Setting up and Creating Streams

To work with stream operations, you need to create a stream first. Streams can be created from various data sources, including collections, arrays, or input/output channels. For example, to create a stream from a list, you can use the `stream()` method:

```java
List<Integer> numbers = List.of(1, 2, 3, 4, 5);
Stream<Integer> stream = numbers.stream();
```

Once you have a stream, you can start applying different operations to transform or process the elements.

## Filtering Elements in Streams

#### Filtering with a predicate

Filtering is a common operation in stream processing, and it allows you to select only the elements that meet a given condition. One way to filter elements is by using a `Predicate` - a functional interface that represents a condition. You can use the `filter()` method to apply the predicate and keep only the elements that satisfy it.

```java
List<Integer> numbers = List.of(1, 2, 3, 4, 5);
Stream<Integer> stream = numbers.stream()
    .filter(num -> num % 2 == 0);
```

In this example, the resulting stream will only contain the even numbers (2 and 4).

#### Filtering with distinct()

The `distinct()` operation removes duplicate elements from a stream, based on their `equals()` method. 

This can be useful when you want to eliminate duplicate values and work only with unique elements.

```java
List<Integer> numbers = List.of(1, 2, 2, 3, 4, 4, 5);
Stream<Integer> stream = numbers.stream()
    .distinct();
```

The resulting stream will contain the distinct numbers [1, 2, 3, 4, , 5], removing any duplicates.

#### Filtering with limit()

The `limit()` operation allows you to limit the size of a stream to a specified number of elements. This can be handy when you only need a portion of the stream or want to reduce the amount of data processed.

```java
List<Integer> numbers = List.of(1, 2, 3, 4, 5);
Stream<Integer> stream = numbers.stream()
    .limit(3);
```

In this case, the resulting stream will contain the first three numbers [1, 2, 3], discarding the rest.

## Mapping Elements in Streams

#### Mapping with map()

Mapping is an operation that transforms each element in a stream into another object based on a function. You can use the `map()` operation to apply a function to each element and obtain a new stream of the transformed elements.

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
Stream<String> stream = numbers.stream()
    .map(num -> "Number " + num);
```

In this example, the resulting stream will contain the strings "Number 1", "Number 2", "Number 3", "Number 4", and "Number 5".

#### Mapping with flatMap()

The `flatMap()` operation is similar to `map()`, but it allows you to transform each element into a stream and then flatten the resulting streams into a single stream. This is useful when working with nested collections or when you want to merge multiple streams together.

```java
List<List<Integer>> numbers = Arrays.asList(
        Arrays.asList(1, 2, 3),
        Arrays.asList(4, 5)
);
Stream<Integer> stream = numbers.stream()
    .flatMap(List::stream);
```

In this case, the resulting stream will contain all the individual numbers from the nested lists [1, 2, 3, 4, 5].

## Reducing and Aggregating Stream Elements

#### Reducing with reduce()

The `reduce()` operation combines all the elements in a stream into a single result. It takes an initial value and an associative binary operator and repeatedly applies the operator to the accumulated result and each element of the stream.

```java
List <Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
Optional<Integer> result = numbers.stream().reduce(Integer::sum);
```

In this example, the result will be an `Optional` holding the sum of all the numbers (15).

#### Aggregating with collect()

The `collect()` operation allows you to accumulate elements from a stream into a mutable result container, such as a `List`, `Set`, or `Map`. It takes a `Collector` as a parameter, which defines how the elements should be collected.

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
List<Integer> squaredNumbers = numbers.stream()
        .map(num -> num * num)
        .collect(Collectors.toList());
```

In this case, the `collect()` operation collects the squared numbers into a new `List`, resulting in [1, 4, 9, 16, 25].

## Sorting and Ordering Stream Elements

#### Sorting with sorted()

The `sorted()` operation allows you to sort the elements of a stream in natural order. For example, let's say you have a stream of integers and you want to sort them in ascending order. You can simply call the `sorted()` operation on the stream and voila! Your stream is now sorted.

Here's an example:

```java
List<Integer> numbers = Arrays.asList(5, 2, 8, 1, 9);
List<Integer> sortedNumbers = numbers.stream()
        .sorted()
        .toList();

System.out.println(sortedNumbers); 
```

The output of the code execution will be the following:

```less
[1, 2, 5, 8, 9]
```

#### Custom Sorting with Comparator

What if you want to sort elements in a non-natural order? Fear not! You can use the `sorted()` operation with a custom `Comparator`. This gives you the flexibility to define your own sorting logic.

For example, let's say you want to sort a list of words by their length in descending order. You can do that by providing a `Comparator` to the `sorted()` operation.

Here's how it looks:

```java
List<String> words = Arrays.asList("apple", "banana", "date", "cherry");
List<String> sortedWords = words.stream()
        .sorted(Comparator.comparingInt(String::length))
        .collect(Collectors.toList());

System.out.println(sortedWords);
```

The output of the code execution will be the following:

```less
[date, apple, cherry, banana]
```

#### Reversing the Order with reverse()

Sometimes, you may want to reverse the order of elements in a stream. Java provides the `reverse()` operation for that

Here's an example:

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
List<Integer> reversedNumbers = numbers.stream()
.sorted(Comparator.reverseOrder())
.collect(Collectors.toList());

System.out.println(reversedNumbers);
```

The output of the code execution will be the following:

```less
[5, 4, 3, 2, 1]
```

## Combining and Concatenating Streams

On occasion, you might encounter a scenario where you need to merge various streams together. Java provides a couple of stream operations designed to effortlessly facilitate this task.

#### Merging Streams with concat()

The `concat()` operation permits the merging of two streams into a unified stream.

Here's an example:

```java
Stream<Integer> stream1 = Stream.of(1, 2, 3);
Stream<Integer> stream2 = Stream.of(4, 5, 6);
Stream<Integer> mergedStream = Stream.concat(stream1, stream2);

mergedStream.forEach(System.out::println);
```

The output of the code execution will be the following:

```less
1
2
3
4
5
6
```

### Flattening Streams with flatMap()

The `flatMap()` Operation transforms a stream of elements that contain nested structures, such as collections or arrays, into a single-level stream. This operation essentially extracts the elements from the nested structures and merges them into one continuous stream.

Here's an example:

```java
List<List<Integer>> listOfLists = Arrays.asList(
Arrays.asList(1, 2, 3),
Arrays.asList(4, 5, 6),
Arrays.asList(7, 8, 9)
);

List<Integer> flattenedList = listOfLists.stream()
.flatMap(List::stream)
.collect(Collectors.toList());

System.out.println(flattenedList); 
```

The output of the code execution will be the following:

```less
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## Stream Pipelines and Chaining Operations

Stream pipelines allow you to chain multiple stream operations together, creating a sequence of transformations on your data. This can lead to more concise and readable code.

Let's first start by defining a class called `Person`

```java
public class Person {
    private String name;
    private int age;

    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public int getAge() {
        return age;
    }
}
```

And here's how the stream pipeline with chaining operations would look:

```java
List<Person> people = List.of(
    new Person("Alice", 25),
    new Person("Bob", 30),
    new Person("Charlie", 22),
    new Person("David", 28),
    new Person("Emma", 35)
);

List<String> result = people.stream()
    .filter(person -> person.getAge() < 30)
    .sorted((p1, p2) -> p1.getName().compareTo(p2.getName()))
    .map(person -> person.getName().toUpperCase())
    .collect(Collectors.toList());

System.out.println("Filtered, sorted, and uppercase names: " + result);
```

In this example:

1. We create a list of `Person` objects.
2. We start a stream pipeline with `people.stream()`.
3. We filter out people with an age greater than or equal to 30.
4. We sort the remaining people by their names in ascending order.
5. We use the `map` operation to transform each person's name to uppercase.
6. We collect the final results into a new list using `collect(Collectors.toList())`.

The output of the code execution will be the following:

```less
Filtered, sorted, and uppercase names: [ALICE, CHARLIE, DAVID]
```
