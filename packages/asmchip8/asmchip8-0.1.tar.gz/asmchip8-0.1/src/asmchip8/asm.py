from .labeldef import LabelDef
from .parser import parse_file
from .translator import translate_stmt, START_ADDRESS
from typing import BinaryIO


def assemble_streams(inf: BinaryIO, outf: BinaryIO) -> bool:
	offset = START_ADDRESS
	labels = {}
	for obj in parse_file(inf):
		if isinstance(obj, LabelDef):
			labels[obj.s] = offset
			continue

		mcode = translate_stmt(obj, offset, labels)
		outf.write(mcode)
		offset += len(mcode)
	return True

def assemble(inpath: str, outpath: str) -> bool:
	with open(inpath, 'rb') as inf, open(outpath, 'wb') as outf:
		return assemble_streams(inf, outf)
