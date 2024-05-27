# import copy
# import random

class Sudoku:
    def __init__(self, template):
        

        self.size = len(template) #size of the grid (normal 9x9, since quadratic we only save the number as one int)
        self.box_size = self.get_box_size() #size of the boxes (normal 3x3, since the box sizes can be different depending on the grid size, we save it as a list [3,3])
        self.template = template #initial numbers within the list of the list of the problem to solve
        self.fixed_indices = self.get_fixed_indices() #indices of the given numbers
        self.possible_entries = self.get_possible_entries() #based on the given numbers, for each cell the possible entries are calculated
        self.number_of_possible_solutions = self.get_number_of_possible_solutions() #total number of possible solutions for the given template (multiplied length of possible entries for each cell up)
        return


    def get_box_size(self):
        #returns the size of the boxes, which is obvious for square numbers like 9x9 and 16x16, where it is the squareroot, but not for 12x12 or 18x18 grids for example
        #In this case the boxes will be in the shape of the possible multiplicators, where the multiplicators sum is the smallest
        #Example: 18 = 2*9 or 3*6, where 2+9 = 11 and 3+6 = 9, so the boxes will be 6,3
        
        #a 1x1 Sudoku doesn't make sense
        if self.size <= 1:
            raise ValueError("The size of the provided template can't be smaller 2!")
        
        #we iterate over the possible multplicators and save the sum for each combination, then we return the combination of multiplicators with the smallest sum
        min_sum = float('inf')
        multiplicators = []
        
        for i in range(1, self.size + 1):
            if self.size % i == 0:
                j = self.size // i
            if i + j < min_sum:
                min_sum = i + j
                multiplicators = [j, i]  #we save j,i so the bigger number which will refer to the number of columns within a box will be first

        #if one of the multiplicators equals 1, the size is a prime number, which we don't allow since then we don't have boxes
        if 1 in multiplicators:
            raise ValueError("The size of the provided template can't be a prime numbers!")
        
        return multiplicators  
    
    
    def get_possible_entries(self):
        
        #empty list for each sudoku cell to fill with possible entires        
        possible_entries = [[[]for i in range(self.size)] for j in range(self.size)]
        
        #numbers 1 to size, theoretically possible
        possible_numbers = [i for i in range(1, self.size + 1)]
        
        #turn box perspective into row perspective
        boxes = boxes_to_rows(self.template, self.box_size)

        
        
        def get_box_index(row, col, box_size):
            # Determine the box indices based on row and column indices
            box_row = row // box_size[1]
            box_col = col // box_size[0]
            # Return the box index
            return box_row * box_size[1] + box_col
        
        
        #we iterate ver each cell, and check which numbers are already in the column/row/box
        #then we substract these numbers from the possible numbers, where as the possible numbers are numbers from 1 to size, and get the possible entries
        for i in range(self.size):
            
            numbers_in_row = self.template[i]
            
            for j in range(self.size):
                
                if (i, j) not in self.fixed_indices:
                
                    numbers_in_column = [row[j] for row in self.template]
                    
                    numbers_in_box = boxes[get_box_index(i,j, self.box_size)]
                    
                    possible_entries[i][j] = (list(set(possible_numbers) - set(numbers_in_row)- set(numbers_in_column)- set(numbers_in_box) ))

        return possible_entries
    
    
        
    def get_fixed_indices(self):
        #get's the fixed_indices, the numbers of the template which are not 0s
        #these are the indices for the numbers we never want to change
        
        return [(i, j) for i in range(self.size) for j in range(self.size) if self.template[i][j] != 0]
    
    
    def get_number_of_possible_solutions(self):
        number_of_possible_solutions = 1
        complexities = []
        
        #for each cell we get the length of the possible entries and append them if the cell is not given by the template
        for i in range(len(self.possible_entries)):
            for j in range(len(self.possible_entries[i])):
                if (i,j) not in self.fixed_indices:
                    complexities.append(len(self.possible_entries[i][j]))

        #then we multiply all these numbers together to get the total number of possible solutions that is the theoretical search space
        number_of_possible_solutions = 1
        for i in range(len(complexities)):
            number_of_possible_solutions = complexities[i] * number_of_possible_solutions
        
        return number_of_possible_solutions


##########################
#here we supply further helpful function that handle the matrix in the sudoku context to provide rows/columns/box perspective




def columns_to_rows(grid):
    #a function that turn the box perspective into the column perspective (first column will be the first row, second column will be second row etc.)
    #this allows us to specify functions that iterate over rows and use them for the columns as well using the columns to rows and rows to columns functions
    
    return [[row[i] for row in grid] for i in range(len(grid))]  #transposes the grid


def rows_to_columns(grid):
    return [[row[i] for row in grid] for i in range(len(grid))]



def boxes_to_rows(grid, box_size):
    #a function that turn the box perspective into the row perspective (first box will be the first row, second box will be second row etc.)
    #same idea as with the columns
    rows = []
    
    #iterates over the box_size[1] columns
    for i in range(0, len(grid), box_size[1]):
        #then over the  box_size[0] rows
        for j in range(0, len(grid), box_size[0]):
            row = []
            #gets each number for the box columnwise first (columns from left to right)
            for k in range(box_size[1]):
                #and then for each row (rows from top to bottom)
                for l in range(box_size[0]):
                    row.append(grid[i + k][j + l])
            rows.append(row)
        #so the top left box will be the first row of the grid, the top middle box will be the second row and so on
    return rows



def rows_to_boxes(rows, box_size):
    #reverse function to get the original boxes perspective back
    
    #get the size
    size = len(rows)
    #generate empty grid
    grid = [[0] * size for _ in range(size)]
    #get the number of columns per box
    box_col_count = size // box_size[0]
    
    #puts the numbers from the rows back into the boxes filling the grid
    for box_index, box in enumerate(rows):
        start_row = (box_index // box_col_count) * box_size[1]
        start_col = (box_index % box_col_count) * box_size[0]
        
        for i in range(box_size[1]):
            for j in range(box_size[0]):
                grid[start_row + i][start_col + j] = box[i * box_size[0] + j]
    
    return grid

def plot_sudoku(object):
    #to get a somewhat nice representation of our sudoku grid we create a print function, which prints the grid with the boxes
    
    def plot_matrix(sudoku, matrix):
    #we define a function that can print a grid, since we used the name grid for the classobject already, we go with the name matrix here for no confusion
    #since the function is designed to print either self.grid or self.template
    #also we color the numbers from the template to distinguish them from the numbers we filled in the grid

        #a bash color for turquoise background in this case
        color = '\033[44m'
        #bashcode to end coloring
        end_color = '\033[0m'
        
        #box_size[1] is the number of rows per box, we iterate over i and if i is dividable by the box size we add a row of '---- to simulate the boxborders
        for i in range(sudoku.size):
            if i % sudoku.box_size[1] == 0 and i != 0:
                print("-" * int(sudoku.size * 3.3), end = '\n') #took a while to find out that 3.3 is best

            #box size[0] is the number of columns per box, after the number of columns is reached we add '|'to simulate the boxborders
            for j in range(sudoku.size):
                if j % sudoku.box_size[0] == 0 and j != 0:
                    print("|", end=" ")

                #if the number to print is in the template we give it a color, not if otherwise
                if (i, j) in sudoku.fixed_indices:
                    print(color + str(matrix[i][j]) + end_color, end=" ")
                else:
                    print(matrix[i][j], end=" ")
                
                #to have an ordered print we need to add a space for one digit numbers    
                if matrix[i][j] < 10:
                    print("", end=" ")

                if j == sudoku.size - 1:
                    print()
            
        return
                    
    #we want the function to work both for individuals and sudokus, so we check the type of the object and then plot the matrix	    
    if str(type(object)) == "<class 'darwin.charles.Individual'>":
        sudoku = object.sudoku
        matrix = object.representation

    elif str(type(object)) == "<class 'darwin.sudoku.Sudoku'>":
        sudoku = object
        matrix = object.template

    else:
        raise TypeError("You can just plot Sudokus or Individuals!")
        
    plot_matrix(sudoku, matrix)

    return