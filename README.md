# Dependency Injection made simple.


# Instalation
```
pip instal simple-injector
```

# Getting Started
```python
from simple_injector import SimpleInjector
from random import random

class Repository():
    def __init__(self):
        self.number = random()

    def get_a_number(self):
        return self.number

class Service():
    def __init__(self, repo: Repository):
        self.repo = repo

    def get_number(self):
        return {"n":self.repo.get_a_number()}

def bootstrap():
    SimpleInjector().register(Repository)
    SimpleInjector().register_singleton(Service)

bootstrap()

repo = SimpleInjector().resolve(Repository)
serv = SimpleInjector().resolve(Service)
```

# Reference Guide

### `SimpleInjector()` 
This will always return the same instance of the SimpleInjector.

### `SimpleInjector().register(class)`
Used to register a class on the dependencies list.

### `SimpleInjector().register_singleton(class)`
Used to register a class as a singleton on the dependencies list.
This class' dependencies will be resolved at the moment of this method call, so all its dependencies must be already registered with SimpleInjector.

### `SimpleInjector().register_instance(class, obj)`
Used to register a class with its instantiate object on the dependencies list.
any call to `SimpleInjector().resolve(class)` to this class will be resolved with the object previously provided.

### `SimpleInjector().resolve(class)`
Used to resolve a dependency of a class that has been registered prior to the execution of this resolve method.
This method will return any object it has on the dependency list for this class, if it is a singleton, or a registered object, otherwise it will return a new instance for the class provided, injecting all needed dependencies, if they were registered prior to the execution of this method.

### `SimpleInjector().instantiate(class, extraParams={})`
Can be used if you need to get a new instance of some class, or if you want a new instance and want to override some param on the constructor of the class.

### `SimpleInjector().reset()`
Can be used if you need to be sure that the SimpleInjector has no dependencies registered on its list.
