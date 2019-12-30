from os import system, name 
import input_puzzle as inp
import library as lib
from puz import Puzzle

def clear(): 
	'''Clears the terminal display'''
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear')

def main_menu():
	'''Display the main menu and take the user's input'''
	clear()
	try:
		print('Welcome to the Diagramless Crossword Puzzle Builder')
		print('-~-' *16)
		print('1. Open the puzzle library')
		print('2. Manually input a puzzle and build')
		print('3. Import puzzle from NYT puzzle cache')
		print('-~-' *16)
		menu_item = int(input('Please make your selection: '))
		if menu_item > 3 or menu_item < 1:
			raise Exception
	except:
		print('Input error. Please try again.')
		main_menu()
	else:
		if menu_item == 1:
			clear()
			size,clue_str,sym,st_sq,find_all = lib.library_menu()
		elif menu_item == 2:
			clear()
			size,clue_str,sym,st_sq,find_all = inp.input_puzzle_solve()
		elif menu_item == 3:
			clear()
			pass
			# size,clue_str,sym,st_sq,find_all = nyt_cache_import()			
		
		active_puzzle = Puzzle(size,clue_str,sym,st_sq,find_all)
		active_puzzle.solve()

def nyt_cache_import():
	pass

if __name__ == '__main__':
	main_menu()

