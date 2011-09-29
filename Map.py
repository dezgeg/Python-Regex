#encoding= utf-8
from List import *

class Map:
	"""Map on assosiatiivinen taulukko, toteutettu yksinkertaisella hajautustauluilla"""
	HASH_SIZE = 13
	def __init__(self):
		self.buckets = list(None for _ in range(Map.HASH_SIZE))
		self.hashval = 0 # cachettaa alkioiden hash-arvoja
	def get_bucket(self, obj):
		"""Private - palauttaa hashattavan olion paikan hajautustaulussa"""
		return hash(obj) % Map.HASH_SIZE
	def __setitem__(self, key, value):
		"""a[b] = c -- lisää taulukkoon/vaihtaa olemassaolevia arvoja"""
		self.hashval ^= hash(key)

		bucket = self.get_bucket(key)
		if self.buckets[bucket] == None:
			self.buckets[bucket] = List()
		collist = self.buckets[bucket]

		for kvpair in collist:
			if kvpair[0] == key:
				self.hashval ^= hash(kvpair[0])
				kvpair[1] = value
				return
		collist.insert([key, value])

	def __getitem__(self, key):
		"""a[b] -- palauttaa arvon taulukosta. Palauttaa None jos ei löydy."""
		collist = self.buckets[self.get_bucket(key)]
		if collist == None:
			return None
		for kvpair in collist:
			if kvpair[0] == key:
				return kvpair[1]
		return None
	def __iter__(self):
		"""Palauttaa iteraattorin, joka käy [avain, arvo]-taulukkoparit läpi mielivaltaisessa järjestyksessä"""
		for bucket in self.buckets:
			if bucket:
				for x in bucket:
					yield x
	def __contains__(self, key):
		"""a in b palauttaa True joss b:ssä on arvo avaimella a"""
		return self[key] != None
	def __hash__(self):
		return self.hashval
	def __eq__(self, other):
		for (n1, n2) in map(None, self, other):
			if n1 != n2:
				return False
		return True
