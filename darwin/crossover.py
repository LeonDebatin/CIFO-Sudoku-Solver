import random
import copy
from darwin.sudoku import rows_to_boxes, rows_to_columns, boxes_to_rows, columns_to_rows



def reproduce(population, crossover_rate=None, crossover_method=None):
    #reproduce function that returns a pair of children using the crossover function
    children=[]
    
    for i in range(0, population.size, 2):
        children1, children2 = crossover(population.parents[i], population.parents[i+1], crossover_rate=crossover_rate, crossover_method=crossover_method)
        children.append(children1)
        children.append(children2)
        
    return children



def crossover(parent1, parent2, crossover_rate = None, crossover_method = None):
    # choses crossover method based on the provided crossover method
    offspring1 = copy.deepcopy(parent1)
    offspring2 = copy.deepcopy(parent2)
    
    if crossover_rate < random.uniform(0,1):
        return offspring1, offspring2
    
    elif crossover_method == 'mixed_single_point_crossover':
        offspring1, offspring2 = row_multi_point_crossover(parent1=parent1, parent2=parent2, offspring1=offspring1, offspring2=offspring2)
        return offspring1, offspring2
    
    elif crossover_method == 'mixed_multi_point_crossover':
        offspring1, offspring2 = row_multi_point_crossover(parent1=parent1, parent2=parent2, offspring1=offspring1, offspring2=offspring2)
        return offspring1, offspring2
    
    elif crossover_method == 'uniform_crossover':
        offspring1, offspring2 = uniform_crossover(parent1=parent1, parent2 = parent2, offspring1=offspring1, offspring2=offspring2)
        return offspring1, offspring2
    
    elif crossover_method == 'a_bit_of_all_crossover':
        offspring1, offspring2 = a_bit_of_all_crossover(parent1=parent1, parent2 = parent2, offspring1=offspring1, offspring2=offspring2)
        return offspring1, offspring2
    
    else:
        raise TypeError('Provide crossover_method!')



def row_single_point_crossover(parent1, parent2, offspring1, offspring2):
    #row wise single point crossover
    #there will be nice visualizatiosn in the report
    crossover_point = random.randint(1, parent1.sudoku.size-1)
    offspring1.representation = parent1.representation[:crossover_point] + parent2.representation[crossover_point:]
    offspring2.representation = parent2.representation[:crossover_point] + parent1.representation[crossover_point:]
    
    return offspring1, offspring2


def column_single_point_crossover(parent1, parent2, offspring1, offspring2):
    
    #we change to a row wise perspective, do the row wise single point crossover and then transpose back
    parent1.representation = columns_to_rows(parent1.representation)
    parent2.representation = columns_to_rows(parent2.representation)
    offspring1.representation = columns_to_rows(offspring1.representation)
    offspring2.representation = columns_to_rows(offspring2.representation)
    
    #rowwise crossover
    offspring1, offspring2 = row_single_point_crossover(parent1, parent2, offspring1=offspring1, offspring2=offspring2)
    
    #transpose back
    offspring1.representation = rows_to_columns(offspring1.representation)
    offspring2.representation = rows_to_columns(offspring2.representation)
    return offspring1, offspring2



def box_single_point_crossover(parent1, parent2, offspring1, offspring2):
    
    # Convert parents' grids into boxes
    parent1.representation = boxes_to_rows(parent1.representation, parent1.box_size)
    parent2.representation = boxes_to_rows(parent2.representation, parent2.box_size)
    offspring1.representation = boxes_to_rows(offspring1.representation, offspring1.box_size)
    offspring2.representation = boxes_to_rows(offspring2.representation, offspring2.box_size)
    
    #rowwise crossover
    offspring1, offspring2 = row_multi_point_crossover(parent1, parent2, offspring1=offspring1, offspring2=offspring2)
    
    #transpose back
    offspring1.representation = rows_to_boxes(offspring1.representation, offspring1.box_size)
    offspring2.representation = rows_to_boxes(offspring2.representation, offspring2.box_size)

    return offspring1, offspring2


def mixed_single_point_crossover(parent1, parent2, offspring1, offspring2):
    #mixed method with 1/3 chance each
    random_percentage = random.uniform(0,1)
    
    if float(1/3) > random_percentage:
        offspring1, offspring2 = row_single_point_crossover(parent1=parent1, parent2=parent2, offspring1=offspring1, offspring2=offspring2)
        return offspring1, offspring2
    
    elif float(2/3) > random_percentage:
        offspring1, offspring2 = column_single_point_crossover(parent1=parent1, parent2 = parent2, offspring1=offspring1, offspring2=offspring2)
        return offspring1, offspring2
                                                
    elif 1 >= random_percentage:
        offspring1, offspring2 = box_single_point_crossover(parent1=parent1, parent2 = parent2, offspring1=offspring1, offspring2=offspring2)
        return offspring1, offspring2
    
    else:
        raise TypeError('Something went wrong!')


def row_multi_point_crossover(parent1, parent2, offspring1, offspring2):
    #multipoint crossover
    
    
    crossover_points = []
    
    #we flip a coin each time from 1 to the total size -1
    for i in range(1, parent1.sudoku.size-1):
        if random.uniform(0,1) > 0.5:
            crossover_points.append(i)
    
    #the last row has to be a fixed crossover point for sure to ensure the sudoku stays the same size
    crossover_points.append(parent1.sudoku.size)
    
    #the first row will stay the same for each offspring
    offspring1.representation = parent1.representation[:crossover_points[0]]
    offspring2.representation = parent2.representation[:crossover_points[0]]
    
    #then we append the representation, for each crossover point we flip from which parent the next part should come
    for i in range(1,len(crossover_points)):
        
        if random.uniform(0,1) > 0.5:
            offspring1.representation = offspring1.representation + parent1.representation[crossover_points[i-1]:crossover_points[i]]
            offspring2.representation = offspring2.representation + parent2.representation[crossover_points[i-1]:crossover_points[i]]
    
        else:
            offspring1.representation = offspring1.representation + parent2.representation[crossover_points[i-1]:crossover_points[i]]
            offspring2.representation = offspring2.representation + parent1.representation[crossover_points[i-1]:crossover_points[i]]
    
    return offspring1, offspring2


def column_multi_point_crossover(parent1, parent2, offspring1, offspring2):
    
    #again we get the row perspective for the columns and use the rowwise function, then transpose back
    
    #transpose matrix
    parent1.representation = columns_to_rows(parent1.representation)
    parent2.representation = columns_to_rows(parent2.representation)
    offspring1.representation = columns_to_rows(offspring1.representation)
    offspring2.representation = columns_to_rows(offspring2.representation)
    
    #rowwise crossover
    offspring1, offspring2 = row_multi_point_crossover(parent1, parent2, offspring1=offspring1, offspring2=offspring2)
    
    #transpose back
    offspring1.representation = rows_to_columns(offspring1.representation)
    offspring2.representation = rows_to_columns(offspring2.representation)
    return offspring1, offspring2



def box_multi_point_crossover(parent1, parent2, offspring1, offspring2):
    
    # same principle for the boxes
    parent1.representation = boxes_to_rows(parent1.representation, parent1.sudoku.box_size)
    parent2.representation = boxes_to_rows(parent2.representation, parent2.sudoku.box_size)
    offspring1.representation = boxes_to_rows(offspring1.representation, offspring1.sudoku.box_size)
    offspring2.representation = boxes_to_rows(offspring2.representation, offspring2.sudoku.box_size)
    
    #rowwise crossover
    offspring1, offspring2 = row_multi_point_crossover(parent1, parent2, offspring1=offspring1, offspring2=offspring2)
    
    #transpose back
    offspring1.representation = rows_to_boxes(offspring1.representation, offspring1.sudoku.box_size)
    offspring2.representation = rows_to_boxes(offspring2.representation, offspring2.sudoku.box_size)

    return offspring1, offspring2


def mixed_multi_point_crossover(parent1, parent2, offspring1, offspring2):
    #a mixed function that with 1/3 chance each selects one of the multipoint crossover methods
    random_percentage = random.uniform(0,1)
    
    if float(1/3) > random_percentage:
        offspring1, offspring2 = row_multi_point_crossover(parent1=parent1, parent2=parent2, offspring1=offspring1, offspring2=offspring2)
        return offspring1, offspring2
    
    elif float(2/3) > random_percentage:
        offspring1, offspring2 = column_multi_point_crossover(parent1=parent1, parent2 = parent2, offspring1=offspring1, offspring2=offspring2)
        return offspring1, offspring2
                                                
    elif 1 >= random_percentage:
        offspring1, offspring2 = box_multi_point_crossover(parent1=parent1, parent2 = parent2, offspring1=offspring1, offspring2=offspring2)
        return offspring1, offspring2
    
    
    else:
        raise TypeError('Something went wrong!')

def uniform_crossover(parent1, parent2, offspring1, offspring2):
    #uniform crossover that coinflips for each cell from which parent the value for this cell should come, and for the other child it will be the opposite
    for i in range(parent1.sudoku.size):
        for j in range(parent1.sudoku.size):
            #if (i,j) not in parent1.fixed_indices:
            if random.uniform(0,1) > 0.5:
                offspring1.representation[i][j] = parent1.representation[i][j]
                offspring2.representation[i][j] = parent2.representation[i][j]
            else:
                offspring1.representation[i][j] = parent2.representation[i][j]
                offspring2.representation[i][j] = parent1.representation[i][j]

    return offspring1, offspring2


def a_bit_of_all_crossover(parent1, parent2, offspring1, offspring2):
    #50% chance of mixed_multi_point_crossover, 50% chance uniform crossover
    
    random_percentage = random.uniform(0,1)
    
    if random_percentage > 0.5:
        offspring1, offspring2 = mixed_multi_point_crossover(parent1=parent1, parent2 = parent2, offspring1=offspring1, offspring2=offspring2)
        return offspring1, offspring2

    else:
        offspring1, offspring2 = uniform_crossover(parent1=parent1, parent2 = parent2, offspring1=offspring1, offspring2=offspring2)
        return offspring1, offspring2