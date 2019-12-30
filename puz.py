from board_class import Board, initialize_first_grid

class Puzzle():
	def __init__(self, puzzle_size, clue_str,symmetry=None,starting_cell=None,find_all=True):
		'''Object that holds this puzzles details and inputs'''
		self.puzzle_size = puzzle_size
		self.clue_str = clue_str + 'Y'
		self.symmetry = symmetry                 	
		self.starting_cell = starting_cell			
		self.find_all = find_all 					
		self.first_board = Board(initialize_first_grid(self.puzzle_size),self)

	def get_puzzle_size(self):
		'''Returns the puzzle size'''
		return self.puzzle_size

	def get_clue_str(self):
		'''Returns the clue string'''
		return self.clue_str

	def get_symmetry(self):
		'''Returns the puzzle symmetry'''
		return self.symmetry

	def get_starting_cell(self):
		'''Returns the puzzle's starting cell'''
		return self.starting_cell	

	def get_find_all(self):
		'''Returns the if the puzzle should find all soltions'''
		return self.find_all

	def print_clue_set(self, by_direction=False):
		'''Prints the clue set, either by clue string or by direction'''
		if by_direction == False:
			for num, clue in enumerate(self.clue_str,1):
				if clue != 'Y':
					print(f'{num}: {clue}')
		
		elif by_direction == True:
			a_list = list()
			d_list = list()
			for num, clue in enumerate(self.clue_str,1):
				if clue != 'Y':
					if clue == 'Z':
						a_list.append(num)
						d_list.append(num)
					if clue == 'A':
						a_list.append(num)
					if clue == 'D':
						d_list.append(num)
			print('Across Clues:', a_list)
			print('Down Clues:', d_list)

	def solve(self):
		'''Main loop; append the first board to the board list, and solve this board, couting solutions and total analyzed'''
		board_analyzed_count = 0
		print('Solving...')

		Board.board_list[0].adjust_starting_cells()
		for board in Board.board_list:
			board_analyzed_count += 1
			while board.is_analyzed == False:
				board.square_logic()
				board.print_grid()
				print(board.pointer_row,board.pointer_col, board.p_sym)
			if board_analyzed_count % 20000 == 0:
				print('{:,} boards analyzed so far.'.format(board_analyzed_count))
			if board.is_correct == True:
				if self.find_all == False:
					break
		print('-~-' * 8)

		for num,board in enumerate(Board.solution_list,1):
			print(f'\nSolution number {num}:')
			board.print_grid(with_clue_nums=True)
			# board.print_grid()
		self.print_clue_set(by_direction=True)
		print('{:,} boards analyzed.'.format(board_analyzed_count))





