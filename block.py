class Block():

	def __init__(self, block):
		self.block = block
		if self.block == 'A':
			self.reflect = False
			self.refract = True
		if self.block == 'B':
			self.reflect = False
			self.refract = False
		if self.block == 'C':
			self.reflect = True
			self.refract = True
