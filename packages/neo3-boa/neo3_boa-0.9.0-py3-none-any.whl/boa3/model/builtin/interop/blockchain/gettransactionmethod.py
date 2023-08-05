from typing import Dict

from boa3.model.builtin.interop.blockchain.transactiontype import TransactionType
from boa3.model.builtin.interop.nativecontract import LedgerMethod
from boa3.model.variable import Variable


class GetTransactionMethod(LedgerMethod):

    def __init__(self, transaction_type: TransactionType):
        from boa3.model.type.collection.sequence.uint256type import UInt256Type

        identifier = 'get_transaction'
        syscall = 'getTransaction'
        args: Dict[str, Variable] = {'hash_': Variable(UInt256Type.build())}
        super().__init__(identifier, syscall, args, return_type=transaction_type)
