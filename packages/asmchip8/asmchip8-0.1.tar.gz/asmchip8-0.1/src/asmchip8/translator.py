from .operand import CurAddrOperand, ImmOperand, LabelOperand, RegOperand
from .statement import Statement, Directive, Instruction
from .transutil import (PcTooLargeError, InvalidLabelError,
	InvalidDirectiveError, InvalidInsError, InvalidOperandError,
	MissingOperandError, LeftoverOperandError, pop_operand)
from . import transdir
from functools import wraps
from typing import Any, Callable


# The program is expected to be loaded at this address.  The file is not
# prefixed with zeroes, however.  Offset `n` in the file would represent
# address `STARTS_ADDRESS + n` in memory.
START_ADDRESS = 512

# Mapping from instruction mnemonics to machine encoding formulas.
#
# A formula is a string of length 4 where each character represents one nibble
# (4 bits) of the instruction in machine language, in big-endian order.  The
# character used determines what value corresponds to the nibble:
#
# 	`0..9A..F`: literal nibble; no translation required for it.
# 	`x`:        first general purpose register operand.
# 	`y`:        second general purpose register operand.
# 	`n`:        immediate operand; the number of consecutive occurrences
# 	            determines its size, from 1 to 3 nibbles (4, 8 or 12
# 	            bits).
# 	`l`:        immediate operand, label or current address; always 3 nibbles
#                   (12 bits).
INS_TABLE = {
	b'cls':     '00E0',
	b'rts':     '00EE',
	b'syscall': '0nnn',
	b'j':       '1lll',
	b'jsr':     '2lll',
	b'skei':    '3xnn',
	b'skni':    '4xnn',
	b'sker':    '5xy0',
	b'li':      '6xnn',
	b'addi':    '7xnn',
	b'move':    '8xy0',
	b'or':      '8xy1',
	b'and':     '8xy2',
	b'xor':     '8xy3',
	b'add':     '8xy4',
	b'sub':     '8xy5',
	b'shr':     '8xy6',
	b'sbr':     '8xy7',
	b'shl':     '8xyE',
	b'sknr':    '9xy0',
	b'la':      'Alll',
	b'jr0':     'Blll',
	b'rand':    'Cxnn',
	b'draw':    'Dxyn',
	b'skkp':    'Ex9E',
	b'skku':    'ExA1',
	b'mfdt':    'Fx07',
	b'waitk':   'Fx0A',
	b'mtdt':    'Fx15',
	b'mtst':    'Fx18',
	b'addx':    'Fx1E',
	b'font':    'Fx29',
	b'bcd':     'Fx33',
	b'sm':      'Fx55',
	b'lm':      'Fx65'
}

def encode(f: Callable[..., int]) -> Callable[..., bytes]:
	@wraps(f)
	def g(*args) -> bytes:
		return f(*args).to_bytes(2, 'big')
	return g

def noleftovers(f: Callable[..., Any]) -> Callable[..., Any]:
	@wraps(f)
	def g(st: Statement, *rest):
		ret = f(st, *rest)
		if st.operands:
			raise LeftoverOperandError(st)
		return ret
	return g

def resolve_label(l: LabelOperand, labels: dict[str, int], linum: int) -> int:
	try:
		addr = labels[l.d]
	except KeyError:
		raise InvalidLabelError(l, linum)
	if addr > 0xFFF:
		raise InvalidLabelError(l, linum)
	return addr

@encode
@noleftovers
def translate_ins(ins: Instruction, offset: int,
		labels: dict[str, int]) -> int:
	'''Translate an instruction into machine code.

	Parameters:
		ins    -- the instruction to translate.
		offset -- current address of the instruction (should start
		          counting from `START_ADDRESS`).
		labels -- dictionary of label definitions.

	Returns: bytes representing the machine code of the instruction.

	Raises:
		InvalidInsError
		InvalidLabelError
		InvalidOperandError
		LeftoverOperandError
		MissingOperandError
		PcTooLargeError
	'''
	try:
		formula = INS_TABLE[ins.mnemonic]
	except KeyError:
		raise InvalidInsError(ins)

	# First nibble.
	mcode = int(formula[0], 16) << 12

	# Second nibble.
	if formula[1] == 'x':
		x = pop_operand(ins)
		if not isinstance(x, RegOperand):
			raise InvalidOperandError(ins)
		mcode |= x.d << 8
	elif formula[1] == 'n':
		nnn = pop_operand(ins)
		if not isinstance(nnn, ImmOperand) or nnn.d > 0xFFF:
			raise InvalidOperandError(ins)
		return mcode | nnn.d
	elif formula[1] == 'l':
		lll = pop_operand(ins)
		if isinstance(lll, LabelOperand):
			return mcode | resolve_label(lll, labels, ins.linum)
		if isinstance(lll, CurAddrOperand):
			if offset > 0xFFF:
				raise PcTooLargeError(ins.linum)
			return mcode | offset
		if isinstance(lll, ImmOperand):
			if lll.d > 0xFFF:
				raise InvalidOperandError(ins)
			return mcode | lll.d
		raise InvalidOperandError(ins)
	else:
		mcode |= int(formula[1], 16) << 8

	# Third nibble.
	if formula[2] == 'y':
		y = pop_operand(ins)
		if not isinstance(y, RegOperand):
			raise InvalidOperandError(ins)
		mcode |= y.d << 4
	elif formula[2] == 'n':
		nn = pop_operand(ins)
		if not isinstance(nn, ImmOperand) or nn.d > 0xFF:
			raise InvalidOperandError(ins)
		return mcode | nn.d
	else:
		mcode |= int(formula[2], 16) << 4

	# Fourth nibble.
	if formula[3] == 'n':
		n = pop_operand(ins)
		if not isinstance(n, ImmOperand) or n.d > 0xF:
			raise InvalidOperandError(ins)
		return mcode | n.d
	else:
		mcode |= int(formula[3], 16)

	return mcode

def translate_directive(d: Directive, offset: int,
		labels: dict[str, int]) -> bytes:
	'''Apply an assembler directive.'''
	name = 'do_' + d.mnemonic.decode()
	try:
		f = getattr(transdir, name)
	except AttributeError:
		raise InvalidDirectiveError(d)
	return f(d, offset, labels)

def translate_stmt(st: Statement, *args) -> bytes:
	'''Translate/Apply a statement.'''
	if isinstance(st, Instruction):
		f = translate_ins
	else:
		f = translate_directive
	return f(st, *args)
