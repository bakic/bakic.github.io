---
title: "Difference between Map and FlatMap in Java"
date: 2021-02-18
description: "The Stream API of Java 8 provides two intermediate stream operations used to perform actions on stream elements and return a stream as an output: map..."
categories: [Java]
tags: [java, streams]
draft: false
---

![Photo by Clément Hélardot on Unsplash](image-1.jpg)

*Photo by [Clément Hélardot](https://unsplash.com/@clemhlrdt?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

The Stream API of Java 8 provides two intermediate stream operations used to perform actions on stream elements and return a stream as an output: `map` and `flatMap`. In this article, we are going to take a look at these two methods and explain the difference between them with examples.

## Map function

The `map` function takes a `Function` as a parameter and applies it to all the elements of the stream. The result will be a stream of the result of the function applied to each element of the initial stream. There is a **one-to-one** mapping between the input and the output elements.

Let’s take a look at how we can use `map`:

In this example, we have as input a list of strings in lowercase. The goal is to have the same list of words but in uppercase. To satisfy this requirement, `map` is the best choice: we will apply the function `toUppercase` of the `String` class to each element and collect the result in a list of `Strings`. The result will be ["ONE", "TWO", "THREE"].

## FlatMap function

In case we have a more complex type like `List<List<String>>` as input, using the `map` method is not going to work for us since there is a nested list: We need to flatten first. Here where comes `flatMap` in action.

In this example, we want to have a list of all the words of sentence1 and sentence2 in uppercase. To do that, the `flatMap` operation will:

- apply the `split` method on each sentence: produce an array of String. The result after this operation will be ["This", "is", "a"] and ["flatMap", "example"].
- flatten the resulting elements in a new stream: the output will be a stream of “This”, “is”, “a”,”flatMap”, “example”. Then we apply the `toUpperCase` operation on the elements of the stream. The`flatMap` operation applies a **one-to-many** transformation to the elements of the stream and then flattens the nested collections into a new stream.

## Summary

In this article, we presented two intermediate operations from the Stream API: `map`and `flatMap`, and we explained how each operation works with examples.
