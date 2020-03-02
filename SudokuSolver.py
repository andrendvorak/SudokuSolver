import glob
import numpy as np
from copy import deepcopy

#Takes in file and creates sudoku puzzle board
def makePuzzle(file):
	#Create array and fill with -1 to represent unfilled position
	board = np.full((9,9), -1)
	variables = {}

	#Fill initial positions
	with open(file) as f:
		for r in range(9):
			for c in range(9):
				value = f.read(1)
				if value != '-':
					board[r,c] = value
				else:
					variables[(r,c)] = [1,2,3,4,5,6,7,8,9]
				f.read(1)

	#Returns initial board and variables that need to be addded
	return board, variables


#Checks if any constraints are violated (same number in same row, column, or square)
#Returns true if contraints are met and false if contraints are violated
def constraints(assignment):
	count = np.zeros((1,9), dtype=int)

	#Checks if the same number is repeating in the same row
	for r in range(9):
		for c in range(9):
			if assignment[r,c] != -1:
				if count[0,assignment[r,c]-1] == 0:
					count[0,assignment[r,c]-1] = 1
				else:
					return False
		count = np.zeros((1,9), dtype=int)

	#Checks if the same number is repeating in the same column
	for c in range(9):
		for r in range(9):
			if assignment[r,c] != -1:
				if count[0,assignment[r,c]-1] == 0:
					count[0,assignment[r,c]-1] = 1
				else:
					return False
		count = np.zeros((1,9), dtype=int)

	#Checks if the same number is repeating in the same square
	x=0
	y=0
	for s in range(9):
		for r in range(x, x+3):
			for c in range(y, y+3):
				if assignment[r,c] != -1:
					if count[0,assignment[r,c]-1] == 0:
						count[0,assignment[r,c]-1] = 1
					else:
						return False
		count = np.zeros((1,9), dtype=int)

		#Set x and y to the coordinates of the upper left corner of the next square
		y += 3
		if (s+1)%3 == 0:
			x+=3
			y=0

	return True

#Checks if the board is complete (no -1's placed)
def complete(board):
	for r in range(9):
		for c in range(9):
			if board[r,c] == -1:
				return False
	return True

def MRV(assignment, variables):
	#Create a copy for encapsulation purposes
	assignment = np.copy(assignment)
	variables = variables.copy()

	minimumRemainingValues = 9
	MRV = (-1,-1)
	#MRV = list(variables.keys())[0]

	#Loop through unassigned positions and their domains
	for var in variables:
		valuesToDelete = []
		for value in variables[var]:
			assignment[var] = value
			#If there is a value that does not work add to list
			if not constraints(assignment):
				valuesToDelete.append(value)

		#Remove values from domain
		for v in valuesToDelete:
			variables[var].remove(v)

		#If the domain is smaller than the previous MRV, set this one instead	
		if len(variables[var]) < minimumRemainingValues:
			minimumRemainingValues = len(variables[var])
			MRV = var

		assignment[var] = -1

	return MRV, variables


#To call recursiveBacktracking
def backtrackingSearch(board, variables):
	return recursiveBacktracking(board, variables)

def recursiveBacktracking(assignment, variables):
	global guessCount

	#If the board is complete and all constraints are met, return the assignments
	if complete(assignment) and constraints(assignment):
		return assignment

	#Create a copy for encapsulation purposes
	assignment = np.copy(assignment)
	variables = deepcopy(variables)

	var, variables = MRV(assignment, variables)

	#Stores possible values of MRV
	values = variables.pop(var)

	#Loop through values and see if they violate any constraint
	#If no constraint is violated place the value and call function again
	#Counts guesses if the list has greater than 1 element
	for v in values:
		assignment[var] = v
		if len(values) != 1:
			guessCount += 1
		if constraints(assignment):
			result = recursiveBacktracking(assignment, variables)
			if result != "failure":
				return result
	return "failure"

#Look through all puzzles
files = glob.glob("Sudoku/*.txt")

for f in files:

	#Stores number of guesses per puzzle
	guessCount = 0

	print("---------------------" + str(f) + "---------------------")

	board, variables = makePuzzle(f)

	print(backtrackingSearch(board, variables))

	print("TOTAL NUMBER OF GUESSES " + str(guessCount))