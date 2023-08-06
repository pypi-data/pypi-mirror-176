from .assemblyerror import AssemblyError
import sys
from typing import Any
if sys.version_info >= (3, 11):
	from typing import Self
else:
	Self = Any


class InvalidRegError(AssemblyError):
	pass

class Operand:
	def __eq__(self, o: Self) -> bool:
		return self.__class__ == o.__class__

class ArgOperand(Operand):

	def __init__(self, d: Any):
		self.d = d

	def __eq__(self, o: Self) -> bool:
		return (self.__class__, self.d) == (o.__class__, o.d)

class CurAddrOperand(Operand):

	def __str__(self) -> str:
		return f'o$CurAddr'

	def normal_line(self) -> str:
		return '.'

class ImmOperand(ArgOperand):

	def __init__(self, n: int):
		self.d = n

	def __str__(self) -> str:
		return f'o$Imm({self.d})'

	def normal_line(self) -> str:
		return str(self.d)

class LabelOperand(ArgOperand):

	def __init__(self, s: bytes):
		self.d = s

	def __str__(self) -> str:
		return f'o$Label({self.d.decode()})'

	def normal_line(self) -> str:
		return self.d.decode()

class RegOperand(ArgOperand):

	def __init__(self, v: int):
		if v < 0 or 15 < v:
			raise InvalidRegError(-1, v)
		self.d = v

	def __str__(self) -> str:
		return f'o$Reg({self.d})'

	def normal_line(self) -> str:
		return f'v{self.d}'

class StrOperand(ArgOperand):

	def __init__(self, s: str):
		self.d = s

	def __str__(self) -> str:
		return f'o$Str({self.d})'

	def normal_line(self) -> str:
		return f'"{self.d}"'
