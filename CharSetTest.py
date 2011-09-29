from CharSet import *
import unittest

class CharSetTest(unittest.TestCase):
	def setUp(self):
		self.cs = CharSet()
	def test_add(self):
		self.cs.add('a')
		self.assertTrue(self.cs.contains('a'))
	def test_add_invalid(self):
		self.assertRaises(ValueError, self.cs.add, '-')
	def test_add_range(self):
		self.cs.add_range('a', 'c')
		for c in ['a', 'b', 'c']:
			self.assertTrue(self.cs.contains(c))
	def test_add_invalid_range(self):
		self.assertRaises(ValueError, self.cs.add_range, 'c', 'a')

if __name__ == '__main__':
	unittest.main()
