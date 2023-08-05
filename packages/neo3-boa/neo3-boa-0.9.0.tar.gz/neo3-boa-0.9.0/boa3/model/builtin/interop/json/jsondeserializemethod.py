from typing import Dict

from boa3.model.builtin.interop.nativecontract import StdLibMethod
from boa3.model.variable import Variable


class JsonDeserializeMethod(StdLibMethod):
    def __init__(self):
        from boa3.model.type.type import Type
        identifier = 'json_deserialize'
        native_identifier = 'jsonDeserialize'
        args: Dict[str, Variable] = {'json': Variable(Type.bytes)}
        super().__init__(identifier, native_identifier, args, return_type=Type.any)
