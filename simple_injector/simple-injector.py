import inspect
from enum import Enum

class SimpleInjector():
    def __init__(self):
        if not self.dependencies:
            self.dependencies={}
            return

    __instance = None
    def __new__(cls):
        """
        Will always return the same instance of the SimpleInjector
        """
        if not SimpleInjector.__instance:
            SimpleInjector.__instance = super().__new__(cls)
            SimpleInjector.dependencies = {}
        return SimpleInjector.__instance

    def reset(self):
        """
        Can be used if you need to be sure that the SimpleInjector has no dependencies registered on its list
        """
        self.dependencies.clear()

    def __register(self, ref, iobj):
        self.dependencies.update({ref:iobj})

    def register(self, ref):
        """
        Used to register a class on the dependencies list.
        """
        iobj = InjectedObject(ref, InjectionType.EAGER)
        self.__register(ref, iobj)

    def register_singleton(self, ref):
        """
        Used to register a class as a singleton on the dependencies list.
        This class' dependencies will be resolved at the moment of this method call, so
        all its dependencies must be already registered with SimpleInjector.
        """
        iobj = InjectedObject(ref, InjectionType.SINGLETON, self.instantiate(ref))
        self.__register(ref, iobj)

    def register_instance(self, ref, obj):
        """
        Used to register a class with its instantiate object on the dependencies list.
        Any call to `SimpleInjector().resolve(class)` to this class will be resolved
        with the object previously provided.
        """
        iobj = InjectedObject(ref, InjectionType.EAGER, obj)
        self.__register(ref, iobj)

    def resolve(self, ref):
        """
        Used to resolve a dependency of a class that has been registered prior to the
        execution of this resolve method.
        This method will return any object it has on the dependency list for this class,
        if it is a singleton, or a registered object, otherwise it will return a new
        instance for the class provided, injecting all needed dependencies, if they were
        registered prior to the execution of this method.
        """
        dep = self.dependencies.get(ref)
        dep_got = dep.get()
        return dep_got if dep else self.instantiate(ref)

    def instantiate(self, ref, extraParams: dict = {}):
        """
        Can be used if you need to get a new instance of some class, or if you want a
        new instance and want to override some param on the constructor of the class.
        """
        sign = inspect.signature(ref)
        params = sign.parameters
        deps = {
            name: self.resolve(params[name].annotation)
            for name in params
            if params[name].annotation in self.dependencies
        }
        return ref(**{**deps, **extraParams})

class InjectionType(Enum):
    SINGLETON=1
    EAGER=2
    LAZY=3 # To be implemented

class InjectedObject():
    def __init__(self, instance_ref, injection_type: InjectionType, obj=None):
        self.__ref = instance_ref
        self.__type = injection_type
        if self.__type == InjectionType.SINGLETON and obj is None:
            raise Exception
        self.__obj = obj

    def get(self):
        if self.__type == InjectionType.SINGLETON:
            return self.__obj
        return SimpleInjector().instantiate(self.__ref)
