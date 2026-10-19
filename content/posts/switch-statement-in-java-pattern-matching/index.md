---
title: "Switch Statement in Java: From Basic to Pattern Matching"
date: 2023-08-29
description: "The switch statement is a fundamental control structure in Java, allowing developers to execute different code blocks based on the value of an..."
categories: [Java]
tags: [java, pattern-matching]
draft: false
---

The switch statement is a fundamental control structure in Java, allowing developers to execute different code blocks based on the value of an expression. Before the introduction of advanced features like pattern matching and switch expressions, Java's switch statement underwent several stages of evolution. In this blog post, we'll take a journey through the evolution of the switch statement, exploring its various stages and providing detailed examples and explanations along the way.

### Stage 1: Basic Switch

The basic switch statement was introduced in the early versions of Java and allowed developers to compare a single value against multiple cases. Each case was a constant value, and the program would execute the block of code associated with the first matching case. Here's an example:

```java
public class BasicSwitchExample {
    public static void main(String[] args) {
        char grade = 'B';
        String result;

        switch (grade) {
            case 'A':
            case 'B':
                result = "Pass";
                break;
            case 'C':
                result = "Marginal pass";
                break;
            case 'D':
            case 'F':
                result = "Fail";
                break;
            default:
                result = "Invalid grade";

        System.out.println("Result: " + result);
    }
}
```

While the traditional switch statement offers a clear way to handle multiple cases, it comes with some limitations:

- **Constant Values**: The expression in the switch statement can only be of certain types, such as primitive types, `char`, `int`, `byte`, `short`, and enumerated types.
- **Exact Matches**: Cases only allow exact value matches. This means you cannot perform more complex checks or matching using patterns.
- **Fall-Through**: If you omit the `break` statement after a case, the code execution falls through to the next case, leading to unintended behavior if not managed carefully.

### Stage 2: Enhanced Switch (Java 12)

Java 12 introduced a major enhancement to the switch statement with the introduction of switch expressions as a **preview feature**. Unlike traditional switch statements, switch expressions allow the direct assignment of a value from a case block. This simplifies the code and eliminates the need for `break` statements.

```java
int day = 2;
String dayType = switch (day) {
    case 1, 2, 3, 4, 5 -> "Weekday";
    case 6, 7 -> "Weekend";
    default -> "Invalid day";
};
```

In this example, the `dayType` variable is assigned based on the matched case, and you don't need explicit `break` statements.

Furthermore, this enhancements simplifies the switch statement by separating multiple cases with commas and using arrow annotation to eliminate error prone break statements.

From the example above, we can see how it's clear and simple to read.

```java
case 1, 2, 3, 4, 5 -> "Weekday";
```

### Stage 3: Enhanced Switch (Java 13)

This version came with a small change in switch expressions, which consists on replacing the `break` keyword by `yield` keyword.

We should note that `yield` is a contextual keyword, this means that it is recognized as a keyword only in the context of a switch expression. So if `yield` is used elsewhere in the code, then no worry, there is no need to update your code.

In the following example, we can see how `yield` is used in a switch expression:

```java
int month = 5;
String season = switch (month) {
    case 12, 1, 2 -> {
        yield "Winter";
    }
    case 3, 4, 5 -> {
        yield "Spring";
    }
    case 6, 7, 8 -> {
        yield "Summer";
    }
    case 9, 10, 11 -> {
        yield "Autumn";
    }
    default -> {
        yield "Invalid month";
    }
};
```

Here, each case contains a block statement enclosed in curly braces, and the `yield` keyword is used to return values.

#### Using Enhanced Switch with Enums

Enhanced switch works well with enums, making your code more concise:

```java
enum Color {
    RED, GREEN, BLUE
}

Color selectedColor = Color.BLUE;
String colorDescription = switch (selectedColor) {
    case RED -> "Red color selected";
    case GREEN -> "Green color selected";
    case BLUE -> "Blue color selected";
};
```

In the above example, we can see that we omitted the `default` case. This is because the compiler recognizes that we covered all the possible cases when we used the `Color` enum. If we extend the Color enumeration by a new color, let's say ORANGE, the compiler will tell us that the switch expressions is incomplete and that we should handle the new case.

### Stage 4: Enhanced Switch (Java 14) - Release

In Java 14, no new enhancements were added to the switch expressions. All the new features discussed earlier were accepted by the Java community and the feature was released in production starting from Java 14.

### Stage 5: Pattern Matching (Java 16)

The next most significant evolution of the switch statement came with Java 16, introducing pattern matching. Pattern matching simplifies code by allowing complex patterns to be matched directly within the switch statement. This makes the code more readable and reduces redundancy.

#### Basic Pattern Matching

In pattern matching, you use patterns to match against expressions. The `case` labels include patterns instead of just simple values. Here's a basic example:

```java
public String getDayType(Day day) {
    return switch (day) {
        case MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY -> "Weekday";
        case SATURDAY, SUNDAY -> "Weekend";
    };
}
```

In this example, `Day` is an enum, and we're directly matching the enum values using patterns.

#### Destructuring Objects

Pattern matching allows you to destructure objects right in the switch statement. For instance, consider a simple `Point` class:

```java
class Point {
    int x, y;
    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }
}
```

You can destructure this class within the switch statement:

```java
public void processPoint(Point point) {
    switch (point) {
        case Point p when p.x == 0 && p.y == 0 -> System.out.println("Origin");
        case Point p when p.x == p.y -> System.out.println("On Diagonal");
        default -> System.out.println("Other Point");
    }
}
```

#### instanceof Checks

Instead of using `instanceof` checks, pattern matching can be used to directly check and cast object types:

```java
public String getType(Object obj) {
    return switch (obj) {
        case Integer i -> "Integer with value " + i;
        case String s -> "String with value " + s;
        default -> "Unknown Type";
    };
}
```

#### Combining Patterns

You can also combine patterns using logical operators like `&&` and `||`:

```java
public String processCombination(Object obj) {
    return switch (obj) {
        case Integer i && i > 0 -> "Positive Integer";
        case Integer i && i < 0 -> "Negative Integer";
        case String s && s.length() > 10 -> "Long String";
        default -> "Other";
    };
}
```

A few remarks can be said about the pattern matching

- **Retro compatibility**: Pattern matching is available starting from Java 16 so if you want to use the new features you have to modify your code.
- **Pattern Complexity**: While pattern matching is useful, using very complex patterns can lead to less readable code.
- **Type Compatibility**: Ensure that the patterns are compatible with the types being matched; otherwise, it will result in compilation errors.
- **Code Maintenance**: While pattern matching can simplify code, overusing it in situations where simpler code suffices might lead to reduced clarity.

### Conclusion

The evolution of the switch statement in Java showcases the language's commitment to improving readability and expressiveness while reducing code duplication. From the basic switch to the enhanced switch and finally to the powerful pattern matching, Java's switch statement has come a long way. As you embrace the new pattern matching feature, remember that it's not just a syntactic improvement but a tool that can lead to more efficient, cleaner, and maintainable code.
