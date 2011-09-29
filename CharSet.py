#encoding= utf-8
from Transition import *
from List import *

class CharSet:
	def __init__(self, contents = []):
		self.__set = set(contents)
	@classmethod
	def is_valid_char(cls, c):
		return c >= 'a' and c <= 'z' and len(c) == 1
	def add(self, item):
		"""Lisää merkin merkkijonojoukkoon"""
		if not CharSet.is_valid_char(item):
			raise ValueError('char not in range')
		self.__set.add(item)
		return self
	def add_range(self, c1, c2):
		"""Lisää merkkivälin [c1, c2] merkkijonojoukkoon"""
		if c2 < c1:
			raise ValueError('invalid range')
		if not CharSet.is_valid_char(c1) or not CharSet.is_valid_char(c2):
			raise ValueError('chars not in range')

		for c in xrange(ord(c1), 1 + ord(c2)):
			self.__set.add(chr(c))
		return self
	def negate(self):
		"""Komplementoi merkkijonojoukon aakkoston suhteen"""
		self.__set = CharSet.valid_chars - self.__set
		return self
	def contains(self, c):
		return c in self.__set
	@classmethod
	def singleton(cls, c):
		return CharSet().add(c)
	def __str__(self):
		if len(self.__set) == 1:
			return self.__set.copy().pop()
		else:
			return '[' + ''.join(self.__set) + ']'
	def to_transition_list(self, node):
		"""Palauttaa listan Transition-siirtymistä solmusta 'node' kaikille tämän joukon merkeille"""
		return List(*(Transition(node, x) for x in self.__set))
	valid_chars = set(chr(c) for c in xrange(ord('a'), 1 + ord('z')))
CharSet.any_char = CharSet(CharSet.valid_chars)
CharSet.empty = CharSet()
