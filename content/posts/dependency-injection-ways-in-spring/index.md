---
title: "Comparison between the different ways of dependency injection in Spring"
date: 2021-03-05
description: "Dependency injection is a core feature of the Spring framework. It is used by Spring to set the bean’s dependencies while initializing the application..."
categories: [Spring Boot]
tags: [spring, dependency-injection, java]
draft: false
---

![Photo by Fazly Shah on Unsplash](image-1.jpg)

*Photo by [Fazly Shah](https://unsplash.com/@fazlyshah?utm_source=medium&utm_medium=referral) on [Unsplash](https://unsplash.com?utm_source=medium&utm_medium=referral)*

Dependency injection is a core feature of the Spring framework. It is used by Spring to set the bean’s dependencies while initializing the application context. We usually use `@Autowired` annotation to get a reference to a bean in the Spring context.

Dependency injection in Spring can be done in three different ways: fields, setter, and constructor. In this article, we will explain each one and give their pros and cons.

## Field-based dependency injection

It consists of annotating with `@Autowired` the field you want to assign a reference from the Spring context. The next code snippet is an example of field dependency injection:

We use field injection for its simplicity: There is less boilerplate code for getters, setters, or constructors for the class. However, field-based dependency injection presents some drawbacks:

- You can not create immutable objects since the fields can not be final.
- It is hard to test classes using the field dependency injection when we do not use a mocking library like Mockito: Classes can not be instantiated without reflection and the use of a dependency injection container to instantiate them.
- It hides the dependencies to the outside world: Usually a class exposes its dependencies using the constructor or the setter methods for the optional ones. With field injection, the dependencies are hidden.
- Can lead to the violation of the Single Responsibility Principle since it is easy to have many dependencies without being aware that the class is doing many things.

## Setter-based dependency injection

It consists of annotating the field’s setter with `@Autowired` and Spring will call that setter method when setting the bean reference. The next code snippet is an example of setter dependency injection:

It means that Spring injects the value to the input of the setter method, which will be assigned after to the attribute. One use-case of this method is to add some logic while setting the value of the attribute (smart setter) but it is not recommended. It is also used to initialize optional attributes that were not set when calling the constructor. The class should be able to function when these dependencies are not provided. Setter injection allows reconfiguring the objects or re-injecting dependencies later. When the immutability of the class is not required, setter dependency injection can be an option.

## Constructor-based dependency injection

It consists of annotating the constructor of the class with `@Autowired` and Spring will set the bean's references to the constructor's parameters when calling it. The next code snippet is an example of constructor dependency injection:

The Spring team encourages the use of the constructor injection since it presents many benefits over the other types of dependency injection:

- The fields injected are declared as final hence, you create immutable objects and can be sure that the object created can be used the moment it is instantiated.
- The components created with constructor DI are returned to the clients in a fully initialized state: there will no need for not-null checks in the client’s code.
- A large number of constructor arguments can be detected as a code smell. It implies that the class may have many responsibilities: A refactoring may be required at that time to address proper separation of concerns.
- We can decouple the class from the dependency injection framework since Spring supports the implicit constructor injection: You no longer need to annotate the constructor with dependency injection annotations.
- No need to have a mocking library to test the application: You can use the constructor to set the dependencies of your class. The example below illustrates that:

## Summary

In this article, we demonstrated how to inject dependencies using the `@Autowired` annotation in the Spring framework in different ways. Then, we presented the advantages and disadvantages of each method. We conclude that it is better to use the constructor dependency injection as it provides many advantages over the other ways.
