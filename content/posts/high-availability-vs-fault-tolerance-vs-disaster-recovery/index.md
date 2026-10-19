---
title: "High availability VS Fault Tolerance VS Disaster Recovery"
date: 2023-03-20
description: "High availability, Fault Tolerance and Disaster Recovery are three concepts to understand for every Solution Architect. These concepts are  sometimes..."
categories: [Architecture]
tags: [aws, architecture, resilience]
draft: false
---

High availability, Fault Tolerance and Disaster Recovery are three concepts to understand for every Solution Architect. These concepts are  sometimes mixed and the difference between each one is not clear enough.

#### High Availability (HA)

First, let's try to give the definition of high availability. Wikipedia has a pretty good one:

> **High availability** (**HA**) is a characteristic of a system which aims to ensure an agreed level of operational performance, usually [uptime](https://en.wikipedia.org/wiki/Uptime), for a higher than normal period.

Many people have an assumption that making a system highly available means ensuring that the system never fails or that the user of the system never experiences any outages, and that's not true.

HA isn't aiming to stop failure and it definitely doesn't mean that customers won't experience outages.

A highly available system is one designed to be online and providing services as often as possible. It's a system designed so that when it fails its components can be replaced or fixed as quickly as possible, often using automation to bring systems back into service.

High availability is not about user experience. if a system fails and a component is replaced and that disrupts the service for a few seconds, that's OK: it's still highly available. It's about maximizing a system's online time and that's it.

System availability is generally expressed in the form of a percentage of uptime. So we might have 99.9% or three nines and this means that we can have 8.77 hours of downtime per year. Imagine only being able to take a system down for 8.77 hours a year, that's less than one hour per month;

It gets worse though, some systems need even higher levels of availability. we have 99.999% availability (five nines) and this only allows for 5.26 minutes per year downtime. that means for all outages during a year, you have 5.26 minutes. that includes identifying that there is an outage, identifying the cause, devising a solution and an outage in this context is defined as something  which impacts that server, so impacts your users 

High availability is about keeping a system operational. it'a bout fast or automatic recovery of issues. it's not about preventing user disruption. While that's a bonus, a highly available system can still have disruption to your user base when there is a failure.

Now, HA has costs required to implement it. It needs some design decisions to be made in advance: some times high availability needs redundant servers ready to switch customers over to in the event of a disaster to minimize downtime.

#### Fault Tolerance (FT)

When most people think of high availability, they are actually mixing it up with fault tolerance.

Fault tolerance in some ways is very similar to high availability, but it's much more.

Fault tolerance is defined as the property that enables a system to continue operating properly in the event of a the failure of some of its components

It means that if a system has faults then it should continue to operate properly event while those faults are present and being fixed. It means it has to continue operating through a failure without impacting customers.

Fault tolerance is what means to operate through failure. it can be expensive because it's much more complex to implement compared to HA.

HA can be accomplished by having a spare equipment, or stand by physical of virtual components.

As long as you automate things and have these spare components ready to go you can minimize outages. With Fault tolerance it's about more than that. You first need to minimize outages, which is the same as HA, but then you need also to design the system to be able to tolerate the failure, which means levels of redundancy and system components which can route traffic and sessions around any failed components

Fault tolerance is harder to design, harder to implement and cost much more.

Implementing fault tolerance hen you really needed high availability simply means you're waisting money: it costs more and takes longer to implement.

But the reverse, implementing high availability when you need fault tolerance means that you're potentially putting life at risk.



#### Disaster Recovery (DR)

Disaster recovery is a set of policies, tools and procedures to enable the recovery or continuation of vital technology infrastructure and systems following a natural or a human induced disaster.

Disaster recovery is about what to plan for and do when a disaster occurs which knocks out the system.

So if HA and FT don't work, what then?

DR is a multiple stage set of processes . So given a disaster, it's about what happens before (the pre-planning) and what happens afterwards, the DR process itself

The worst time for any business is recovering in the event of a major disaster

A good set of DR processes need to preplan, build a set of processes and documentation, plan for staffing and physical issues when a disaster happens 

A good DR plan means taking regular backups. But the worst thing you can do is store these backups at the same site as your system: if your main site is damaged your primary data and your backups are damaged at the same time.
you need to have place in place for offsite backup storage. So in the event of a disaster the backups can be restored at the standby location 

Effective DR planning isn't just about the tech though, it's about knowledge: make sure that you have copies of all your processes available, all your logins to key systems need to be available for the staff to use when they're at this standby site.

Do this in advance and it won't be a chaotic proces when an issue inevitably occurs

Ideally you want to run periodic DR testing to make sure that you have everything you need and then if you identify anything missing  you can refine the processes and run the test again.

Conclusion



HA -> Minimize any outages

FT -> Operate through Faults

DR -> Used when these don't work











# ENHANCED Version



As a Solution Architect, it is crucial to comprehend the concepts of High Availability, Fault Tolerance, and Disaster Recovery. However, these terms are often confused, and their distinctions are not always apparent. It is essential to understand the differences between these concepts to design robust and reliable systems. By mastering these concepts, you can design systems that can withstand any challenge and provide uninterrupted service to your customers.

#### High Availability (HA)

First, let's try to give the definition of high availability. Wikipedia has a pretty good one:

> **High availability** (**HA**) is a characteristic of a system which aims to ensure an agreed level of operational performance, usually uptime, for a higher than normal period.

Many people assume that a highly available system means that it will never fail and that users will never experience outages. However, this is not entirely true. High availability (HA) is designed to keep a system online and providing services as often as possible. It is not about preventing user disruption, but rather about maximizing a system's online time.

HA is not a fail-safe mechanism that guarantees a system will never fail. Instead, it is a system designed to quickly replace or fix components when they fail, often using automation to bring systems back into service. This means that if a system fails and a component is replaced, causing a few seconds of disruption, it is still considered highly available.

System availability is generally expressed as a percentage of uptime. For example, 99.9% uptime means that a system can have 8.77 hours of downtime per year. Some systems require even higher levels of availability, such as 99.999% uptime, which only allows for 5.26 minutes of downtime per year.

Implementing HA requires design decisions to be made in advance, such as having redundant servers ready to switch customers over to in case of failure. However, it is important to note that HA comes with costs.

In summary, HA is about keeping a system operational and quickly recovering from issues. It is not about preventing user disruption, but rather maximizing a system's online time. While a highly available system can still experience disruption, it is designed to quickly recover and minimize downtime.

#### Fault Tolerance (FT)

When it comes to ensuring system reliability, two terms that are often confused: high availability and fault tolerance. While they share some similarities, fault tolerance is a more comprehensive approach.

Fault tolerance refers to a system's ability to continue functioning properly even if some of its components fail. This means that the system must be able to operate seamlessly despite the presence of faults, and without any negative impact on customers. 

Achieving fault tolerance is a complex and expensive process, as it requires a high level of redundancy and the ability to route traffic and sessions around any failed components. In contrast, high availability can be achieved by simply having spare equipment or standby components ready to go. By automating processes and having these backups in place, outages can be minimized. However, high availability alone may not be enough to ensure system reliability in the face of faults.

It's important to note that implementing fault tolerance when high availability would suffice is a waste of resources, as it is a more complex and costly approach. On the other hand, implementing high availability when fault tolerance is necessary can put lives at risk.

In summary, while high availability and fault tolerance share some similarities, fault tolerance is a more comprehensive approach that ensures system reliability even in the face of faults. Achieving fault tolerance is a complex and expensive process, but it is necessary in situations where system failure could have serious consequences.



#### Disaster Recovery (DR)

Disaster recovery is a crucial set of policies, tools, and procedures that enable the recovery or continuation of vital technology infrastructure and systems following a natural or human-induced disaster. It's about planning for the worst-case scenario and knowing what to do when disaster strikes and knocks out your system.

What happens when high availability (HA) and fault tolerance (FT) fail? That's where disaster recovery comes in. It's a multi-stage process that involves pre-planning, building a set of processes and documentation, and planning for staffing and physical issues when a disaster happens.

The worst time for any business is recovering in the event of a major disaster. That's why a good set of disaster recovery processes needs to include regular backups and offsite backup storage. Storing backups at the same site as your system is a recipe for disaster. If your main site is damaged, your primary data and backups are damaged at the same time. Having an offsite backup storage location ensures that backups can be restored at the standby location in the event of a disaster.

Effective disaster recovery planning isn't just about the technology, though. It's also about knowledge. Make sure that you have copies of all your processes available and that all your logins to key systems are accessible to staff at the standby site. By doing this in advance, you can avoid a chaotic process when an issue inevitably occurs.

Ideally, you should run periodic disaster recovery testing to ensure that you have everything you need. If you identify anything missing, you can refine the processes and run the test again. With a solid disaster recovery plan in place, you can rest assured that your business will be able to recover quickly and efficiently in the event of a disaster.

#### Conclusion

High Availability refers to a system's ability to remain operational and accessible even in the event of hardware or software failures. Fault Tolerance, on the other hand, involves designing a system to continue functioning even if a component fails. Finally, Disaster Recovery is the process of restoring a system to its previous state after a catastrophic event.
