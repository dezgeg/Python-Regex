#encoding= utf-8
class ListNode:
	def __init__(self, value, next):
		self.value = value
		self.next = next
class ListIterator:
	def __init__(self, node):
		self.node = node
	def __iter__(self):
		return self
	def next(self):
		if self.node == None:
			raise StopIteration()
		val = self.node.value
		self.node = self.node.next
		return val

class List:
	"""Yhteen suuntaan linkitetty lista. Listan pääasiallinen käyttö on Map:n hash-taulun ylivuotoketjuissa, joten operaatioiden tuottamien listojen järjestys on hassuhko"""
	def __init__(self, *contents):
		self.head = None
		for x in contents:
			self.insert(x)
	def insert(self, elem):
		"""Lisää listan alkuun alkion"""
		self.head = ListNode(elem, self.head)
	def __iter__(self):
		return ListIterator(self.head)
	def __iadd__(self, rhs):
		"""Operaattori +=, in-place konkatenaatio"""
		for x in rhs:
			self.insert(x)
		return self
	def __add__(self, rhs):
		"""Operaattori +, konkatenaatio, palauttaa uuden kopion"""
		lst = List()
		lst += self
		lst += rhs
		return lst
