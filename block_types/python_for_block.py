from .block_base import block_base
import math
from CompileError import CompileError, Pos

class python_for_block(block_base):
	def __init__(self, line, ids, val, sub):
		self.line = line
		self.ids = ids
		self.val = val
		self.sub = sub
		
	def compile(self, func):
		set = self.val.get_value(func)
		
		try:
			iter(set)
		except TypeError:
			raise CompileError(f'"{set}" in "for" block at line {self.line} is not an iterable set.', Pos(self.line)) from None

		for v in set:
			if len(self.ids) == 1:
				func.set_dollarid(self.ids[0], v)
			else:
				try:
					v_len = len(v)
				except Exception as e:
					raise CompileError(f'Set is not a tuple at line {self.line}', Pos(self.line)) from e
				if v_len != len(self.ids):
					raise CompileError(f'Expected {len(self.ids)} tuple items at line {self.line}, got {v_len}.', Pos(self.line))
				for idx in range(v_len):
					func.set_dollarid(self.ids[idx], v[idx])
			try:
				func.compile_blocks(self.sub)
			except CompileError as e:
				raise CompileError(f'Unable to compile python for block contents at line {self.line}', Pos(self.line)) from e
			except Exception as e:
				raise CompileError(f'Unable to compile python for block contents at line {self.line}', Pos(self.line)) from e
