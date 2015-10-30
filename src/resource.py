from copy import deepcopy, copy
from itertools import repeat, chain
import os


class Move:
	action = ['flip', 'place', 'none']

	def __init__(self, action='none', player=-1, column=-1):
		self._action = action
		self._player = player
		self._column = column

	def toTupple(self):
		return (self._player, self._action, self._column)

	def __eq__(self, mv):
		return self.toTupple() == mv.toTupple()

	def __hash__(self):
		return self.toTupple().__hash__()

	def __repr__(self):
		return self.toTupple().__str__()


class SystemState:
	NUM_COLS = 7
	NUM_ROWS = 6
	MAX_FLIPS = 4

	def __init__(self, board=list(repeat([], 7)), prev_move=Move(), \
			cur_player=0, num_flips=(0, 0), is_down=0):
		self._board = board
		self._prev_move = prev_move
		self._cur_player = cur_player
		self._num_flips = num_flips
		self._is_down = is_down

	def update(self, mv):
		new_board = deepcopy(self._board)
		new_player = self._cur_player
		new_flips = deepcopy(self._num_flips)
		new_down = self._is_down

		if mv._action == 'flip':
			if self._prev_move._player == mv._player:
				new_player = int(not new_player)
			new_flips = tuple(map(lambda i: new_flips[i] + (i == self._cur_player), range(2)))
			new_down = int(not new_down)
		elif mv._action == 'place':
			if self._is_down:
				new_board[mv._column] = [self._cur_player] + new_board[mv._column]
			else:
				new_board[mv._column] = new_board[mv._column] + [self._cur_player]
		elif mv._action == 'none':
			if self._prev_move._player == mv._player:
				new_player = int(not new_player)

		return SystemState(new_board, mv, new_player, new_flips, new_down)

	def validMove(self, mv):
		if self._cur_player != mv._player:
			return False

		if mv._player == self._prev_move._player:
			if self._prev_move._action != 'place':
				if mv._action == 'place':
					return True

		if self._prev_move._action != 'flip':
			return mv._action != 'place'
		else:
			return mv._action == 'none'

		return False

	def genMoves(self):
		moves = set()

		if self._cur_player == self._prev_move._player:
			if self._prev_move._action == 'flip' or self._prev_move._action == 'none':
				for i in range(SystemState.NUM_COLS):
					moves.add(Move('place', self._cur_player, i))
				return moves

		if self._prev_move._action != 'flip':
			moves.add(Move('flip', self._cur_player))
			moves.add(Move('none', self._cur_player))
		else:
			moves.add(Move('none', self._cur_player))

		return moves


	def isGoal(self, mv):
		row = len(self._board[mv._column])-1
		matrix = deepcopy(self.filledMatrix())
		col = copy(mv._column)

		if matrix[col][row] != 2: #Avoid test in case of none or flip moves
			# Horizontal
			i = col - 3 if col > 3 else 0
			while i <= col and i <= SystemState.NUM_COLS-4:
				if matrix[i][row]==matrix[i+1][row]==matrix[i+2][row]==matrix[i+3][row]:
					return True
				i += 1
			# Vertical
			j = row - 3 if (row%7) > 3 else 0
			while j <= row and j <= SystemState.NUM_ROWS-4:
				if matrix[col][j]==matrix[col][j+1]==matrix[col][j+2]==matrix[col][j+3]:
					return True
				j += 1
			# Diagonal Left to rigth down
			startCol = col - 3 if col > 3 else 0
			startRow = row + 3 if col > 3 else row + col
			while startCol <= col and startCol <= 3:
				if startRow > 2 and startRow <6:
					if matrix[startCol][startRow]==matrix[startCol+1][startRow-1]\
					==matrix[startCol+2][startRow-2]==matrix[startCol+3][startRow-3]:
						return True
				startCol += 1
				startRow -= 1
			# Diagonal left to Right up
			startCol = col - 3 if col > 3 else 0
			startRow = row - 3 if col > 3 else row - col
			while startCol <= col and startCol <= 3:
				if startRow >= 0 and startRow <4:
					if matrix[startCol][startRow]==matrix[startCol+1][startRow+1]\
					==matrix[startCol+2][startRow+2]==matrix[startCol+3][startRow+3]:
						return True
				startCol += 1
				startRow += 1

		return False

	def filledMatrix(self):
		if self._is_down:
			filled = list(map(lambda c: c[::-1] + [2]*(SystemState.NUM_ROWS - len(c)), self._board))
		else:
			filled = list(map(lambda c: c + [2]*(SystemState.NUM_ROWS - len(c)), self._board))
		return deepcopy(filled)

	def toTupple(self):
		boardTup = self.getBoardTuple()
		return (boardTup, self._prev_move, self._cur_player, self._num_flips, self._is_down)

	def getBoardTupple(self):
		return tuple(map(tuple, self._board))

	def __eq__(self, state):
		return (self.getBoardTupple(), self._is_down) == (mv.getBoardTupple(), mv._is_down)

	def __hash__(self):
		return (self.getBoardTupple(), self._is_down).__hash__()

	def __repr__(self):
		return self.toTupple().__repr__()

	def __str__(self):
		filled = self.filledMatrix()
		conv = lambda k: 'X' if k == 0 else 'O' if k == 1 else ' '
		filled = list(map(lambda c: list(map(conv, c)), filled))

		toPrint = ' ' + '----' * 14 + '\n|'
		for j in range(SystemState.NUM_ROWS - 1, -1, -1):
			for i in range(SystemState.NUM_COLS):
				toPrint += '{0:^7}|'.format(filled[i][j])

				if i % 7 == 6:
					toPrint += '\n'
					toPrint += ' ' + '----' * 14 + '\n|'
		toPrint = toPrint[:-1]

		toPrint += ' '
		for i in range(7):
			toPrint += '{0:^7} '.format(i+1)
		if self._cur_player == 0:
			toPrint += '\nPlayer 1:'
		else:
			toPrint += '\nPlayer 2:'

		return toPrint
