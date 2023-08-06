'''Test resulting output files against expected output.'''

from asmchip8.asm import assemble_streams
from collections.abc import Iterable
import os
import tempfile


DIRPATH    = 'tests/full'
IN_SUFFIX  = '.s'
OUT_SUFFIX = '.out'

def entry_to_paths(e: str) -> tuple[str, str]:
	inpath = os.path.join(DIRPATH, e)
	outpath = inpath.removesuffix(IN_SUFFIX) + OUT_SUFFIX
	return inpath, outpath

def fetch_paths() -> Iterable[tuple[str, str]]:
	for e in os.listdir(DIRPATH):
		if not e.endswith(IN_SUFFIX):
			continue
		yield entry_to_paths(e)

def write_outf(outf, inpath):
	with open(inpath, 'rb') as inf:
		assemble_streams(inf, outf)

def cmp_outf(outf, otherpath):
	with open(otherpath, 'rb') as otherf:
		return outf.read() == otherf.read()

def test_full():
	with tempfile.TemporaryFile() as tmp_outf:
		for inpath, outpath in fetch_paths():
			write_outf(tmp_outf, inpath)
			tmp_outf.seek(0)
			assert cmp_outf(tmp_outf, outpath)
			tmp_outf.seek(0)
			tmp_outf.truncate()
