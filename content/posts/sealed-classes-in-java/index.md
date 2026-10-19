---
title: "Sealed Classes in Java"
date: 2023-08-07
description: "Sealed classes, a new addition to the Java programming language starting from Java 15, provide developers with a powerful tool for defining restricted..."
categories: [Java]
tags: [java, sealed-classes]
draft: false
---

Sealed classes, a new addition to the Java programming language starting from Java 15, provide developers with a powerful tool for defining restricted class hierarchies. By explicitly specifying which classes can extend or implement them, sealed classes offer enhanced control over inheritance and extensibility.

This article explores the concept of sealed classes in Java, their syntax and declaration, as well as their purpose, benefits, and limitations.

## What are Sealed Classes?

Sealed classes in Java are a new feature introduced in Java 15 that allows developers to restrict the inheritance hierarchy of a class. By marking a class as sealed, you can control which other classes can extend it. This adds an extra layer of control and encapsulation to your code.

Sealed classes have evolved from sealed interfaces, which were introduced in Java 15 as well. Sealed interfaces restrict the implementation to a limited set of classes. With the introduction of sealed classes, the same concept of restriction has been extended to class inheritance, providing a more comprehensive way of managing the hierarchy of classes.

## Syntax and Declaration of Sealed Classes

### Declaring a Sealed Class

To declare a sealed class, you use the `sealed` keyword before the class declaration. For example:

```java
public sealed class Animal { }
```

This declares an `Animal` class as sealed, indicating that only specific classes can extend it.

### Declaring a Sealed Interface

To declare a sealed interface, you use the `sealed` keyword before the interface declaration. For example:

```java
public sealed interface Animal { }
```

This declares an `Animal` interface as sealed, indicating that only specific classes can implement it.

## Purpose and Benefits of Sealed Classes

### Ensuring Extensibility with Sealed Classes

Sealed classes provide a way to control the extensibility of your code. By explicitly specifying which classes can extend a sealed class, you prevent unauthorized or unintended inheritance, ensuring that your code remains robust and maintainable.

### Enforcing Stronger Encapsulation

With sealed classes, you can encapsulate the implementation details of your classes more effectively. By restricting the inheritance hierarchy, you prevent external classes from accessing or modifying the internal state, enhancing the security and integrity of your code.

## Exploring the Limitations and Constraints of Sealed Classes

### Restrictions on Inheritance

Sealed classes impose certain restrictions on inheritance. Only classes declared in the same module as the sealed class can extend it. This limitation ensures that the restricted hierarchy remains within the boundaries of a module, preventing unauthorized extensions from external modules.

### Impact on Subclassing and Extensibility

The use of sealed classes can potentially limit subclassing and extensibility. While it promotes more controlled and maintainable code, it might require additional effort and planning when introducing new subclasses. Developers need to be mindful of the sealed class hierarchy and plan the inheritance structure accordingly.

## Implementing Sealed Classes in Java

### Creating a Sealed Class Hierarchy

Creating a sealed class hierarchy in Java allows you to define a set of classes that can be inherited from, but only within a specific package or module. This helps enforce encapsulation and maintain control over class inheritance.

To create a sealed interface, you simply use the `sealed` keyword before the class definition. Then, you specify the classes that are allowed to implement it using the `permits` keyword. For example:

```java
package com.example;
    
sealed interface Animal permits Dog, Cat, Bird {}

final class Dog implements Animal {/*Class implementation*/}
final class Cat implements Animal {/*Class implementation*/}
final class Bird implements Animal {/*Class implementation*/}
```

In this example, the `Animal` interface is sealed and permits only the `Dog`, `Cat`, and `Bird` classes to implement it within the `com.example` package.

By using sealed classes, you can control the inheritance hierarchy and prevent other classes from extending the sealed class without explicit permission.

We can notice that all the classes implementing the sealed interface are marked as `final` to maintain control over the class inheritance since a final class can not be extended. However, if we remove the final keyword, we get this error from the compiler:

```
sealed, non-sealed or final modifiers expected
```

So, a class extending a sealed class or interface should be `sealed`, `non-sealed`, or `final`.

We can choose the `non-sealed` if we want the class to be inherited. For example, if we want to extend the `Bird` class with no control over the classes that can extend it then the code above should be changed  regarding the `Bird` class definition and it should be like this:

```java
non-sealed class Bird implements Animal {/*Class implementation*/}
```

It's possible now to extend the Bird class with new types. For example:

```java
final class Pigeon extends Bird {/*Class implementation*/}
final class Parrot extends Bird {/*Class implementation*/}
```

### Implementing Pattern Matching with Sealed Classes

Pattern matching is a powerful feature introduced in Java 14 that allows you to concisely and safely extract components from sealed classes. It simplifies code that would otherwise involve verbose `instanceof` checks and casting.

To demonstrate pattern matching with sealed classes, let's consider the following example:

```java
public String getSound(Animal animal) {
    return switch(animal) {
        case Dog dog -> dog.bark();
        case Cat cat -> cat.meow();
        case Bird bird -> bird.chirp();
    };
}
```

In this example, the `getSound` method takes an `Animal` object and uses pattern matching to determine the specific subclass. Depending on the subclass, the appropriate sound method is called.

The compiler recognizes that the object `animal` can only be an instance of `Dog`, `Cat`, or `Bird`; thus, the switch statement is complete and does not require a `default` case.

Another advantage is that the compiler will point out the missing `switch` case if the class hierarchy is extended later.

Let's extend our class hierarchy with the Animal `Cow`

```java
sealed interface Animal permits Dog, Cat, Bird, Cow {}

final class Dog extends Animal {}
final class Cat extends Animal {}
final class Bird extends Animal {}
final class Cow extends Animal {}
```

When trying to recompile, we get the following error message:

```
the switch statement does not cover all possible input values
```

By utilizing sealed class hierarchies, the compiler can assist us in preventing errors that often arise when extending class hierarchies due to incomplete switch statements or expressions.

## Backward compatibility

With the introduction of new keywords such as `sealed`, `non-sealed`, and `permits`, JDK developers were left wondering what should be done with existing code that uses these same keywords as method or variable names.

For this reason, they decided to use the **contextual keywords**. The contextual keywords allow developers to introduce new features and functionalities without breaking existing code. By restricting the usage of certain keywords to specific contexts, Java ensures that older code bases can continue to function as intended.

Hence, the new keywords  `sealed`, `non-sealed`, and `permits` are contextual keywords and they have meaning only in the context of a class definition. If they are used as a method name or a variable name.

The following code is  a valid Java code:

```java
public String sealed() {
    var permits = "permits and sealed are allowed";
    return permits;
}
```

## Comparing Sealed Classes with Other Similar Concepts in Java

### Sealed Classes vs. Abstract Classes

Sealed classes and abstract classes serve different purposes. An abstract class cannot be directly instantiated and is designed to be extended by subclasses. On the other hand, a sealed class can be instantiated but has a defined set of permitted subclasses.

While abstract classes provide a way to implement shared behavior, sealed classes focus on controlling class inheritance within a specific package or module.

### Sealed Classes vs. Final Classes

Final classes and sealed classes also have distinct characteristics. A final class cannot be subclassed, making it the most restricted form of class inheritance. In contrast, a sealed class can be inherited from, but only by permitted subclasses.

Final classes ensure complete immutability and prevent any form of inheritance, while sealed classes allow limited inheritance while maintaining control over the subclass hierarchy.

## Conclusion

Sealed classes provide a powerful mechanism to control class inheritance in Java. By permitting only specific subclasses, they help maintain encapsulation and prevent unintended inheritance.

With the addition of pattern matching in Java 14, working with sealed classes becomes even more concise and readable. They find practical use in many scenarios, such as modeling different types of entities or managing class hierarchies.

As a developer, understanding sealed classes and incorporating them into your code base can lead to cleaner, more maintainable code. So go ahead, give sealed classes a try, and unlock the benefits they offer in Java development!
