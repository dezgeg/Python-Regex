from Set import *
import unittest

class SetTest(unittest.TestCase):
	def setUp(self):
		self.set = Set()
	def testInsert(self):
		self.set.add('foo')
		self.assertTrue('foo' in self.set)
	def testIterator(self):
		self.set.add('a')
		self.set.add('b')
		self.set.add('c')
		self.assertEquals(list(sorted(self.set)), ['a', 'b', 'c'])

if __name__ == '__main__':
	unittest.main()
