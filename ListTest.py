from List import *
import unittest

class ListTest(unittest.TestCase):
	def setUp(self):
		self.list = List()
	def testInsert(self):
		self.list.insert(42)
		self.list.insert(1337)
		self.assertEquals(list(self.list), [1337, 42])
	def test__iadd__(self):
		self.list.insert(2)
		self.list.insert(1)

		list2 = List()
		list2.insert(4)
		list2.insert(3)

		self.list += list2
		self.assertEquals(sorted(list(self.list)), [1,2,3,4])
	def test__add__(self):
		self.assertEquals(sorted(list(List(1,2) + List(3,4))), [1,2,3,4])
if __name__ == '__main__':
	unittest.main()
