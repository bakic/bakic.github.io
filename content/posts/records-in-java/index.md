---
title: "Records in Java"
date: 2021-10-02
description: "After being a preview feature in Java 14 and Java 15, Java records are now part of the Java language starting from Java 16. "
categories: [Java]
tags: [java, records]
draft: false
---

![Photo by AltumCode on Unsplash](image-1.jpg)

*Photo by [AltumCode](https://unsplash.com/@altumcode?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

After being a preview feature in Java 14 and Java 15, Java records are now part of the Java language starting from Java 16.

In this article, we are going to take a deep dive into Java records and look at what this feature provides and how can we use it.

## Records

As per the [JEP 395](https://openjdk.java.net/jeps/395), records are described as `classes that act as transparent carriers for immutable data`.

Before having records in Java, when we want to represent some data, we end up with a class like shown below:

Here we have a class with four attributes. To use it, we need much more code to work with it. For instance, we need to have a constructor, getters to get the values of the attributes. We also need `toString()`, `hashCode()` and `equals()` methods to have a complete implementation of this class.

This boilerplate code can be generated using an IDE, or by using some libraries like Lombok, but this comes with drawbacks.

What we needed is a mechanism in the Java language that can handle data-only classes without dealing with boilerplate code or external tools that can cause issues in our program.

To solve this problem, records come into play. A record class declaration consists of a name, a header, and a body. The header lists the fields of the record known as *components*.

The previous class implementation can be written this way using records:

In the example above, a record is described as follows:

- the name of the record is `User`,
- the header contains the components `String firstName,String lastName` ,
- the body is empty for the moment.

By using records, we get a class that has an implicit constructor accepting all the attributes of the record which is called a canonical constructor. We get also implementations of `toString()`, `hashCode()` and `equals()` methods based on the attributes of the class. In addition, we get an accessor method for every attribute.

We should notice that a record doesn’t implement setter methods for its attributes, which means that a record is *immutable*: once instantiated with certain values, the state of the record can not be changed.

## Restrictions on Records

In comparison to a normal class, some restrictions apply to records:

- **can not extend another class**: A record class declaration doesn’t have an `extends` clause. Unlike a normal class which can implicitly extend its superclass Object, a record can not inherit from another class even Its superclass `java.lang.Record`.
- **a final class**: A record is final and can not be abstract. This means that the state of a record can not be enhanced later by another class using inheritance.
- **immutable**: A record is the best way to use to carry data without being modified since all the attributes are final.
- **no instance fields**: Instance fields are not allowed in a record class. The state of the record is defined only by the attributes declared in the record header.

In our example, if we want to add an instance field called `password`, we will get a compilation error:

## Use Cases of a Record

A record can be used in many ways as an alternative to an ordinary class. In the following, we will see some examples of these use cases.

- **Temporary container of data**: A record can be created to store temporary data in a method for example. There is no need to create a dedicated class file for a record if we need it only to hold some data inside our method. We can call it a *local record class*.

In this example, we created a record to use it a data store of the purchases of each client. This record is local to this method and will not be used outside it.

- **Data Transfer Objects(DTOs)**: A record can be used to represent a DTO which is an object that does not have a behavior: it is only used to transfer data.
- **Key in a map**: A record can be useful if we want to use a key composed of many values in a `Map`. The `hashCode()` and `equals()`methods are implemented in a record by default.

## Records vs Java Beans

Many developers will be tempted to use a record when they want to implement a Java Bean. However, a record can not really play the role of a Java Bean for several reasons:

- Java Beans that represent entities are usually mutable objects, however records are immutable.
- The name of the field accessors doesn’t conform to the Java bean convention: it doesn’t start with `get`. In the previous example, if we want to get the value of the `firstName` from the record, the statement will be `user.firstName()` instead of `user.getFirstName()`
