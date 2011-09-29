#encoding= utf-8
from Node import *
from Set import *

def print_dfa(first):
	"""Tulostaa NFA:n debuggausta varten"""
	print("First state: " + str(id(first)))

	visit(first, Set())
def visit(node, seen):
	"""Tulostaa yhden NFA-solmun, ja rekursiivisesti kaikki siitä saavutettavissa olevat solmut"""
	if node in seen:
		return
	seen.add(node)
	print node
	for x in node.get_transitions():
		visit(x[1], seen)
