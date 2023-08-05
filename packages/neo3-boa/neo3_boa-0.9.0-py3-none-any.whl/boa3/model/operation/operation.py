from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from boa3.model.operation.operator import Operator
from boa3.model.type.itype import IType
from boa3.neo.vm.opcode.Opcode import Opcode


class IOperation(ABC):
    """
    An interface used to represent operations

    :ivar operator: the operator of the operation
    :ivar result: the result type of the operation
    """

    def __init__(self, operator: Operator, result_type: IType):
        self.operator: Operator = operator
        self.result: IType = result_type

    @property
    def opcode(self) -> List[Tuple[Opcode, bytes]]:
        """
        Gets the operation sequence of opcodes with in Neo Vm

        :return: the opcode if exists. Empty list otherwise.
        """
        return []

    @property
    def bytecode(self) -> bytes:
        """
        Gets the operation bytecode

        :return: the bytecode if exists. Empty bytes otherwise.
        """
        str_mult_bytes = bytearray()
        for opcode, data in self.opcode:
            str_mult_bytes += opcode + data
        return bytes(str_mult_bytes)

    @property
    @abstractmethod
    def number_of_operands(self) -> int:
        """
        Gets the number of operands required for this operations

        :return: Number of operands
        """
        pass

    @property
    def op_on_stack(self) -> int:
        """
        Gets the number of arguments that must be on stack before the opcode is called.

        :return: the number of arguments. Same from `number_of_operands` by default.
        """
        return self.number_of_operands

    @abstractmethod
    def validate_type(self, *types: IType) -> bool:
        """
        Verifies if the given operands are valid to the operation

        :param types: types of the operand
        :return: True if all arguments are valid. False otherwise.
        """
        pass

    def is_valid(self, operator: Operator, *types: IType) -> bool:
        """
        Verifies if the given operator and operands are valid to the operation

        :param operator:
        :param types: types of the operand
        :return: True if all arguments are valid. False otherwise.
        """
        if len(types) != self.number_of_operands:
            return False

        return operator is self.operator and self.validate_type(*types)

    @property
    def is_supported(self) -> bool:
        """
        Verifies if the operation is supported by the compiler

        :return: True if it is supported. False otherwise.
        """
        return True

    @classmethod
    @abstractmethod
    def build(cls, *operands: IType) -> Optional[IOperation]:
        """
        Creates an operation with the given operands types

        :param operands: operands types
        :return: The built operation if the operands are valid. None otherwise
        :rtype: IOperation or None
        """
        return None
