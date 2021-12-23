from typing import Type, TypeVar
from functions.function_baseclass import Pytestxrd_Base_Function
from functions.mv import Mv
from functions.testfunc import Testfunc
from functions.ping import Ping

DerivedClass = TypeVar("DerivedClass", bound=Pytestxrd_Base_Function)

funclist: list[Type[DerivedClass]] = [ # type: ignore
    Testfunc,
    Mv,
    Ping
]
