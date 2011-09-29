# encoding= utf-8
from Lexer import *
from CharSet import *
from Node import *
from Transition import *
import sys

class Parser:

# Säännöllisten lausekkeiden syntaksi on seuraava:
# regex -> alt EOF
# alt -> concat alt_tail*
# alt_tail -> '' | '|' concat alt_tail
# concat -> quant concat_tail
# concat_tail -> '' | quant concat_tail
# quant -> paren quant_tail
# quant_tail -> '?' | '+' | '*' | ''
# paren -> '(' alt ')' | lit

# toteutus perstuntumalta käsin koodattu LL-parseri suurinpiirtein tämän mukaisesti: https://www.cs.helsinki.fi/i/vihavain/k10/okk/content3.html
# Parserin sisällä NFA:t kulkevat parina (first, out_transitions), missä first on alkutila, ja out_transitions on List()a Transition-olioista, josta kulkemalla pääsee hyväksyvään tilaan
# Jäsentämisen jälkeen hyväksyvistä tiloista pidetään kirjaa solmujen accepting-attribuutin avulla
################ kielen produktiot #############
	def regex(self):
		(first, accept_transitions) = self.alt()
	        accepting_state = Node()
		accepting_state.accepting = True
		for x in accept_transitions:
			x.attach_destination(accepting_state)

		self.assert_match("<EOF>")
		return first
	def alt(self):
		(first, transitions) = self.concat()
		branch_node = None

		# alt_tail
		while self.match('|'):
			(second, snd_transitions) = self.concat()
			if branch_node == None:
				branch_node = Node()
				branch_node.add_epsilon_transition(first)
			branch_node.add_epsilon_transition(second)
			transitions += snd_transitions
			self.append_postfix('|')
		if branch_node == None:
			return (first, transitions)
		else:
			return (branch_node, transitions)
	def concat(self):
		(first, transitions) = self.quant()
		
		while self.quant_matches():
			(second, second_transitions) = self.quant()
			for tr in transitions:
				tr.attach_destination(second)
			transitions = second_transitions
			self.append_postfix('#')
		return (first, transitions)
	def quant(self):
		(first, transitions) = self.paren()

		# quant_tail
		res = self.match('+', '?', '*')
		if res:
			self.append_postfix(res)
			if res == '*':
				loop_node = Node()
				for n in transitions:
					n.attach_destination(loop_node)
				loop_node.add_epsilon_transition(first)
				transition = Transition(loop_node, None)
				return (loop_node, List(transition))
			elif res == '+':
				loop_node = Node()
				for tr in transitions:
					tr.attach_destination(loop_node)
				loop_node.add_epsilon_transition(first)
				out_transition = Transition(loop_node, None)
				return (first, List(out_transition))
			elif res == '?':
				skip_node = Node()
				skip_node.add_epsilon_transition(first)
				return (skip_node, transitions + List(Transition(skip_node, None)))
		return (first, transitions)
	def quant_matches(self):
		return self.__token == '(' or isinstance(self.__token, CharSet)
	def paren(self):
		ret = None
		if self.match('('):
			ret = self.alt()
			self.assert_match(')')
		else:
			ret = self.lit()
		return ret
	def lit(self):
		token = self.advance()
		if isinstance(token, CharSet):
			self.append_postfix(token)
			first = Node()
			
			return (first, token.to_transition_list(first))
		raise ParseError('Unexpected input: ' + str(token))
############# luokan varsinaiset metodit #####
	def match(self, *lits):
		"""Tarkistaa, onko seuraavana syötteessä oleva tekstialkio jokin parametrina annetuista.
		Palauttaa sen ja siirtyy eteenpäin syötteessä jos on, palauttaa False muuten"""
		if self.__token in lits:
			old_token = self.advance()
			return old_token
		return False
	
	def assert_match(self, *lits):
		"""Sama kuin match(), mutta heittää fataalin poikkeuksen mikäli seuraava tekstialkio ei vastaa jotain parametrinä annetuista"""
		if self.match(*lits) is False:
			raise ParseError('Unexpected `' + str(self.__token) + "', expecting one of " + ", ".join(lits))
	def advance(self):
		"""Palauttaa nykyisen tekstialkion ja siirtyy eteenpäin syötteessä"""
		old_token = self.__token
		self.__token = self.__lexer.next_token()
		return old_token
	def __init__(self, str):
		self.__lexer = Lexer(str)
		self.__token = self.__lexer.next_token()
		self.postfix = ''

	def append_postfix(self, c):
		"""Lisää merkki postfix-sivutuotteeseen"""
		self.postfix += str(c)
	def parse(self):
		"""Jäsentää konstruktorissa annetun lausekkeen, ja palauttaa viitteen NFA:n alkutilaan"""
		return self.regex()
