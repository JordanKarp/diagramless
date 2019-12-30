import sys
import csv
from operator import itemgetter
import input_puzzle

def library_menu():
	'''Display's the puzzle library menu'''
	print('Welcome to the puzzle library.\n\t1. Choose puzzle from library to build.\n\t2. Add a new puzzle to the library')
	menu_option = int(input('Please make your selection: '))
	if menu_option == 1:
		puz_list = read_and_print_library() 
		return get_library_choice(puz_list)
	elif menu_option == 2:
		append_new_puzzle()
		read_and_print_library()
		sys.exit()

def read_and_print_library():
	'''Open the puzzle.csv file and print out the possible puzzle choices'''
	with open('puzzle.csv') as csvfile:
		lib_file = csv.reader(csvfile,delimiter=',')
		num_puzzles = 0
		puzzle_list = []
		for row in lib_file:
			num_puzzles += 1
			size = int(row[0])
			clue_str = row[1]
			sym = row[2]
			st_sq = int(row[3])
			find_all = row[4]
			puzzle_list.append([size,clue_str,sym,st_sq,find_all])
		puzzle_list = sorted(puzzle_list,key=itemgetter(0))

	print('#\tSize\t  Symmetry\tStart  Find All\tClue String')
	print('-~-' * 16)
	for num,puzzle in enumerate(puzzle_list,1):
		size,clue,sym,st_sq,find_all = puzzle
		print('{0}:\t{1:<2}\t{2:^12}\t{3}\t{4}\t{5}'.format(num,size,sym,st_sq,find_all,clue))
	return puzzle_list

def get_library_choice(puzzle_list):
	'''Get the puzzle choice from the user, and check that it's a valid input'''
	try:
		lib_choice = int(input('Which puzzle would you like to build? '))
	except:
		print('Input error, please try again.')
		sys.exit()
	else:
		return puzzle_list[lib_choice - 1]

def append_new_puzzle():
	'''Add a new puzzle to the puzzle library csv'''
	with open('puzzle.csv','a') as csvfile:
		csvWriter = csv.writer(csvfile)
		size,clue,sym,st_sq,find_all = input_puzzle.input_puzzle_solve()
		csvWriter.writerow([size,clue,sym,st_sq,find_all])

if __name__ == '__main__':
	library_menu()