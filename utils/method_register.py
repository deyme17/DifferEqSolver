from typing import Optional
from core import ODEMethodInterface



class ODEMethodRegistry:
    _methods: dict[str, ODEMethodInterface]

    @classmethod
    def register(cls, method_class: ODEMethodInterface) -> ODEMethodInterface:
        if not issubclass(method_class, ODEMethodInterface):
            raise TypeError("Method must inherit from ODEMethodInterface")
        cls._methods[method_class.__name__.lower()] = method_class
        return method_class

    @classmethod
    def get_method(cls, method_id: str) -> Optional[ODEMethodInterface]:
        return cls._methods.get(method_id)

    @classmethod
    def get_method_choices(cls) -> list[tuple[str, str]]:
        return [
            (key, getattr(cls._methods[key], "display_name", key.title()))
            for key in cls._methods
        ]