BUFFER_SIZE = 3
BLACK = u'\u2588'
BLANK = ' '

class Board():
	board_list = []
	solution_list = []

	def __init__(self, grid, puzzle, pointer_row=0, pointer_col=0, clue_counter=0):
		''' Object that holds a potentially correct board'''
		self.grid = grid
		self.puzzle = puzzle	
		self.p_size = puzzle.get_puzzle_size()
		self.p_clue_str = puzzle.get_clue_str()
		self.p_sym = puzzle.get_symmetry()
		self.p_starting_cell = puzzle.get_starting_cell()	
		self.p_find_all = puzzle.get_find_all()																		
		self.pointer_row = pointer_row                     
		self.pointer_col = pointer_col 
		self.clue_counter = clue_counter 
		self.is_correct = False    
		self.is_analyzed = False
		Board.board_list.append(self)

	def print_grid(self, with_clue_nums=False):
		'''Prints the grid, with either clues (A,D,Z) or with numbers'''
		if with_clue_nums == False:
			for row in self.grid[BUFFER_SIZE:-BUFFER_SIZE]:
				print(row[BUFFER_SIZE:-BUFFER_SIZE])
		
		elif with_clue_nums == True:
			clue_num_counter = 1
			print(('-' * self.p_size * 5)+ '-')
			for row in self.grid[BUFFER_SIZE:-BUFFER_SIZE]:
				print('| ', end='')
				for col in row[BUFFER_SIZE:-BUFFER_SIZE]:
					if col == 'Z' or col == 'A' or col == 'D':
						print(str(clue_num_counter).zfill(2),'| ', end='')
						clue_num_counter += 1
					if col == BLACK:
						print(BLACK+BLACK,'| ',end='')
					if col == BLANK:
						print(str('  '),'| ',end='')
				print('\n'+('-' * self.p_size * 5)+ '-')

	def copy_grid(self):
		'''Make a duplicate of the current board'''
		return [row[:] for row in self.grid]

	def finished_analyzing_grid(self):
		'''Stop analyzing this board'''
		self.is_analyzed = True

	def correct(self):
		'''This board is a correct solution'''
		self.is_correct = True
		Board.solution_list.append(self)

	def advance_clue_counter(self):
		'''Keeps track of what clue we're placing for this board'''
		self.clue_counter += 1

	def advance_pointer(self):
		'''Moves the pointer to the next available spot, checking for a valid row'''
		if self.pointer_col < self.p_size - 1:			
			self.pointer_col += 1 
			return                      		          
		if self.not_a_full_black_row() and self.no_blank_following_a_black() and self.no_black_above_blank():						
			self.pointer_row += 1
			self.pointer_col = 0
			return
		else:
			self.finished_analyzing_grid()
			return

	def not_a_full_black_row(self):
		'''Check if there is a full row of black squares'''
		for col in self.grid[self.pointer_row+BUFFER_SIZE]:
			if col != BLACK:
				return True
		return False
	
	def no_blank_following_a_black(self):
		'''Check that if there is black cell, the next cell is not a blank'''
		for i in range(self.p_size+BUFFER_SIZE):
			if self.grid[self.pointer_row + BUFFER_SIZE][i] == BLACK:
				if self.grid[self.pointer_row + BUFFER_SIZE][i +1] == BLANK:
					return False
		return True

	def no_black_above_blank(self):
		'''Check that if there is a blank cell, the above cell is not black'''
		for i in range(self.p_size + BUFFER_SIZE):
			if self.grid[self.pointer_row+BUFFER_SIZE][i] == BLANK or self.grid[self.pointer_row+BUFFER_SIZE][i] == '-':
				if self.grid[self.pointer_row+BUFFER_SIZE -1][i] == BLACK:
					return False
		return True

	def place_at_pointer(self, clue):
		'''Put the given clue at the given pointer row and pointer column'''
		self.grid[BUFFER_SIZE + self.pointer_row][BUFFER_SIZE + self.pointer_col] = str(clue)

	def place_clue_incr_counter_and_pointer(self,clue):
		'''Place clue, increment the clue counter, and advance the pointer'''
		self.place_at_pointer(clue)
		self.advance_clue_counter()
		self.advance_pointer()

	def place_blank_incr_pointer(self):
		'''Place a blank square, then advance the pointer'''
		self.place_at_pointer(BLANK)
		self.advance_pointer()

	def place_black_at_symmetrical_pointer(self):
		'''Place a black square at the given symmetrical spot'''
		if self.p_sym == 'Diagonal':
			sym_row = self.p_size - self.pointer_row - 1        
			sym_col = self.p_size - self.pointer_col -1     
			self.grid[BUFFER_SIZE + sym_row][BUFFER_SIZE + sym_col] = BLACK
		elif self.p_sym == 'Vertical':
			sym_row = self.pointer_row 
			sym_col = self.p_size - self.pointer_col - 1     
			self.grid[BUFFER_SIZE + sym_row][BUFFER_SIZE + sym_col] = BLACK
		elif self.p_sym == 'Horizontal':
			sym_row = self.p_size - self.pointer_row - 1       
			sym_col = self.pointer_col 
			self.grid[BUFFER_SIZE + sym_row][BUFFER_SIZE + sym_col] = BLACK

	def symmetrical_spot_or_no_symmetry(self):
		'''If there is no symmetry or the pointer is in the symmetrical placeable 'half' of the puzzle, return True.'''
		midpoint = self.p_size / 2
		if self.p_sym == None or self.p_sym == 'None':
			return True
		elif self.p_sym == 'Diagonal' or self.p_sym == 'Horizontal':
			if self.p_size % 2 == 0:
				if self.pointer_row < midpoint:
					return True
				if self.pointer_row >= midpoint:
					return False
			if self.p_size % 2 == 1:		
				if self.pointer_row < (midpoint - .5):
					return True
				if self.pointer_row == (midpoint - .5):
					if self.pointer_col < (midpoint - .5):
						return True
					else:
						return False
				else:
					return False
		elif self.p_sym == 'Vertical':
			if self.p_size % 2 == 0:
				if self.pointer_col < midpoint:
					return True
				else:
					return False
			if self.p_size % 2 == 1:		
				if self.pointer_col < (midpoint - .5):
					return True
				else:
					return False

	def adjust_starting_cells(self):
		'''If there is a starting cell, fix the board to match that'''
		if self.p_starting_cell != None and self.p_starting_cell > 0:
			for _ in range(self.p_starting_cell-1):
				self.check_if_place_black_and_sym_black()
			self.place_clue_incr_counter_and_pointer('Z')


	def clue_at_pointer(self):
	'''Return what clue is at the current pointer'''
		return self.grid[BUFFER_SIZE + self.pointer_row][BUFFER_SIZE + self.pointer_col]

	def U1(self): 
		'''Return the clue up 1 from the pointer'''
		return self.grid[BUFFER_SIZE + self.pointer_row - 1][BUFFER_SIZE + self.pointer_col]
	def U2(self): 
		'''Return the clue up 2 from the pointer'''
		return self.grid[BUFFER_SIZE + self.pointer_row - 2][BUFFER_SIZE + self.pointer_col]
	def U3(self): 
		'''Return the clue up 3 from the pointer'''
		return self.grid[BUFFER_SIZE + self.pointer_row - 3][BUFFER_SIZE + self.pointer_col]
	def D1(self): 
		'''Return the clue down 1 from the pointer'''
		return self.grid[BUFFER_SIZE + self.pointer_row + 1][BUFFER_SIZE + self.pointer_col]
	def D2(self): 
		'''Return the clue down 2 from the pointer''' 
		return self.grid[BUFFER_SIZE + self.pointer_row + 2][BUFFER_SIZE + self.pointer_col]
	def D3(self): 
		'''Return the clue down 3 from the pointer'''
		return self.grid[BUFFER_SIZE + self.pointer_row + 3][BUFFER_SIZE + self.pointer_col]
	def L1(self): 
		'''Return the clue left 3 from the pointer'''
		return self.grid[BUFFER_SIZE + self.pointer_row][BUFFER_SIZE + self.pointer_col - 1]
	def L2(self): 
		'''Return the clue left 2 from the pointer'''
		return self.grid[BUFFER_SIZE + self.pointer_row][BUFFER_SIZE + self.pointer_col - 2]
	def L3(self): 
		'''Return the clue left 3 from the pointer'''
		return self.grid[BUFFER_SIZE + self.pointer_row][BUFFER_SIZE + self.pointer_col - 3]
	def R1(self): 
		'''Return the clue right 1 from the pointer'''
		return self.grid[BUFFER_SIZE + self.pointer_row][BUFFER_SIZE + self.pointer_col + 1]
	def R2(self): 
		'''Return the clue right 2 from the pointer'''
		return self.grid[BUFFER_SIZE + self.pointer_row][BUFFER_SIZE + self.pointer_col + 2]
	def R3(self): 
		'''Return the clue right 3 from the pointer'''
		return self.grid[BUFFER_SIZE + self.pointer_row][BUFFER_SIZE + self.pointer_col + 3]

	def check_free_spot(self, *check_clues):
		'''Returns true if ALL the following clues are open'''
		return len([True for clue in check_clues if clue != BLACK]) == len(check_clues)

	def check_filled_spot(self, *check_clues):
		'''Returns true if ONE the following clues are NOT free'''
		return len([True for clue in check_clues if clue == BLACK]) > 0

	def check_if_place_black_and_sym_black(self):
		'''Check if we can, then place a black square and at its sym black, and advance the pointer'''
		if self.symmetrical_spot_or_no_symmetry():
			self.place_at_pointer(BLACK)
			if self.p_sym != None:
				self.place_black_at_symmetrical_pointer()
		self.advance_pointer()

	def check_if_dup_grid_and_dup_sym(self):
		'''Check if we can, then create a dupboard, place a black and sym black in it, advance pointer, then append to board list ''' 
		print('in dup func')
		if self.symmetrical_spot_or_no_symmetry():
			print('in dup func, passed sym/nosym check')

			new_board = Board(self.copy_grid(),self.puzzle,self.pointer_row,self.pointer_col, self.clue_counter)
			new_board.place_at_pointer(BLACK)
			if self.p_sym != None:
				new_board.place_black_at_symmetrical_pointer()
			new_board.advance_pointer()
			Board.board_list.append(new_board)

	def square_logic(self):
		'''Depending on the clue and what is neighboring the pointer, do approproiate action for that pointer location.'''
		if self.p_sym != None and self.pointer_row != self.p_size:
			if self.clue_at_pointer() == BLACK:
				self.advance_pointer()
				return
		if self.p_clue_str[self.clue_counter] == 'D':
			if self.U1() == BLACK:
				if self.L1() == BLACK:
					self.finished_analyzing_grid()
					return
				if self.check_free_spot(self.L1()):
					if self.check_filled_spot(self.D1(),self.D2()):
						self.finished_analyzing_grid()
						return
					if self.check_free_spot(self.D1(),self.D2()):
						self.place_clue_incr_counter_and_pointer('D')
						return
			if self.check_free_spot(self.U1()):
				if self.check_free_spot(self.L1()):
					self.place_blank_incr_pointer()
				else:
					self.finished_analyzing_grid()
				return

		if self.p_clue_str[self.clue_counter] == 'A':
			if self.U1() == BLACK:
				if self.L1() == BLACK:
					self.check_if_place_black_and_sym_black()
					return
				if self.check_free_spot(self.L1()):
					if self.check_filled_spot(self.L2(), self.L3()):
						self.finished_analyzing_grid()
					if self.check_free_spot(self.L2(),self.L3()):
						self.check_if_place_black_and_sym_black()
						return
			if self.check_free_spot(self.U1()):
				if self.L1() == BLACK:
					if self.check_filled_spot(self.R1(),self.R2()):
						self.check_if_place_black_and_sym_black()
						return
					if self.check_free_spot(self.U2(),self.U3()):
						self.check_if_dup_grid_and_dup_sym()
					self.place_clue_incr_counter_and_pointer('A')
					return
				if self.check_free_spot(self.L1()):
					if self.check_filled_spot(self.L2(),self.L3(),self.U2(),self.U3()):
						self.place_blank_incr_pointer()
						return
					if self.check_free_spot(self.L2(),self.L3(),self.U2(),self.U3()):
						self.check_if_dup_grid_and_dup_sym()
						self.place_blank_incr_pointer()
						return

		if self.p_clue_str[self.clue_counter] == 'Z':
			if self.U1() == BLACK:
				if self.L1() == BLACK:
					if self.check_filled_spot(self.R1(),self.R2(),self.D1(),self.D2()):
						self.check_if_place_black_and_sym_black()
						return
					if self.check_free_spot(self.R1(),self.R2(),self.R3(),self.D1(),self.D2()):
						self.check_if_dup_grid_and_dup_sym()
					self.place_clue_incr_counter_and_pointer('Z')
					return
				if self.check_free_spot(self.L1()):
					if self.check_filled_spot(self.L2(),self.L3()):
						self.finished_analyzing_grid()
						return
					if self.check_free_spot(self.L2(),self.L3()):
						self.check_if_place_black_and_sym_black()
						return
			if self.check_free_spot(self.U1()):
				if self.L1() == BLACK:
					if self.check_filled_spot(self.U2(),self.U3()):	
						# self.place_blank_incr_pointer()
						self.finished_analyzing_grid()
						return
					if self.check_free_spot(self.U2(),self.U3()):	
						self.check_if_dup_grid_and_dup_sym()
					self.place_blank_incr_pointer()
					return
				if self.check_free_spot(self.L1()):
					if self.check_filled_spot(self.L2(),self.L3(),self.U2(),self.U3()):
						self.place_blank_incr_pointer()
						return
					if self.check_free_spot(self.L2(),self.L3(),self.U2(),self.U3()):
						self.check_if_dup_grid_and_dup_sym()
					self.place_blank_incr_pointer()
					return


		if self.p_clue_str[self.clue_counter] == 'Y':
			if self.pointer_row == self.p_size:
				self.correct()
				self.finished_analyzing_grid()
				return
			if self.pointer_row < self.p_size - 1:
				self.finished_analyzing_grid()
				return
			if self.pointer_row == self.p_size - 1:
				if self.check_filled_spot(self.L1()):
					self.check_if_place_black_and_sym_black()
					return
				if self.check_free_spot(self.L1()):
					if self.check_filled_spot(self.U1(),self.U2()):
						self.finished_analyzing_grid()
						return
					if self.check_filled_spot(self.L2(),self.L3()):
						self.place_blank_incr_pointer()
						return
					if self.check_free_spot(self.L2(),self.L3()):
						self.check_if_dup_grid_and_dup_sym()
					self.place_blank_incr_pointer()
					return
		# else:
		# 	self.finished_analyzing_grid()


def initialize_first_grid(p_size):
	'''Set's up the very first blank grid based on the puzzle size, with a buffer'''
	board_size = (2 * BUFFER_SIZE) + p_size
	#List comprehension to fill BLACK in to a list of lists
	first_grid = [[(BLACK)] * board_size for i in range(board_size)]     
 	#Turn the space inside the buffer into BLANK 
	for i in range(BUFFER_SIZE, board_size - BUFFER_SIZE):    
		for j in range(BUFFER_SIZE, board_size - BUFFER_SIZE):
			first_grid[i][j] = '-'
	return first_grid

		
