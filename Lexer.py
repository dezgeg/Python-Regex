# coding= utf-8

from CharSet import *


class ParseError(Exception):
	def __init__(self, str):
		self.__str = str
	def __str__(self):
		return repr(self.__str)

class Lexer:
	def __init__(self, str):
		self.__string = str
		self.__index = 0
	def next_char(self, none_on_error = False):
		"""Lukee syötemerkin puskurista, ja siirtyy seuraavaan merkkiin. Toisen parametrin mukaan joko heitetään poikkeus tai palautetaan None"""
		if self.__index >= len(self.__string):
			if none_on_error:
				return None
			else:
				raise ParseError("Unexpected end of expression")
		c = self.__string[self.__index]
		self.__index += 1
		return c
	def peek_char(self):
		"""Palauttaa puskurissa olevan syötemerkin, mutta ei siirry seuraavaan merkkiin."""
		if self.__index >= len(self.__string):
			raise ParseError("Unexpected end of expression")
		return self.__string[self.__index]
	def next_token(self):
		"""Palauttaa seuraavan tekstialkion syötteestä.
		Tekstialkioita kuvaa pääosin yhden merkin pituinen merkkiä vastaava merkkijono, mutta merkkiluokat, ., ja yksittäiset merkit palautetaan CharSet-olioina"""
		c = self.next_char(True)
		if c == None:
			return '<EOF>'
		elif c == '.':
			return CharSet.any_char
		elif c == '[':
			return self.__read_charset()
		elif c >= 'a' and c <= 'z':
			return CharSet.singleton(c)
		else:
			return c
	def __read_charset(self):
		"""Lukee syötteestä merkkijoukon ja palauttaa sen, kun merkkijoukon avaava '[' on luettu ennen tämän funktion kutsua"""
		c = self.next_char()
		negated = False
		charset = CharSet()

		if c == '^':
			negated = True
			c = self.next_char()
		
		while c != ']':
			self.check_allowed_char(c)
			c2 = self.peek_char()
			if c2 == '-': # character range
				self.next_char() # eat -
				c2 = self.next_char()
				self.check_allowed_char(c2)
				charset.add_range(c, c2)
			else:
				charset.add(c)
			c = self.next_char()
		if negated:
			charset.negate()
		return charset
	"""Heittää poikkeuksen jos merkki ei kuulu aakkostoon"""
	def check_allowed_char(self, c):
		if c < 'a' or c > 'z':
			raise ParseError(str.format("Character '{0}' not in alphabet", c))
	
