import numpy as np
from overrides import overrides
from pathlib import Path
from typing import Any
from .cache import Cache

class DictMemory(Cache):
	def __init__(self):
		self.cache = {}

	@overrides
	def get(self, key:str) -> np.ndarray:
		key = key.split("/")
		item = self.cache
		for i in range(len(key)):
			item = item[key[i]]
		return item

	@overrides
	def check(self, key:str) -> bool:
		key = key.split("/")
		item = self.cache
		for i in range(len(key)):
			if not key[i] in item:
				return False
			item = item[key[i]]
		return True
	
	@overrides
	def set(self, key:str, value:np.ndarray):
		key = key.split("/")
		item = self.cache
		for i in range(len(key) - 1):
			if not key[i] in item:
				item[key[i]] = {}
			item = item[key[i]]
		item[key[-1]] = value

	def __str__(self) -> str:
		Str = "[DictMemory]"
		Str += "\n  - Num top level keys: %d" % len(self.cache.keys())
		return Str