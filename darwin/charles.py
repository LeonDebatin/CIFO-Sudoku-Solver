import random
import copy
from darwin.sudoku import columns_to_rows, boxes_to_rows
random.seed(55)

    

class Individual:
    def __init__(self, sudoku):
        
        self.sudoku = sudoku
        self.representation = self.fill_template()
        self.fitness = self.get_fitness()
        
    
    
    def fill_template(self):
        #to generate a representation for each individual, we fill the 0s of the template,
        # which are the not appearing numbers in the fixed indices, from the sudoku object with random numbers from the possible_entries
        
        #we create a deepcopy cause we overwrite template otherwise, even with .copy() function
        filled_template = copy.deepcopy(self.sudoku.template) 
        
        for i in range(self.sudoku.size):
            for j in range(self.sudoku.size):
                if (i, j) not in self.sudoku.fixed_indices:
                    filled_template[i][j] = random.choice(self.sudoku.possible_entries[i][j])
        return filled_template
    
    
    #other option to fill the template, we didnt use it in the end because its not about genetic algorithms
    def fill_template2(self):
        #after we get the fixed indices we fill the 0s of the template with random numbers within the range of 1 to size
        #hereby we create the grid, that we want to turn into a possible solution for the template
        #print('startl',len(self.sudoku.fixed_indices))
        #we create a deepcopy cause we overwrite template otherwise, even with .copy() function
        #then we fill 0s with random numbers if they are not in the fixed_indices
        for i in range(self.sudoku.size):
            for j in range(self.sudoku.size):
                if (i, j) not in self.sudoku.fixed_indices:
                    if len(self.sudoku.possible_entries[i][j]) == 1:
                        self.sudoku.template[i][j] = self.sudoku.possible_entries[i][j][0]

        self.sudoku.fixed_indices = self.sudoku.get_fixed_indices() 
        self.sudoku.possible_entries = self.sudoku.get_possible_entries()
        
        
        filled_template = copy.deepcopy(self.sudoku.template)

        for i in range(self.sudoku.size):
            for j in range(self.sudoku.size):
                if (i, j) not in self.sudoku.fixed_indices:

                    filled_template[i][j] = random.choice(self.sudoku.possible_entries[i][j])

        
        
        return filled_template
    
    
    
    def get_fitness(self):
    #we define the fitness as the sum of the number of duplicates within each row, column and box
    #since we only change numbers that are not given by the template
    #we know that we have a plausible solution if the number of duplicates is 0
    
        def count_duplicates(list):
            #we start with a function that counts the duplicates for a list
            #we use a dictionary to count the occurences for each number
            
            number_counts = {}
            for number in list:
                if number in number_counts:
                    number_counts[number] += 1
                else:
                    number_counts[number] = 1
            
            
            #then we return the difference between the length of the list and the length of the keys of the dictionary which is the number of duplicates
            return (len(list)-len(number_counts.keys()))
        
        
        def count_row_duplicates(grid):
            #then we define a function that iterates over the grid, gets the duplicates within each row and sums them up
            
            duplicates = 0
            for row in grid:
                duplicates += count_duplicates(row)
            return duplicates
            
        def count_column_duplicates(grid):
            #since we have a function already for getting the duplicates in a row wise perspective, we use the columns to rows function that transposes the grid
            #and therefore 'turns the column perspective in a row perspective' and allows us to use the row function to sum up
            grid = columns_to_rows(grid)
            return count_row_duplicates(grid)        
        
        def count_box_duplicates(grid, box_size):
            #then we calculate the box_duplicates turing the box into a row perspective and using the row count duplicates function
            grid = boxes_to_rows(grid, box_size)
            return count_row_duplicates(grid)

        #finally we return the sum of the duplicates for rows, columns and boxes
        return  count_row_duplicates(self.representation) + count_column_duplicates(self.representation) + count_box_duplicates(self.representation, self.sudoku.box_size)
        
        


class Population:

    def __init__(self, size, sudoku):    
        
        self.size = size #number of individuals
        self.sudoku = sudoku #sudoku to give to individuals
        self.individuals = [] #individuals
        self.children = None #children
        self.parents = None #parents
        self.best_fitness = None #best individuals fitness
        self.average_fitness = None #mean of fitness
        
        #fill individuals when initializing
        for i in range(size):
            self.individuals.append(
                Individual(sudoku=sudoku)
            )

    def get_best_fitness(self):
        #return the best individual
        self.best_fitness = self.individuals[0].fitness
    
    def get_average_fitness(self):
        #get the average fitness
        sum = 0
        for i in range(self.size):
            sum += self.individuals[i].fitness

        self.average_fitness = sum // self.size
    
    def sort_individuals(self):
        #sort individuals
        self.individuals = sorted(self.individuals, key=lambda x: x.fitness)
        
    def sort_children(self):
        #sort children
        self.children = sorted(self.children, key=lambda x: x.fitness)
    
    def get_fitnesses(self):
        #get the fitnesses of the individuals
        for i in range(self.size):
            self.individuals[i].fitness = self.individuals[i].get_fitness()

    def get_fitnesses_for_children(self):
        #get the fitnesses of the individuals
        for i in range(self.size):
            self.children[i].fitness = self.children[i].get_fitness()

    