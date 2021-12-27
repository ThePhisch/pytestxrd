from typing import Type, TypeVar
from functions.function_baseclass import Pytestxrd_Base_Function
from functions.mv import Mv
from functions.ping import Ping
from functions.chmod import Chmod
from functions.dir import Dir
from functions.rm import Rm
from functions.rmdir import Rmdir
from functions.open import Open
from functions.close import Close

DerivedClass = TypeVar("DerivedClass", bound=Pytestxrd_Base_Function)

funclist: list[Type[DerivedClass]] = [Dir, Mv, Chmod, Ping, Rm, Rmdir, Open, Close]  # type: ignore
