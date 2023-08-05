from typing import Dict, Optional, Tuple

from boa3.model.variable import Variable


class FunctionArguments:

    def __init__(self):
        self._args: Dict[str, Variable] = {}
        self._vararg: Optional[Tuple[str, Variable]] = None

    @property
    def args(self) -> Dict[str, Variable]:
        return self._args.copy()

    def add_arg(self, arg_id: str, arg: Variable) -> bool:
        if not isinstance(arg, Variable):
            return False
        self._args[arg_id] = arg
        return True

    @property
    def vararg(self) -> Optional[Tuple[str, Variable]]:
        return self._vararg

    def set_vararg(self, arg_id: str, arg: Variable) -> bool:
        if not isinstance(arg, Variable):
            return False
        self._vararg = (arg_id, arg)
        return True
