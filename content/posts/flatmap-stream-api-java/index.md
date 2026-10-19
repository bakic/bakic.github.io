---
title: "A Deep Dive into the flatMap Operation of the Stream API in Java with Examples"
date: 2023-08-10
description: "The flatMap operation is an intermediate operation provided by the Stream API, which allows you to transform each element of a stream into zero or more..."
categories: [Java]
tags: [java, streams]
draft: false
---

The `flatMap` operation is an intermediate operation provided by the Stream API, which allows you to transform each element of a stream into zero or more elements and then flatten the resulting elements into a single stream. It's useful to use with nested data structures, such as lists within lists and effectively "flattening" them into a more manageable format.

In this article we are going to explain how this operation works internally and give some examples.

## How Does 'flatMap' Operation Work?

The `flatMap` operation has the following signature in the Stream API:

```java
<R> Stream<R> flatMap(Function<? super T, ? extends Stream<? extends R>> mapper);
```

Here's what the components of this signature mean:

- `T`: The type of elements in the original stream.
- `R`: The type of elements in the resulting stream after applying the mapping function.
- `mapper`: A function that takes an element of type `T` from the original stream and returns a stream of elements of type `R`. 

The function is applied to each element in the original stream, and the resulting streams are then flattened into a single stream of type `R`.

When I started using the `flatMap` operation, i though that it was first flattening all the lists and then applying the map function to all the elements from the result stream, but I was wrong! In fact it was the other way around.

An example can illustrate this very well and make it crystal clear in your mind.

Suppose you have a list of strings, and you want to split each string into words and then create a single stream of words.

```java
List<String> strings = List.of("Hello-World", "Java-Programming");

List<String> words = strings.stream()
    .flatMap(str -> Arrays.stream(str.split(" ")))
    .toList();

```

Here is what happens internally:

1. The mapping function (`str -> Arrays.stream(str.split("-"))`) is applied to each string in the input list. This function takes a string and splits it into an array of words using a hyphen as the delimiter.
2. For the first string "Hello World", the mapping function returns a `stream` containing two words: "Hello" and "World". For the second string "Java Programming", the mapping function returns a `stream` with two words: "Java" and "Programming".
3. The individual streams from each mapping function are then flattened into a single stream containing all the words. The order is maintained, so the resulting stream would be: "Hello", "World", "Java", "Programming".
4. This flattened stream of words is collected into a list using the `toList` operation.

## Examples Where flatMap is used

The `flatMap` operation can be used to perform a variety of transformations on a stream. Some common use cases include:

- #### Flattening Lists of Objects


Suppose you have a list of `Person` objects, and each person has a list of phone numbers.

```java
class Person {
    private String name;
    private List<String> phoneNumbers;
    
    // omitted code of constructor, getters, setters
}
```

You want to extract all the phone numbers from all the persons and create a flat list of phone numbers.

```java
List<Person> people = new ArrayList<>();
people.add(new Person("John", List.of("1234", "5678")));
people.add(new Person("Bob", List.of("91011")));
people.add(new Person("Charlie", List.of("121314", "151617", "181920")));

List<String> allPhoneNumbers = people.stream()
        .flatMap(person -> person.getPhoneNumbers().stream()) // Flattening phone numbers of each person
        .collect(Collectors.toList());

System.out.println(allPhoneNumbers);
```

In this example, the `flatMap` operation is used to extract the phone numbers of each person and then flatten them into a single stream of phone numbers. The output will be:

```
[1234, 5678, 91011, 121314, 151617, 181920]
```

- #### Parsing and Flattening Strings


Suppose you have a list of strings where each string represents a comma-separated list of numbers. You want to parse each string, split it into numbers, and then create a flat stream of those numbers.

```java
List<String> inputStrings = Arrays.asList("1,2,3", "4,5", "6,7,8");

List<Integer> allNumbers = inputStrings.stream()
        .flatMap(str -> Arrays.stream(str.split(",")) // Splitting each string into numbers
                .map(Integer::parseInt) // Converting each number from string to integer
        ) 
        .toList();

System.out.println(allNumbers);
```

In this example, the `flatMap` operation is used to first split each input string into an array of strings representing individual numbers. Then, using the `map` operation, each string is parsed into an integer. The result is a flat stream of integers:

```
[1, 2, 3, 4, 5, 6, 7, 8]
```

- #### Working with Optional Values


Suppose you have a list of `optional` values, and you want to extract the present values and create a flat stream of those values.

```java
List<Optional<Integer>> optionals = Arrays.asList(
        Optional.of(1), 
        Optional.empty(), 
        Optional.of(3), 
        Optional.empty(), 
        Optional.of(5)
);

List<Integer> presentValues = optionals.stream()
        .flatMap(Optional::stream) // Flattening optional values
        .collect(Collectors.toList());

System.out.println(presentValues);
```

In this example, the `flatMap` operation is used to extract the present values from the optional values and flatten them into a stream of integers:

```
[1, 3, 5]
```
