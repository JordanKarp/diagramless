import sys

def input_puzzle_solve():
	'''Get a puzzle input from the user'''
	puz_size = input_puzzle_size()
	puz_sym = input_puzzle_symmetry()
	puz_start_sq = input_puzzle_starting_square(puz_size)
	puz_find_all = input_puzzle_find_all()
	puz_clue_set_str = input_across_and_down_clues()
	return puz_size, puz_clue_set_str, puz_sym, puz_start_sq, puz_find_all

def input_puzzle_size():
	'''Get the puzzle size from the user, and check that it's a valid input'''
	try:
		input_size = int(input('What is the size of your puzzle (3 - 21): '))
		if input_size < 3 or input_size > 21:
			raise Exception
	except:
		print('Input error, please try again.')
		sys.exit()
	else:
		return input_size

def input_puzzle_symmetry():
	'''Get the puzzle symmetry from the user, and check that it's a valid input'''
	possible_answers = ['1','2','3','4','N','D','V','H','n','d','v','h','None','Diagonal','Vertical','Horizontal']
	try:
		print('''Symmetry: \n\t1. None (default)\n\t2. Diagonal Axis\n\t3. Vertical Axis\n\t4. Horizontal Axis''')
		input_symmetry = str(input('Puzzle Symmetry: '))
		if input_symmetry not in possible_answers:
			raise Exception
	except:
		print('Input error, please try again.')
		sys.exit()
	else:
		if input_symmetry == '1' or input_symmetry == 'N' or input_symmetry == 'n' or input_symmetry == 'None' or input_symmetry == None:
			puz_sym = 'None'
		if input_symmetry == '2' or input_symmetry == 'D' or input_symmetry == 'd' or input_symmetry == 'Diagonal':
			puz_sym = 'Diagonal'
		if input_symmetry == '3' or input_symmetry == 'V' or input_symmetry == 'v' or input_symmetry == 'Vertical':
			puz_sym = 'Vertical'
		if input_symmetry == '4' or input_symmetry == 'H' or input_symmetry == 'h' or input_symmetry == 'Horizontal':
			puz_sym = 'Horizontal'
		return puz_sym

def input_puzzle_starting_square(p_size):	
	'''Get the puzzle starting square from the user, and check that it's a valid input'''
	try:
		input_starting_sq = int(input('Starting square (0 for none): '))
		if input_starting_sq >= p_size - 1:
			raise Exception
	except:
		print('Input error, please try again.')
		sys.exit()
	else:
		return input_starting_sq

def input_puzzle_find_all():
	'''Get the puzzle's find all value from the user, and check that it's a valid input'''
	possible_answers = ['T','t','True',True,'F','f','False',False]
	try:
		input_puz_f_all = input('Find all solutions (True or False): ')
		if input_puz_f_all not in possible_answers:
			raise Exception
	except:
		print('Input error, please try again.')
		sys.exit()
	else:
		if input_puz_f_all == 'T' or input_puz_f_all == 't' or input_puz_f_all == 'True' or input_puz_f_all == True:
			find_all = True
		elif input_puz_f_all == 'F' or input_puz_f_all == 'f' or input_puz_f_all == 'False' or input_puz_f_all == False:
			find_all = False
		return find_all

def clue_set_converter(across_nums,down_nums):
	'''Converts a list of across clues and a list of down clues into one lists of A/D/Z clues (clueset)'''
	clue_set = []
	for number in range(1,int(max(across_nums)) + 1):
	    if number in across_nums and number in down_nums:
	        clue_set.append('Z')
	    if number in across_nums and number not in down_nums:
	        clue_set.append('A')
	    if number not in across_nums and number in down_nums:
	        clue_set.append('D')
	clue_set_str = ''.join(clue_set)
	return clue_set_str

def input_across_and_down_clues():
	'''Get the puzzle's across and down clues from the user, and check that thery are valid inputs'''
	try:
		input_across_set = [int(x) for x in input('Input the Across clue numbers, separated by spaces: ').split()]
		input_down_set = [int(x) for x in input('Input the Down clue numbers, separated by spaces: ').split()]
	except:
		print('Input error, please try again.')
		sys.exit()
	else:
		clue_set = clue_set_converter(input_across_set,input_down_set)
		return clue_set

