import sys
from typing import Any
if sys.version_info >= (3, 11):
	from typing import Self
else:
	Self = Any


class Token: pass

class Punctuation(Token):

	def __eq__(self, t: Self) -> bool:
		return self.__class__ == t.__class__

class ArgToken(Token):

	def __init__(self, d: Any):
		self.d = d

	def __eq__(self, t: Self) -> bool:
		return (self.__class__, self.d) == (t.__class__, t.d)

class Comma(Punctuation):

	def __repr__(self) -> str:
		return 't$Comma'

class Semicolon(Punctuation):

	def __repr__(self) -> str:
		return 't$Semicolon'

class Colon(Punctuation):

	def __repr__(self) -> str:
		return 't$Colon'

class IntLiteral(ArgToken):

	def __init__(self, n: int):
		self.d = n

	def __repr__(self) -> str:
		return f't$IntLiteral({self.d})'

class StrLiteral(ArgToken):

	def __init__(self, s: bytes):
		self.d = s.decode()

	def __repr__(self) -> str:
		return f't$StrLiteral({self.d})'

class Reg(ArgToken):

	def __init__(self, n: int):
		self.d = n

	def __repr__(self) -> str:
		return f't$Reg({self.d})'

class Ident(ArgToken):

	def __init__(self, s: bytes):
		self.d = s

	def __repr__(self) -> str:
		return f"t$Ident('{self.d.decode()}')"
