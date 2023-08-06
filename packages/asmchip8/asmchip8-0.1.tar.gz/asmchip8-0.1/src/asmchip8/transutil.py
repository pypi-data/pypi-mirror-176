from .operand import Operand, ImmOperand, LabelOperand
from .statement import Statement
from collections.abc import Iterable


class PcTooLargeError(Exception):
	def __init__(self, linum: int):
		self.linum = linum

class InvalidLabelError(Exception):
	def __init__(self, lb: LabelOperand, linum: int):
		self.name = lb.d
		self.linum = linum

class StatementError(Exception):
	def __init__(self, st: Statement):
		self.name = st.mnemonic
		self.linum = st.linum

class InvalidDirectiveError(StatementError): pass
class InvalidInsError(StatementError): pass
class InvalidOperandError(StatementError): pass
class MissingOperandError(StatementError): pass
class LeftoverOperandError(StatementError): pass

def pop_operand(st: Statement) -> Operand:
	try:
		return st.operands.pop(0)
	except IndexError:
		raise MissingOperandError(st)

def pop_operand_default(st: Statement, default: Operand|None) -> Operand|None:
	try:
		return st.operands.pop(0)
	except IndexError:
		return default

def extract_operands(st: Statement, mandatory: Iterable[type],
		optionals: Iterable[Operand] = ()) -> list[Operand]:
	ops = []
	for c in mandatory:
		o = pop_operand(st)
		if not isinstance(o, c):
			raise InvalidOperandError(st)
		ops.append(o)
	for default in optionals:
		ops.append(pop_operand_default(st, default))
	if st.operands:
		raise LeftoverOperandError(st)
	return ops
