r'''Lexer.

For the sake of documentation, the language of each token is described below
with a regular expression:

	Comma      ::= ','
	Semicolon  ::= ';'
	Colon      ::= ':'
	IntLiteral ::= '0[Bb][01]+' | '0[Oo][0-7]+' |
	               '0[Xx][0-9A-Fa-f]+' | '[0-9]+'
	StrLiteral ::= '"[^"]*"'
	Reg        ::= '[Vv][0-9A-Fa-f]'
	Ident      ::= '[A-Za-z_.][0-9A-Za-z_.]*'
'''

from .token import (Token, Comma, Semicolon, Colon, IntLiteral, StrLiteral,
	Reg, Ident)
from typing import Any, Callable


_ALL_DIGITS = b'0123456789ABCDEF'

def get(bs: bytes, i: int) -> bytes:
	try:
		return bytes([bs[i]])
	except IndexError:
		return b''

def _int_literal_prefix(input: bytes) -> tuple[int, bytes]:
	'''Extract prefix of integer literal and determine the base.'''

	base = 10
	if get(input, 0) == b'0':
		match get(input, 1):
			case b'b' | b'B':
				input = input[2:]
				base = 2
			case b'o' | b'O':
				input = input[2:]
				base = 8
			case b'x' | b'X':
				input = input[2:]
				base = 16
	return base, input

def int_literal(input: bytes) -> None|tuple[Token, bytes]:
	'''Try to get an integer literal token.'''

	base, input = _int_literal_prefix(input)

	digits = _ALL_DIGITS[:base]
	i = 0
	while (c := get(input, i).upper()) and c in digits:
		i += 1
	if i == 0:
		return None
	s = input[:i]
	return IntLiteral(int(s, base)), input[i:]

def _is_control(c: bytes) -> bool:
	'''Check whether a byte character is a UTF-8 control character.'''
	n = ord(c)
	return n in range(0x20) or n == 0x7F or n in range(0x80, 0xA0)

def str_literal(input: bytes) -> None|tuple[Token, bytes]:
	r'''Try to get a string literal token.

	Two simple escape sequences are available: `\"` for a literal double
	quote (`"`) and `\\` for a literal backslash (`\`).  Any other escape
	sequence produces an error.

	For safety, neither raw UTF-8 control characters nor other escape
	sequences are allowed.  If present, the token is invalidated.
	'''
	if get(input, 0) != b'"':
		return None
	i = 1
	cs = []
	while (c := get(input, i)) and c != b'"':
		i += 1
		# Disallow control characters.
		if _is_control(c):
			return None
		# Allow only the simplest escapes.
		if c == b'\\':
			d = get(input, i)
			i += 1
			match d:
				case b'"':  e = b'"'
				case b'\\': e = b'\\'
				case _:     return None
			cs.append(e)
		else:
			cs.append(c)
	if not c:
		return None
	s = b''.join(cs)
	return StrLiteral(s), input[i + 1:]

def reg(input: bytes) -> None|tuple[Token, bytes]:
	'''Try to take a register token.'''

	if not (c := get(input, 0)) or c not in b'vV':
		return None
	v = get(input, 1)
	if v.upper() not in _ALL_DIGITS:
		return None
	return Reg(int(v, 16)), input[2:]

def ident(input: bytes) -> None|tuple[Token, bytes]:
	'''Try to take an identifier token.'''

	EXTRA_CHARS = (b'_', b'.')
	if not (c := get(input, 0)).isalpha() and c not in EXTRA_CHARS:
		return None
	i = 1
	while (c := get(input, i)).isalnum() or c in EXTRA_CHARS:
		i += 1
	s = input[:i]
	return Ident(s), input[i:]

def any_lexer(*lxs) -> Callable[..., Any]:
	def f(input: bytes) -> None|tuple[Token, bytes]:
		for lx in lxs:
			if res := lx(input):
				return res
		return None
	return f

def punctuation_lexer(t: type, char: bytes) -> Callable[..., Any]:
	def f(input: bytes) -> None|tuple[Token, bytes]:
		if get(input, 0) != char:
			return None
		return t(), input[1:]
	return f

comma       = punctuation_lexer(Comma,     b',')
semicolon   = punctuation_lexer(Semicolon, b';')
colon       = punctuation_lexer(Colon,     b':')
punctuation = any_lexer(comma, semicolon, colon)
token       = any_lexer(punctuation, int_literal, str_literal, reg, ident)

def space(input: bytes) -> bytes:
	i = 0
	while get(input, i).isspace():
		i += 1
	return input[i:]

def comment(input: bytes) -> bytes:
	if get(input, 0) != b'#':
		return input
	i = 1
	while get(input, i) not in b'\n':
		i += 1
	return input[i:]

def _next_token(input: bytes) -> None|tuple[Token, bytes]:
	return token(comment(space(input)))

def lex(input: bytes) -> list[Token]:
	tokens = []
	while res := _next_token(input):
		t, input = res
		tokens.append(t)
	return tokens
