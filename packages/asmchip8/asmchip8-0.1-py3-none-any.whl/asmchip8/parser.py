'''Parser.

The grammar accepted by the parser:

    start     ::= line+
    line      ::= labeldef* stmts
    labeldef  ::= IDENT DOT
    stmts     ::= stmt? (SEMICOLON stmt?)*
    stmt      ::= IDENT operands?
    operands  ::= operand (COMMA operands)?
    operand   ::= REG | IDENT | INTLITERAL | STRLITERAL
'''

from .assemblyerror import AssemblyError
#from directive import Directive
from .labeldef import LabelDef
from .operand import (Operand, CurAddrOperand, ImmOperand, LabelOperand,
	RegOperand, StrOperand)
from .statement import Statement, Directive, Instruction
from .token import Token
from . import lexer
from . import token as t
from collections.abc import Iterable
from typing import Any, BinaryIO


DIRECTIVE_PREFIX = b'.'
CURADDR_LABEL = b'.'

class LeftoverParseError(AssemblyError):
	pass

def get(ts: list[Token], i: int) -> None|Token:
	try:
		return ts[i]
	except IndexError:
		return None

def token_parser(t: type):
	def f(ts: list[Token]) -> None|tuple[Token, list[Token]]:
		u = get(ts, 0)
		if not isinstance(u, t):
			return None
		return u, ts[1:]
	return f

def opt(parser, default):
	def f(ts: list[Token]) -> None|tuple[list[Any], list[Token]]:
		return parser(ts) or (default, ts)
	return f

def seq(*parsers):
	def f(ts: list[Token]) -> None|tuple[list[Any], list[Token]]:
		objs = []
		for p in parsers:
			if not (res := p(ts)):
				return None
			obj, ts = res
			objs.append(obj)
		return objs, ts
	return f

def zeroormore(parser):
	def f(ts: list[Token]) -> None|tuple[list[Any], list[Token]]:
		objs = []
		while res := parser(ts):
			obj, ts = res
			objs.append(obj)
		return objs, ts
	return f

def oneormore(parser):
	def f(ts: list[Token]) -> None|tuple[list[Any], list[Token]]:
		objs, ts = zeroormore(parser)(ts)
		return (objs, ts) if objs else None
	return f

comma     = token_parser(t.Comma)
semicolon = token_parser(t.Semicolon)
colon     = token_parser(t.Colon)
ident     = token_parser(t.Ident)

def labeldef(ts: list[Token]) -> None|tuple[LabelDef, list[Token]]:
	if not (res := seq(ident, colon)(ts)):
		return None
	objs, ts = res
	return LabelDef(objs[0].d), ts

def _operand_from_token(op: Token|None) -> Operand|None:
	if isinstance(op, t.IntLiteral):
		return ImmOperand(op.d)
	elif isinstance(op, t.StrLiteral):
		return StrOperand(op.d)
	elif isinstance(op, t.Reg):
		return RegOperand(op.d)
	elif isinstance(op, t.Ident):
		if op.d == CURADDR_LABEL:
			return CurAddrOperand()
		else:
			return LabelOperand(op.d)
	else:
		return None

def operand(ts: list[Token]) -> None|tuple[Operand, list[Token]]:
	t = get(ts, 0)
	op = _operand_from_token(t)
	return (op, ts[1:]) if op else None

def operands(ts: list[Token]) -> None|tuple[list[Operand], list[Token]]:
	if not (res := seq(operand, zeroormore(seq(comma, operand)))(ts)):
		return None
	ops, ts = res
	ops = [ops[0]] + [b for a in ops[1] for b in a]
	ops = [op for op in ops if not isinstance(op, t.Comma)]
	return ops, ts

def _statement_from_mnemonic(mnem: t.Ident,
		opers: list[Operand]) -> Statement:
	if mnem.d.startswith(DIRECTIVE_PREFIX):
		return Directive(mnem.d[len(DIRECTIVE_PREFIX):], opers)
	else:
		return Instruction(mnem.d, opers)

def statement(ts: list[Token]) -> None|tuple[Statement, list[Token]]:
	if not (res := seq(ident, opt(operands, []))(ts)):
		return None
	[mnemonic, opers], ts = res
	st = _statement_from_mnemonic(mnemonic, opers)
	return st, ts

def statements(ts: list[Token]) -> None|tuple[list[Statement], list[Token]]:
	(pairs, last), ts = seq(
		zeroormore(seq(opt(statement, None), semicolon)),
		opt(statement, None)
	)(ts)
	objs = [o[0] for o in pairs if o[0]]
	if last:
		objs.append(last)
	return objs, ts

def parse_tokens(ts: list[Token], linum: int) -> Iterable[LabelDef|Statement]:
	while ldres := labeldef(ts):
		lb, ts = ldres
		lb.linum = linum
		yield lb
	if stres := statements(ts):
		stmts, ts = stres
		for st in stmts:
			st.linum = linum
			yield st
	if ts:
		raise LeftoverParseError(linum, ts)

def parse(bs: bytes, linum: int) -> Iterable[LabelDef|Statement]:
	return parse_tokens(lexer.lex(bs), linum)

def parse_file(input: BinaryIO) -> Iterable[LabelDef|Statement]:
	for linum, l in enumerate(input.readlines(), 1):
		for a in parse(l, linum):
			yield a
