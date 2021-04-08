"""
OOP is a programming paradigm that provides a means of structuring
programs so that properties and behaviors are bundled into individual
objects.

An object contains data and behavior.
"""

"""
Classes are used to create user-defined data structures.

functions are methods - class behaviors

Class is a blueprint for how object defined

Class instance is built from class blueprint and contains real data

"""

# define class
class Dog:
    # class attribute
    species = "Canis familiaris"

    # sets the initial instance state
    def __init__(self, name, age):      # dunder method __method__
        self.name = name # attribute
        self.age = age 

    # Instance method
    def speak(self, sound):
        return f"{self.name} says {sound}"

# child class
class JackRussellTerrier(Dog):
    # will override parent method (only do if necessary)
    # def speak(self, sound="Arf"):
        #return f"{self.name} says {sound}"

    # extend functionality of parent class
    def speak(self, sound="Arf"):
        # call parent class speak with child class speak arguments
        return super().speak(sound) 

# instantiating an object from a class
fluffy = Dog("Fluffy", 10)
fluffy.name
fluffy.age
fluffy.species

miles = JackRussellTerrier("Miles", 4) 
miles.speak()
# 'Miles says Arf'
type(miles)
instance(miles, Dog)

"""
Inheritance is the process by which one class takes on the attributes
and methods of another.

Classes derived from classes are child classes.
Parent - child classes

e.g. dying your hair a different color = overriding the hair color 
attribute you inherited

e.g. you learn an additional language. you extend your language attributes
that you inherited.
"""