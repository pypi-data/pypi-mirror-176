from .operand import Operand
import sys
from typing import Any
if sys.version_info >= (3, 11):
	from typing import Self
else:
	Self = Any


class Statement:

	def __init__(self, mnemonic: bytes, operands: list[Operand]):
		self.mnemonic = mnemonic
		self.operands = operands
		self.linum = 0

	def __eq__(self, st: Self) -> bool:
		return ((self.mnemonic, self.operands)
			== (st.mnemonic, st.operands))

	def __repr__(self) -> str:
		ops = ', '.join(map(repr, self.operands))
		sep = ' ' if ops else ''
		c = self.__class__.__name__
		return f'b${c}({self.mnemonic.decode()}{sep}{ops})'

	def normal_line(self) -> str:
		ops = ','.join(map(repr, self.operands))
		sep = ' ' if ops else ''
		return f'{self.mnemonic.decode()}{sep}{ops}'

class Directive(Statement):

	def normal_line(self) -> str:
		return '.' + super().normal_line()

class Instruction(Statement): pass
