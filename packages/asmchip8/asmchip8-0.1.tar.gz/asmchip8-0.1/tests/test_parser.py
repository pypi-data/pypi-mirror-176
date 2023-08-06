'''Unit tests for parser.'''

from asmchip8.statement import Directive, Instruction
from asmchip8.labeldef import LabelDef
from asmchip8.operand import ImmOperand, LabelOperand, RegOperand, StrOperand
from asmchip8.parser import parse_tokens, LeftoverParseError
from asmchip8.token import (Comma, Semicolon, Colon, IntLiteral, StrLiteral,
	Reg, Ident)
import pytest


def p(ts):
	return list(parse_tokens(ts, 0))

def test_empty():
	assert p([]) == []

def test_semicolons_alone():
	assert p([Semicolon()]) == []
	assert p([Semicolon(), Semicolon()]) == []

def test_semicolons_with_instruction():
	tss = (
		[Semicolon(), Ident(b'ins')],
		[Semicolon(), Semicolon(), Ident(b'ins')],
		[Ident(b'ins'), Semicolon()],
		[Ident(b'ins'), Semicolon(), Semicolon()],
		[Semicolon(), Ident(b'ins'), Semicolon()],
		[Semicolon(), Semicolon(), Ident(b'ins'),
			Semicolon(), Semicolon()]
	)
	for ts in tss:
		assert p(ts) == [Instruction(b'ins', [])]

def test_leftover_simple():
	with pytest.raises(LeftoverParseError):
		p([Comma()])
		p([Colon()])

def test_leftover_in_operands():
	with pytest.raises(LeftoverParseError):
		p([Ident(b'mne'), Comma()])
		p([Ident(b'mne'), Comma(), Reg(0)])
		p([Ident(b'mne'), Reg(0), Comma()])
		p([Ident(b'mne'), Reg(0), Comma(), Comma(), Reg(0)])

def test_leftover_in_labeldef():
	with pytest.raises(LeftoverParseError):
		p([Ident(b'hello'), Colon(), Colon()])
		p([Ident(b'hello'), Colon(), Comma()])
		p([Ident(b'hello'), Comma(), Colon()])
		p([Ident(b'hello'), Semicolon(), Colon()])

def test_directive_mnemonic():
	mnems = [b'byte', b'fill', b'zero']
	for m in mnems:
		assert p([Ident(b'.' + m)]) == [Directive(m, [])]

def test_instruction_mnemonic():
	mnems = [b'cls', b'j', b'jv0', b'syscall']
	for m in mnems:
		assert p([Ident(m)]) == [Instruction(m, [])]

def test_instruction_sequence():
	pairs = (
		([Ident(b'one'), Semicolon(), Ident(b'two')],
			[Instruction(b'one', []), Instruction(b'two', [])]),
		([Ident(b'one'), Semicolon(), Semicolon(), Ident(b'two')],
			[Instruction(b'one', []), Instruction(b'two', [])]),
		([Ident(b'one'), Semicolon(), Ident(b'two'), Semicolon()],
			[Instruction(b'one', []), Instruction(b'two', [])]),
		([Semicolon(), Ident(b'one'), Semicolon(), Ident(b'two')],
			[Instruction(b'one', []), Instruction(b'two', [])]),
		([Ident(b'one'), Semicolon(), Ident(b'two'),
				Semicolon(), Ident(b'three')],
			[Instruction(b'one', []), Instruction(b'two', []),
				Instruction(b'three', [])])
	)
	for ts, res in pairs:
		assert p(ts) == res

def test_operand_types():
	pairs = (
		([Ident(b'mne'), IntLiteral(42)],
			[Instruction(b'mne', [ImmOperand(42)])]),
		([Ident(b'mne'), StrLiteral(b'foo')],
			[Instruction(b'mne', [StrOperand('foo')])]),
		([Ident(b'mne'), Ident(b'hello')],
			[Instruction(b'mne', [LabelOperand(b'hello')])]),
		([Ident(b'mne'), Reg(0)],
			[Instruction(b'mne', [RegOperand(0)])])
	)
	for ts, res in pairs:
		assert p(ts) == res

def test_multiple_operands():
	assert (p([Ident(b'mne'), Reg(0), Comma(), Reg(1)])
		== [Instruction(b'mne', [RegOperand(0), RegOperand(1)])])

def test_labeldef():
	pairs = (
		([Ident(b'hello'), Colon()],
			[LabelDef(b'hello')]),
		([Ident(b'hello'), Colon(), Ident(b'world'), Colon()],
			[LabelDef(b'hello'), LabelDef(b'world')])
	)
	for ts, res in pairs:
		assert p(ts) == res

def test_labeldef_with_instruction():
	assert (p([Ident(b'hello'), Colon(), Ident(b'ins')])
		== [LabelDef(b'hello'), Instruction(b'ins', [])])
