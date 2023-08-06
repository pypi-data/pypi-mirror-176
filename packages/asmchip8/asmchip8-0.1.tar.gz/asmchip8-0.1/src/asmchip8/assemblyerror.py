from typing import Any


class AssemblyError(Exception):
	def __init__(self, linum: int, data: Any = ''):
		self.linum = linum
		self.data = data
