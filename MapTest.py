from Map import *
import unittest

class MapTest(unittest.TestCase):
	def setUp(self):
		self.map = Map()
	def testGetNonexistent(self):
		self.assertEquals(None, self.map['foo'])
	def testInsert(self):
		self.map['foo'] = 'bar'
		self.assertEquals(self.map['foo'], 'bar')
	def testModify(self):
		self.map['foo'] = 'bar'
		self.map['foo'] = 'baz'
		self.assertEquals(self.map['foo'], 'baz')
	def testIterator(self):
		self.map['a'] = 1
		self.map['b'] = 2
		self.map['c'] = 3
		self.assertEquals(list(sorted(self.map)), [['a', 1], ['b', 2], ['c', 3]])

if __name__ == '__main__':
	unittest.main()
