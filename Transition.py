#encoding= utf-8

class Transition:
	"""'Irrallinen' siirtymä NFA:n tilojen välillä, jossa lähtösolmu sekä siirtymämerkki ovat tiedossa, mutta kohdesolmu ei toistaiseksi ole tiedossa.
	Jäsennysvaiheessa NFA:n hyväksyvistä tiloista pidetään kirjaa näiden avulla"""
	def __init__(self, node, c):
		self.char = c
		self.source = node
	def attach_destination(self, dest):
		"""'Kytkee' siirtymän kohdesolmuun 'dest'"""
		self.source.add_transition(self.char, dest)
