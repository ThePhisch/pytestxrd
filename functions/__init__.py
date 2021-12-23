from typing import Type, TypeVar
from functions.function_baseclass import Pytestxrd_Base_Function
from functions.mv import Mv
from functions.testfunc import Testfunc
from functions.ping import Ping
from functions.chmod import Chmod

DerivedClass = TypeVar("DerivedClass", bound=Pytestxrd_Base_Function)

funclist: list[Type[DerivedClass]] = [ # type: ignore
    Testfunc,
    Mv,
    Chmod,
    Ping,
]
