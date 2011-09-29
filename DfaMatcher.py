#encoding= utf-8
from Map import *
from Node import *

class DfaMatcher:
	"""Tunnistaa NFA:n tunnistamia merkkijonoja luomalla laiskasti NFA:sta DFA merkkijonon tunnistuksen yhteydessä"""
	def __init__(self, first):
		self.cache = Map()
		self.start_node = self.get_dfa_node(first.get_epsilon_closure())
	def match(self, str):
		"""Palauttaa True joss NFA tunnistaa merkkijonon str, ja False jos ei."""
		state = self.start_node
		for c in str:
			state = self.step_state(state, c)
			if state == False:
				return False
		return state != False and state.accepting
	def step_state(self, state, c):
		"""Palauttaa DFA-tilan, johon päästään kulkemalla DFA-tilasta 'state' merkillä 'c'"""
		if c in state.transitions:
			return state.transitions[c]
				
		nodeset = Set()
		for nfa_state in state.nfa_states:
			if c in nfa_state.transitions:
				dest_node = nfa_state.transitions[c]
				if dest_node:
					for dest_ec_node in dest_node.get_epsilon_closure():
						nodeset.add(dest_ec_node)

		dfa_node = self.get_dfa_node(nodeset)
		state.add_transition(c, dfa_node)
		return dfa_node
	def get_dfa_node(self, nodeset):
		"""Palauttaa sen DFA-tilan, joka vastaa kyseistä NFA-tilajoukkoa 'nodeset'"""
		if nodeset in self.cache:
			return self.cache[nodeset]

		node = Node()
		node.nfa_states = nodeset
		for n in nodeset:
			if n.accepting:
				node.accepting = True
				break
		self.cache[nodeset] = node
		return node
			
