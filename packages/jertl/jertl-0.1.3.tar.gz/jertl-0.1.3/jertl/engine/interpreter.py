from   dataclasses import dataclass
from   functools   import singledispatch
from   typing      import Dict, List, Any
from   copy        import copy

from   jertl.engine.opcodes   import OpCode
from   jertl.engine.masks     import MaskedList, MaskedDict, freeze, snapshot
from   jertl.exceptions       import JertlInterpreterException

@dataclass
class Context:
    identifier:  str
    bindings:    Dict[str, Any]
    focus_stack: List[Any]
    ic:          int

@singledispatch
def values_match(a, b):
    return a == b

@values_match.register(int)
def _(a, b):
    return isinstance(b, int) and not isinstance(b, bool) and a == b

@values_match.register(float)
def _(a, b):
    return isinstance(b, float) and a == b

@values_match.register(bool)
def _(a, b):
    return isinstance(b, bool) and a == b

@values_match.register(type(None))
def _(_, b):
    return b is None


class Interpreter:
    """_summary_"""

    def __init__(self, instructions, trace=False):
        """__init__

        Args:
            instructions List[OpCode]: the 'program' to interpred
            trace (bool, optional): Flag determining if we should trace operation of vm, defaults to False
        """
        self.instructions  = instructions
        self.trace         = trace
        self.focus_stack   = []
        self.context_stack = []
        self.ic            = 0
        self.running       = False

    def backtrack(self):
        if self.trace:
            print(f'...backtracking')

        if len(self.context_stack) > 0:
            context = self.context_stack[-1]
            if len(context.focus_stack[-1]) == 0:
                self.context_stack.pop()
                self.backtrack()
            else:
                context.bindings[context.identifier].widen()
                context.focus_stack[-1].pop()
                self.focus_stack = copy(context.focus_stack)
                self.focus_stack[-1] = context.focus_stack[-1].snapshot()
                self.ic = context.ic
                self.bindings = copy(self.bindings)
        else:
            # Nothing left to do
            self.running = False

    def maybe_trace(self):
        if self.trace:
            ic    = self.ic
            fc    = len(self.focus_stack) - 1
            focus = self.focus_stack[-1] if fc >= 0 else '<NO-FOCUS>'
            print(f'ic: {ic:3}, focus[{fc}]:{self.instructions[ic]} -- {focus}')


    def match_all(self, focus, bindings=None):
        self.running = True
        self.bindings = {} if bindings is None else bindings
        self.focus_stack.append(focus)

        while self.running:
            self.maybe_trace()

            instruction = self.instructions[self.ic]
            opcode      = instruction[0]
            self.ic    += 1

            if opcode == OpCode.MATCH_VALUE:
                if not values_match(instruction[1], self.focus_stack[-1]):
                    self.backtrack()

            elif opcode == OpCode.MATCH_VARIABLE:
                if not values_match(self.bindings[instruction[1]], self.focus_stack[-1]):
                    self.backtrack()

            elif opcode == OpCode.BIND_VARIABLE:
                self.bindings[instruction[1]] = self.focus_stack[-1]

            elif opcode == OpCode.BIND_VARARGS:
                binding = self.focus_stack[-1].snapshot()
                binding.collapse()
                self.bindings[instruction[1]] = binding

                context = Context(identifier=instruction[1],
                                  focus_stack=[snapshot(focus) for focus in self.focus_stack],
                                  bindings=copy(self.bindings),
                                  ic=self.ic)

                self.context_stack.append(context)

            elif opcode == OpCode.MATCH_VARARGS:
                binding = self.bindings[instruction[1]]
                if len(binding) <= len(self.focus_stack[-1]):
                    for value in binding:
                        if not values_match(value, self.focus_stack[-1].pop()):
                            self.backtrack()
                            break
                else:
                    self.backtrack()

            elif opcode == OpCode.MASK_IF_LIST:
                if not isinstance(self.focus_stack[-1], list):
                    self.backtrack()
                else:
                    self.focus_stack[-1] = MaskedList(self.focus_stack[-1])

            elif opcode == OpCode.MASK_IF_DICT:
                if not isinstance(self.focus_stack[-1], dict):
                    self.backtrack()
                else:
                    self.focus_stack[-1] = MaskedDict(self.focus_stack[-1])

            elif opcode == OpCode.FOCUS_ON_HEAD:
                if len(self.focus_stack[-1]) == 0:
                    self.backtrack()
                else:
                    self.focus_stack.append(self.focus_stack[-1].pop())

            elif opcode == OpCode.FOCUS_ON_KEY:
                if instruction[1] not in self.focus_stack[-1]:
                    self.backtrack()
                else:
                    self.focus_stack.append(self.focus_stack[-1].pop(instruction[1]))

            elif opcode == OpCode.FOCUS_ON_BINDING:
                self.focus_stack.append(self.bindings[instruction[1]])

            elif opcode == OpCode.POP_FOCUS:
                self.focus_stack.pop()

            elif opcode == OpCode.YIELD_BINDINGS:
                yield {v: freeze(b) for v, b in self.bindings.items()}
                self.backtrack()

            else:
                raise JertlInterpreterException(f'OpCode {opcode} not understood')
