#encoding= utf-8
from Parser import *
from DfaMatcher import *

def tester(testfile):
	"""Ajaa kaikki annetun testitiedoston testit, ja tulostaa virheilmon epäonnistuneista testeistä"""
	skipped_lines = 0
	total_lines = 0
	failed_tests = 0

	file = open(testfile, 'r')
	matcher = None
	regexstr = None
	for line in file:
		total_lines += 1
		arg = line[1:].strip()
		if line[0] == '=': # vaihdetaan käytettävää regexpiä
			(regexstr, expected_postfix) = arg.split('=')

			try:
				parser = Parser(regexstr)
				matcher = DfaMatcher(parser.parse())
			except Exception as e:
				print(str.format("Parsing /{0}/ failed unexpectedly: {1}", regexstr, str(e)))
				failed_tests += 1
				continue
			if expected_postfix != '' and parser.postfix != expected_postfix:
				print(str.format("Parsing regex '{0}' failed: expected postfix '{1}', got '{2}'", regexstr, expected_postfix, parser.postfix))
				failed_tests += 1
		elif line[0] == '+' or line[0] == '-': # koitetaan tunnistaa annettu merkkijono nykyisellä regexpillä
			expected = line[0] == '+'
			if expected != bool(matcher.match(arg)):
				print(str.format("Matching '{0}' against /{1}/ caused unexpected result '{2}' instead of '{3}'", arg, regexstr, expected, not expected))
				failed_tests += 1
		else:
			skipped_lines += 1
	total_tests = total_lines - skipped_lines
	print(str.format("{0}/{1} tests passed.", total_tests - failed_tests, total_tests))
