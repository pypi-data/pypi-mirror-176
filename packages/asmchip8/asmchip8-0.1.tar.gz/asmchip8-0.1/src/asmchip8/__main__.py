#!/usr/bin/env python3

import asmchip8 as asm
import getopt
import sys
from typing import NoReturn


USAGE = '''\
Usage: {} [-h] [-o <outpath>] [<long options>] [--] <inpath>

Options:
	-h, --help           Show this help message and quit.
	-o, --output <path>  Set the path of the output file.  If absent,
                             `{}' is used.
Mandatory arguments to long options are mandatory for short options too.\
'''
DEFAULT_OUTPATH = 'asmchip8.out'

def fail(msg: str, prefix: str = '') -> NoReturn:
	print(f'{prefix}Error: {msg}', file = sys.stderr)
	sys.exit(1)

def fail_asm(path: str, linum: int, data: str) -> NoReturn:
	fail(data, f'{path}:{linum}: ')

def parse_args() -> tuple[str, str]:
	try:
		opts, positional = getopt.gnu_getopt(sys.argv[1:],
			'ho:', ['help', 'output='])
	except getopt.GetoptError as e:
		fail(f"invalid option `{e.opt}'")

	outpath = DEFAULT_OUTPATH
	for o, v in opts:
		if o in ('-o', '--output'):
			outpath = v
		elif o in ('-h', '--help'):
			print(USAGE.format(sys.argv[0], DEFAULT_OUTPATH))
			sys.exit()

	try:
		inpath, *rest = positional
	except ValueError:
		fail('too few positional arguments, 1 expected.')
	if rest:
		fail('too many positional arguments, 1 expected.')
	return inpath, outpath

def main() -> int:
	inpath, outpath = parse_args()
	try:
		asm.assemble(inpath, outpath)
	except (FileNotFoundError, IsADirectoryError, PermissionError) as e:
		if e.filename == inpath:
			fail(f"unable to open `{e.filename}' for reading: {e.strerror}")
		if e.filename == outpath:
			fail(f"unable to open `{e.filename}' for writing: {e.strerror}")
		fail_asm(inpath, 0, f"unable to open `{e.filename}': {e.strerror}")
	except asm.LeftoverParseError as e:
		fail_asm(inpath, e.linum,
			'could not parse line: leftover tokens.')
	except asm.InvalidLabelError as e:
		fail_asm(inpath, e.linum,
			"undefined label: `{}'".format(e.name.decode()))
	except asm.InvalidDirectiveError as e:
		fail_asm(inpath, e.linum,
			"no such directive: `{}'".format(e.name.decode()))
	except asm.InvalidInsError as e:
		fail_asm(inpath, e.linum,
			"no such instruction: `{}'".format(e.name.decode()))
	except asm.InvalidOperandError as e:
		fail_asm(inpath, e.linum,
			"invalid operand for statement: `{}'"
			.format(e.name.decode()))
	except asm.MissingOperandError as e:
		fail_asm(inpath, e.linum,
			"missing operand for statement: `{}'"
			.format(e.name.decode()))
	except asm.LeftoverOperandError as e:
		fail_asm(inpath, e.linum,
			"too many operands for statement: `{}'"
			.format(e.name.decode()))
	except asm.PcTooLargeError as e:
		fail_asm(inpath, e.linum,
			'current instruction address too large to store, program too big.')
	return 0

if __name__ == '__main__':
	sys.exit(main())
