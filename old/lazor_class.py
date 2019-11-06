class Lazor(object):
	'''
	The lazor class that determines lazor attributes:
		position (inBoard)
		movement
		reflection
		refraction
	'''
	def __init__(self, x, y, vx, vy, initialcoordinates,
			movementcoordinates):
		# is it better to have:
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		# or:
		self.ixy = initialcoordinates
		self.vxy = movementcoordinates

	def inBoard(self, board):
		'''
		Checks whether or not the lazor is actually on the board.

		**Parameters**

			board: *list, list, tuple*
				List of list of board coordinates in tuples??
			x: *int*
				x-coordinate of lazor
			y: *int*
				y-coordinate of lazor
		'''
		if self.x >= 0 and self.x < len(board[0]):
			if self.y>= 0 and self.y < len(board):
				return True

	def movement(self):
		'''
		Increments the lazor 'final' position.
		'''
		self.x += self.vx
		self.y += self.vy


	def reflect(self, block):
		'''
		Handles the action of a lazor hitting a reflect block.
		'''
		dx = [0, 0, 1, -1]
		dy = [1, -1, 0, 0]
		for i in range(4):
			pass
		pass

	def refract(self):
		'''
		Handles the action of a lazor hitting a refract block.
		'''
		pass

	def hitTarget(self, board):
		'''
		Handles the action of a lazor hitting the target.
		'''
		return path[-1] == board.target
		

	def path(self, board, path=[]):
		'''
		Uses the above functions to outline the path of the
		lazor

		**Parameters**

		**Returns**

			path: *list, list, tuples*
				a list of lists of lazor coordinates that
				correspond to the path the lazor takes
		'''
		path = []
		path.append((self.x, self.y))
		while True:
			# if 'o' or 'x':
				# move normally
			if board(self.x, self.y) == 'o' or 'x':
				path.append(move((self.x, self.y)))
			else:
				continue
			# if 'A'
				# reflect, i.e. change direction of path depending
				# on face of block encountered
			if board(self.x, self.y) == 'A':
				path.append(reflect((self.x, self.y)))
			else:
				continue
			# if 'B'
				# opaque, stop lazor path right there at that
				# coordinate
			if board(self.x, self.y) == 'B':
				break
			else:
				continue
			# if 'C'
				# refract, i.e. split path at that coordinate
				# and have one change direction based off of
				# face encountered and have one continue in the same
				# direction. That is, refract = move + reflect
			if board(self.x, self.y) == 'C':
				path.append(move((self.x, self.y)))
				path.append(reflect((self.x, self.y)))
			else:
				continue
		return path


if __name__ == '__main__':
	test = Lazor(10, 11, 1, 1, (10, 11), (11, 12))
	# print(test.path())
