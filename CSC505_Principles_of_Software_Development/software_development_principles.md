Coupling
- Coupling refers to the interdependencies between modules. 
- Coupling is the principle of "separation of concerns". This means that one object doesn't directly change or modify the state or behavior of another object. 
- Coupling looks at the relationship between objects and how closely connected they are.
- Objective: loose coupling. 
    - Objects that are independent from one another and do not directly modify the state of other objects are said to be loosely coupled. 
    - Loose coupling lets the code be more flexible, more changeable, and easier to work with.

Cohesion
- Cohesion refers to the degree to which the elements inside a module belong together. 
- In one sense, it is a measure of the strength of relationship between the methods and data of a class and some unifying purpose or concept served by that class.
- Cohesion describes how related the functions within a single module are. 

Tell Don't Ask
The Tell, Don't Ask (TDA) principle suggests that it is better to issue an object a command do perform some operation or logic, rather than to query its state and then take some action as a result.

YAGNI 
"You aren't gonna need it" (YAGNI) is a principle of extreme programming (XP) that states a programmer should not add functionality until deemed necessary.

SOLID Design Principles
- Single Responsibility Principle
- Open Closed Principle
- Liskov's Substitutability Principle
- Interface Segregation Principle
- Dependency Inversion Principle