'''Translators for each assembler directive.

Each directive is represented by a top-level function in this module with the
`do_` prefix.  The name of the directive corresponds with the name of the
function, with the leading dot stripped and the aforementioned `do_` added.
Any additional dots are not allowed.

In order to add a directive, all that is required is to define the appropriate
function.  Directives have access to the following resources:

- Current address (read-only).
- Labels dictionary (read-write).
- General process state (via Python modules).

They can append to the output file by means of their function's return value.
'''

from .operand import ImmOperand, StrOperand
from .statement import Directive
from .transutil import (InvalidOperandError, pop_operand, pop_operand_default,
	extract_operands)
from typing import Any, Callable


## Raw-data directives.

def nbyte(itemsize: int) -> Callable[..., Any]:
	def f(d: Directive, *_args) -> bytes:
		'''Output one or more raw N-byte values.'''
		out = []
		while o := pop_operand_default(d, None):
			if not isinstance(o, ImmOperand):
				raise InvalidOperandError(d)
			try:
				b = o.d.to_bytes(itemsize, 'big')
			except ValueError:
				raise InvalidOperandError(d)
			out.append(b)
		return b''.join(out)
	return f

do_byte = nbyte(1)
do_2byte = nbyte(2)
do_4byte = nbyte(4)
do_8byte = nbyte(8)

def do_fill(d: Directive, *_args) -> bytes:
	'''Output a given amount of a constant value with a given size.'''
	cnt, sz, val = extract_operands(d, (ImmOperand,),
		(ImmOperand(1), ImmOperand(0)))
	try:
		b = val.d.to_bytes(sz.d, 'big')
	except ValueError:
		raise InvalidOperandError(d)
	return b * cnt.d

def do_space(d: Directive, *_args) -> bytes:
	'''Output a given amount of a constant byte.'''
	cnt, val = extract_operands(d, (ImmOperand,), (ImmOperand(0),))
	try:
		return bytes(val.d for _ in range(cnt.d))
	except ValueError:
		raise InvalidOperandError(d)

def do_zero(d: Directive, *_args) -> bytes:
	'''Output a given amount of zero bytes.'''
	cnt, = extract_operands(d, (ImmOperand,))
	return bytes(cnt.d)

def do_incbin(d: Directive, *_args) -> bytes:
	'''Include a binary file verbatim.'''
	path, start, count = extract_operands(d, (StrOperand,),
		(ImmOperand(0), ImmOperand(-1)))
	with open(path.d, 'rb') as f:
		if start.d:
			f.seek(start.d)
		return f.read(count.d)
