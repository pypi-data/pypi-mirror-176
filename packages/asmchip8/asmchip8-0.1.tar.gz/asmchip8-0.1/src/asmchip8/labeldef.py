import sys
from typing import Any
if sys.version_info >= (3, 11):
	from typing import Self
else:
	Self = Any


class LabelDef:

	def __init__(self, s: bytes):
		self.s = s
		self.linum = 0

	def __eq__(self, ld: Self) -> bool:
		return self.s == ld.s

	def __repr__(self) -> str:
		return f'b$Label({self.s.decode()})'

	def normal_line(self) -> 'bytes':
		return self.s + b':'
