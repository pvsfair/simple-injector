import inspect
from enum import Enum

def inject(ref):
    return SimpleInjector().resolve(ref)

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
        Can be used if you need to be sure that the SimpleInjector has no dependencies
            registered on its list
        """
        self.dependencies.clear()

    def __register(self, ref, iobj):
        self.dependencies.update({ref:iobj})

    def register(self, ref, obj_or_callable=None):
        """
        Used to register a class on the dependencies list.
        Can also receive an instance of the object that you want to assign to it.
        Can also receive a callable with one parameter, that will be the instance
            of the Reference.
        Can also receive a callable with 0 parameters.
        Any lambda received as a parameter should always return the instance that
            will be injected.
        """
        if callable(obj_or_callable):
            if len(inspect.signature(obj_or_callable).parameters) > 1:
                raise Exception("Should be 0 or 1 parameter")

            iobj = InjectedObject(ref, InjectionType.LAMBDA, obj_or_callable)
            self.__register(ref, iobj)
            return

        iobj = InjectedObject(ref, InjectionType.EAGER, obj_or_callable)
        self.__register(ref, iobj)

    def singleton(self, ref):
        """
        Used to register a class as a singleton on the dependencies list.
        This class' dependencies will be resolved at the moment of this method call, so
            all its dependencies must be already registered with SimpleInjector.
        """
        iobj = InjectedObject(ref, InjectionType.SINGLETON, self.instantiate(ref))
        self.__register(ref, iobj)

    def lazy(self, ref, obj):
        """
        Used to register a class with its instantiate object on the dependencies list.
        Any call to `SimpleInjector().resolve(class)` to this class will be resolved
            with the object previously provided.
        """
        iobj = InjectedObject(ref, InjectionType.LAZY, obj)
        self.__register(ref, iobj)

    def resolve(self, ref):
        """
        Used to resolve a dependency of a class that has been registered prior to the
            execution of this resolve method.
        This method will return an object it has on the dependency list for this class,
            if it is a singleton, or a registered object, otherwise it will return a
            new instance for the class provided, injecting all needed dependencies, if
            they were registered prior to the execution of this method.
        """
        dep = self.dependencies.get(ref)
        dep_got = dep.get()
        return dep_got if dep else self.instantiate(ref)

    def instantiate(self, ref, extraParams: dict = {}):
        """
        Can be used if you need to get a new instance of some class, or if you want a
            new instance and want to override some param on the constructor of the
            class.
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
    LAMBDA=4

class InjectedObject():
    def __init__(self, instance_ref, injection_type: InjectionType, obj=None):
        self.__ref = instance_ref
        self.__type = injection_type
        if self.__type == InjectionType.SINGLETON and obj is None:
            raise Exception
        self.__obj = obj

    def get(self):
        if self.__type == InjectionType.LAMBDA:
            params = inspect.signature(self.__obj).parameters
            deps = {}
            if len(params):
                deps = {
                    name: SimpleInjector().instantiate(self.__ref)
                    for name in params
                }
            return self.__obj(**deps)

        if self.__type == InjectionType.SINGLETON or self.__obj is not None:
            return self.__obj
        return SimpleInjector().instantiate(self.__ref)
