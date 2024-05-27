import random


def mutate(individual, mutation_rate, mutation_method=None):

    #choses the mutation method based on te given mutation_method
    
    if mutation_method == 'flip_mutation':
        individual = flip_mutation(individual, mutation_rate)
        return individual
        
    if mutation_method == 'mixed_exchange_mutation':
        mixed_exchange_mutate(individual, mutation_rate)
        return individual
    
    if mutation_method == 'box_exchange_mutation':
        box_exchange_mutate(individual, mutation_rate)
        return individual
    
    if mutation_method == 'a_bit_of_all_mutation':
        a_bit_of_all_mutation(individual, mutation_rate)
        return individual
        
    else:
        raise TypeError('Something went wrong!')


def flip_mutation(individual, mutation_rate):
    # replaces the value of a cell with a random value from the possible entries
    # its not exactly a flip mutation but we thought its the most comparable to a such thats why we called it that way
    for i in range(individual.sudoku.size):
        for j in range(individual.sudoku.size):
            if (i, j) not in individual.sudoku.fixed_indices:
                if random.uniform(0, 1) <= mutation_rate:
                    individual.representation[i][j] = random.choice(individual.sudoku.possible_entries[i][j])

    return individual




def row_exchange_mutate(individual, mutation_rate):
    #replaces two numbers within a row with each other(if its not a fixed index)
    #also we need to be careful that the numbers are in the possible entries of the other cell
    for i in range(individual.sudoku.size):
        for j in range(individual.sudoku.size):
            if random.uniform(0,1) <= mutation_rate:
                if (i,j) not in individual.sudoku.fixed_indices:
                    
                    random_indic =  random.randint(0,individual.sudoku.size -1)
                    
                    #if the number is not included in the template and the possible entries match
                    if ((i, random_indic)) not in individual.sudoku.fixed_indices and (individual.representation[i][j] in individual.sudoku.possible_entries[i][random_indic]) and (individual.representation[i][random_indic] in individual.sudoku.possible_entries[i][random_indic]):
                        #we exchange
                        help = individual.representation[i][j]
                        individual.representation[i][j] = individual.representation[i][random_indic]
                        individual.representation[i][random_indic] = help
    return individual


def column_exchange_mutate(individual, mutation_rate):
    #replaces two numbers within a column with each other(if its not a fixed index)
    #also we need to be careful that the numbers are in the possible entries of the other cell
    for i in range(individual.sudoku.size):
        for j in range(individual.sudoku.size):
            if random.uniform(0, 1) <= mutation_rate:
                if (i, j) not in individual.sudoku.fixed_indices:
                    random_indic = random.randint(0, individual.sudoku.size - 1)
                    
                    #we change order of random_inc and i and exchange i with j because we want to change the column
                    if ((random_indic, j)) not in individual.sudoku.fixed_indices and (individual.representation[i][j] in individual.sudoku.possible_entries[random_indic][j]) and (individual.representation[random_indic][j] in individual.sudoku.possible_entries[random_indic][j]):
                        help = individual.representation[i][j]
                        individual.representation[i][j] = individual.representation[random_indic][j]
                        individual.representation[random_indic][j] = help
    return individual
                        
                    
def box_exchange_mutate(individual, mutation_rate):
    #replaces two numbers within a box with each other(if its not a fixed index)
    #also we need to be careful that the numbers are in the possible entries of the other cell
    for i in range(individual.sudoku.size):
        for j in range(individual.sudoku.size):
            if random.uniform(0, 1) <= mutation_rate:
                if (i, j) not in individual.sudoku.fixed_indices:
                    #because of the boxes it gets more complex and we work with two random numbers in order to change boxes and columns
                    box_i = i // individual.sudoku.box_size[1]
                    box_j = j // individual.sudoku.box_size[0]
                    random_i = random.randint(0, individual.sudoku.box_size[1] - 1)
                    random_j = random.randint(0, individual.sudoku.box_size[0] - 1)
                    new_i = box_i * individual.sudoku.box_size[1] + random_i
                    new_j = box_j * individual.sudoku.box_size[0] + random_j
                    #if numbers not in template and possible entries match
                    if (new_i, new_j) not in individual.sudoku.fixed_indices and (individual.representation[i][j] in individual.sudoku.possible_entries[new_i][new_j]) and (individual.representation[new_i][new_j] in individual.sudoku.possible_entries[i][j]):
                        #we swap
                        individual.representation[i][j], individual.representation[new_i][new_j] = individual.representation[new_i][new_j], individual.representation[i][j]
    return individual

def mixed_exchange_mutate(individual, mutation_rate):
    #1/3 chance each of doing a row mutation, column mutation or box mutation
    
    random_percentage = random.uniform(0,1)
    
    if float(1/3) > random_percentage:
        individual = row_exchange_mutate(individual, mutation_rate)
        return individual
    
    elif float(2/3) > random_percentage:
        individual = column_exchange_mutate(individual, mutation_rate)
        
    elif 1 > random_percentage:
        individual = box_exchange_mutate(individual, mutation_rate)
        return individual
    
    else:
        raise TypeError('something went wrong')
    
    
def a_bit_of_all_mutation(individual, mutation_rate):
    #1/2 chance each of doing a flip mutation or a mixed exchange mutation
    random_percentage = random.uniform(0,1)
    
    if random_percentage > 0.5:
        individual = flip_mutation(individual, mutation_rate)
        return individual
    
    else:
        individual = mixed_exchange_mutate(individual, mutation_rate)
        return individual