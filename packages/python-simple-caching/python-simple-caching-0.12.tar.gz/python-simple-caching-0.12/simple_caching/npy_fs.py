import os
import numpy as np
import random
import string
from overrides import overrides
from pathlib import Path
from typing import Any
from .cache import Cache

class NpyFS(Cache):
	def __init__(self, baseDirectory=None):
		if baseDirectory is None:
			Str = "".join(random.choices(string.printable, k=10))
			baseDirectory = ".cache/%s" % Str

		self.cacheDir = Path(os.path.abspath(os.path.realpath(baseDirectory)))
		self.cacheDir.mkdir(exist_ok=True, parents=True)
		print("[NpyFS] Cache dir: %s" % str(self.cacheDir))

	@overrides
	def get(self, key:str) -> np.ndarray:
		if not key.endswith(".npy"):
			key = "%s.npy" % key
		cacheFile = Path("%s/%s" % (str(self.cacheDir), key))

		item = np.load(cacheFile, allow_pickle=True)
		try:
			item = item.item()
		except Exception:
			pass
		return item

	@overrides
	def check(self, key:str) -> bool:
		if not key.endswith(".npy"):
			key = "%s.npy" % key
		cacheFile = Path("%s/%s" % (str(self.cacheDir), key))
		return cacheFile.exists() and cacheFile.is_file()
	
	@overrides
	def set(self, key:str, value:np.ndarray):
		if not key.endswith(".npy"):
			key = "%s.npy" % key
		cacheFile = Path("%s/%s" % (str(self.cacheDir), key))
		cacheFile.parent.mkdir(exist_ok=True, parents=True)
		np.save(cacheFile, value)

	def __str__(self) -> str:
		Str = "[NpyFS]"
		Str += "\n  - Cache directory: %s" % str(self.cacheDir)
		return Str