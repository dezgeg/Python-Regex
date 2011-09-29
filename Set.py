#encoding= utf-8
from Map import *

class Set:
	"""Joukkotietorakenne, perustuu Map:iin. On joukko, eli saa olla vain yksi sama alkio, ei järjestystä"""
	def __init__(self, *contents):
		self.map = Map()
		for x in contents:
			self.add(x)
	def add(self, key):
		"""Lisää alkion, ei tee mitään jos oli jo olemassa sama"""
		existing = self.map[key]
		if existing == None:
			self.map[key] = key
	def __contains__(self, key):
		return key in self.map
	def __iter__(self):
		for (_, v) in self.map:
			yield v
	def __hash__(self):
		return hash(self.map)
	def __str__(self):
		return '[' + ', '.join(str(x) for x in self) + ']'
	def __eq__(self, other):
		try:
			return self.map == other.map
		except AttributeError:
			return False
