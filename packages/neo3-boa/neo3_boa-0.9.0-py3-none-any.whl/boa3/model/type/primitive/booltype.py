from typing import Any

from boa3.model.type.itype import IType
from boa3.model.type.primitive.inttype import IntType
from boa3.neo.vm.type.AbiType import AbiType
from boa3.neo.vm.type.StackItem import StackItemType


class BoolType(IntType):
    """
    A class used to represent Python bool type
    """

    def __init__(self):
        super().__init__()
        self._identifier = 'bool'

    @property
    def default_value(self) -> Any:
        return bool()

    @property
    def abi_type(self) -> AbiType:
        return AbiType.Boolean

    @property
    def stack_item(self) -> StackItemType:
        return StackItemType.Boolean

    @classmethod
    def build(cls, value: Any) -> IType:
        if cls._is_type_of(value):
            from boa3.model.type.type import Type
            return Type.bool

    @classmethod
    def _is_type_of(cls, value: Any):
        return type(value) in [bool, BoolType]
