import sys
from Parser import *
from Debug import *
from Tester import *
from DfaMatcher import *

if len(sys.argv) < 3:
	print(str.format("usage: {0} <regex> <file>\n       {0} -t <testfile>", sys.argv[0]))
	sys.exit(1)
if sys.argv[1] == '-t':
	tester(sys.argv[2])
else:
	parser = Parser(sys.argv[1])
	nfa = parser.parse()
	matcher = DfaMatcher(nfa)
	file = open(sys.argv[2])
	
	for line in file:
		line = line.strip()
		if matcher.match(line):
			print line
