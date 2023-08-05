import numpy as np
from abc import abstractmethod, ABC

class Cache(ABC):
	@abstractmethod
	def set(self, key:str, value:np.ndarray):
		pass
	
	@abstractmethod
	def get(self, key:str) -> np.ndarray:
		pass
	
	@abstractmethod
	def check(self, key:str) -> bool:
		pass