import inspect
from enum import Enum

class SimpleInjector():
    def __init__(self):
        if not self.dependencies:
            self.dependencies={}
            return

    __instance = None
    def __new__(cls):
        if not SimpleInjector.__instance:
            SimpleInjector.__instance = super().__new__(cls)
            SimpleInjector.dependencies = {}
        return SimpleInjector.__instance

    def reset(self):
        self.dependencies.clear()

    def __register(self, ref, iobj):
        self.dependencies.update({ref:iobj})

    def register(self, ref):
        iobj = InjectedObject(ref, InjectionType.EAGER)
        self.__register(ref, iobj)

    def register_singleton(self, ref):
        iobj = InjectedObject(ref, InjectionType.SINGLETON, self.instantiate(ref))
        self.__register(ref, iobj)

    def register_instance(self, ref, obj):
        iobj = InjectedObject(ref, InjectionType.EAGER, obj)
        self.__register(ref, iobj)

    def resolve(self, ref):
        dep = self.dependencies.get(ref)
        dep_got = dep.get()
        return dep_got if dep else self.instantiate(ref)

    def instantiate(self, ref, extraParams: dict = {}):
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
