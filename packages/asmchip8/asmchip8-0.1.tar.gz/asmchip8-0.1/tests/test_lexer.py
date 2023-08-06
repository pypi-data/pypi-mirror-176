'''Unit tests for lexer.'''

from asmchip8.lexer import lex
from asmchip8.token import (Comma, Semicolon, Colon, IntLiteral, StrLiteral,
	Reg, Ident)


def test_blank():
	assert lex(b'') == []

def test_whitespace():
	ss = (
		b' ',
		b'\t',
		b'\n',
		b'\r',
		b'\v',
		b'  ',
		b' \t',
		b'\t ',
		b'\n\n',
		b'\r\n'
	)
	for s in ss:
		assert lex(s) == []

def test_comment():
	ss = (
		b'#',
		b' #',
		b'# ',
		b'#hello',
		b'#hello\nworld'
	)
	for s in ss:
		assert lex(s) == []

def test_punctuation():
	assert lex(b',') == [Comma()]
	assert lex(b';') == [Semicolon()]
	assert lex(b':') == [Colon()]
	assert lex(b';;') == [Semicolon(), Semicolon()]

def test_int_literal0():
	assert lex(b'0') == [IntLiteral(0)]
	assert lex(b'00') == [IntLiteral(0)]

def test_int_literal_bases():
	ss = (
		b'0b10101',
		b'0B10101',
		b'0o25',
		b'0O25',
		b'0x15',
		b'0X15',
		b'21'
	)
	for s in ss:
		assert lex(s) == [IntLiteral(21)]

def test_str_literal_verbatim():
	assert lex(b'""')    == [StrLiteral(b'')]
	assert lex(b'"foo"') == [StrLiteral(b'foo')]

def test_str_literal_valid_escapes():
	assert lex(b'"\\""')      == [StrLiteral(b'"')]
	assert lex(b'"\\\\"')     == [StrLiteral(b'\\')]
	assert lex(b'"\\"\\""')   == [StrLiteral(b'""')]
	assert lex(b'"\\"\\\\"')  == [StrLiteral(b'"\\')]
	assert lex(b'"\\\\\\""')  == [StrLiteral(b'\\"')]
	assert lex(b'"\\\\\\\\"') == [StrLiteral(b'\\\\')]

def test_str_literal_invalid_escapes():
	ss = (
		b'"\\0"',
		b'"\\a"',
		b'"\\b"',
		b'"\\e"',
		b'"\\f"',
		b'"\\n"',
		b'"\\r"',
		b'"\\t"',
		b'"\\v"',
		b'"\\\'"',
		b'"\\?"',
		b'"\\052"',
		b'"\\x2A"',
		b'"\\x2a"',
		b'"\\u002A"',
		b'"\\u002a"',
		b'"\\U0000002A"',
		b'"\\U0000002a"'
	)
	for s in ss:
		assert lex(s) == []

def test_reg():
	for c in '0123456789ABCDEFabcdef':
		n = int(c, 16)
		assert lex(b'v' + c.encode()) == [Reg(n)]
		assert lex(b'V' + c.encode()) == [Reg(n)]

def test_ident():
	ss = (
		b'_',
		b'.',
		b'a',
		b'A',
		b'__',
		b'_.',
		b'_a',
		b'_A',
		b'_0',
		b'._',
		b'..',
		b'.a',
		b'.A',
		b'.0',
		b'a_',
		b'a.',
		b'aa',
		b'aA',
		b'a0',
		b'A_',
		b'A.',
		b'Aa',
		b'AA',
		b'A0',
		b'b0d',
		b'bcd'
	)
	for s in ss:
		assert lex(s) == [Ident(s)]

def test_multi():
	assert lex(b'zero:one;two;;three four,5,0o6.') == [
		Ident(b'zero'), Colon(),
		Ident(b'one'), Semicolon(),
		Ident(b'two'), Semicolon(), Semicolon(),
		Ident(b'three'), Ident(b'four'), Comma(),
		IntLiteral(5), Comma(), IntLiteral(6), Ident(b'.')
	]
