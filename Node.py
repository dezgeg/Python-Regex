# encoding= utf-8
from CharSet import *
from Set import *
from Transition import *

def make_epsilon_closure(node, eclos):
	"Lisää solmujoukkoon 'eclos' solmun 'node' epsilon-sulkeuman, joka on niiden solmujen joukko, johon pääsee kys. solmusta käyttämällä pelkästään epsilon-siirtymiä"""
	if node in eclos:
		return
	eclos.add(node)
	for n in node.epsilon_transitions:
		make_epsilon_closure(n, eclos)
	return eclos

class Node:
	"""Node-luokka vastaa NFA:n tai DFA:n yhtä solmua"""
	def __init__(self):
		self.transitions = Map()
		self.epsilon_transitions = List() # Toisin kuin tavallisia deterministisiä siirtymiä, solmusta voi lähteä useita epsilonsiirtymiä
		self.accepting = False # Onko hyväksyvä tila. Ei käytetä NFA:n rakennus/jäsennysvaiheessa
		self.nfa_states = None # NFA-solmuille kerran laskettu solmun epsilon-sulkeumajoukko. DFA-solmuille sen sisältämien NFA-solmujen joukko
	def __str__(self):
		"""Muuntaa solmun merkkijonoksi debuggausta varten, mistä ilmenee sen id, sitä vastaavat nfa:n tilat, sekä siirtymät.
		 esim. 1234(4567,8910): a -> 4321, b -> 5678."""
		return str.format("{0}({1}): {2}", id(self), ','.join(str(id(x)) for x in self.nfa_states), 
			", ".join(str(x[0]) + " -> " + str(id(x[1])) for x in self.get_transitions()))
	def add_transition(self, c, dest):
		"""Lisää siirtymän syötemerkillä 'c' solmuun 'dest'. Arvolla c == None lisätää epsilon-siirtymä."""
		if c:
			self.transitions[c] = dest
		else:
			self.epsilon_transitions.insert(dest)
	def add_epsilon_transition(self, dest):
		"""Lisää epsilonsiirtymän solmuun 'dest'"""
		self.add_transition(None, dest)
	def get_epsilon_closure(self):
		"""Palauttaa solmun epsilon-sulkeuman"""
		if self.nfa_states == None:
			self.nfa_states = make_epsilon_closure(self, Set())
		return self.nfa_states
			
	def get_transitions(self):
		"""Palauttaa iteraattorin, joka käy läpi solmun kaikki siirtymät"""
		for n in self.transitions:
			yield n
		for dest in self.epsilon_transitions:
			yield [None, dest]
