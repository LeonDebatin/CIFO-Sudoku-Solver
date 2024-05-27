from darwin.charles import Population
from darwin.evolution import evolve
import csv
import time


def solve_sudoku(   population_size,
                    sudoku, 
                    generations, 
                    selection_method = None,
                    tournament_size = None,
                    T = None,
                    cooling_rate = None,
                    elitism = None,
                    elitism_percentage = None,
                    crossover_rate = None,
                    crossover_method = None,
                    mutation_rate = None,
                    mutation_method = None, 
                    log=False, 
                    log_name=None, 
                    generations_earlystop= None
                    ):
    
    #
    time_start = time.time()
    
    #mutation_rate_start and help are needed for the second early_stopping variant in which we increase the mutation rate for a couple of epochs in order
    #to escape local minima
    mutation_rate_start = mutation_rate
    help = 0
    
    #generate population 
    p = Population(size = population_size, sudoku=sudoku)
    p.best_fitness = float('inf')
    p.average_fitness = float('inf')
    best_fitness_history = []
    
    #start log if log wit header
    if log:
        name = 'logs/' + log_name + '.csv'
        with open(name, 'w', newline='\n') as csvfile:
            w = csv.writer(csvfile, delimiter=';')
            w.writerow(['generations']+['average_fitness']+['best_fitness']+['time'])
    
    #for each generation we evolve
    for i in range(generations):
        p = evolve( population= p, 
                    selection_method=selection_method, 
                    tournament_size=tournament_size, 
                    T = T,
                    elitism=elitism, 
                    elitism_percentage=elitism_percentage, 
                    crossover_rate= crossover_rate, 
                    crossover_method=crossover_method, 
                    mutation_rate=mutation_rate, 
                    mutation_method=mutation_method)
        
        #then if we have boltzmann selection update the weight
        if selection_method == 'boltzmann':
            T = T * cooling_rate
        
        #if we want to take the log we update our log
        if log:
            with open(name, 'a', newline='\n') as csvfile:
                w = csv.writer(csvfile, delimiter=';')
                w.writerow([i]+[p.average_fitness]+[p.best_fitness]+[time.time() -time_start])
        
        #append the history for best fitness
        best_fitness_history.append(p.best_fitness)
        
        #if we solve the sudoku we return the population
        if p.best_fitness == 0:
            return p
        

        #early_stop version1
        #this version allows to early stop if the best fitness doesnt decrease anymore
        #this was active during random search
        # if (i > generations_earlystop):
        #     if (p.best_fitness == best_fitness_history[-generations_earlystop]):
        #         return p
        
        #version 2    
        #this version allows to change the mutation rate after a certain amount of generations without decrease of the best fitness in the hope to get out of a local optima
        #this was active during solving attemps
        if (i > generations_earlystop):
            if (p.best_fitness == best_fitness_history[-generations_earlystop]) & (help <= 5):
                mutation_rate = 0.25
                help += 1
            
            if (help > 5) :
                mutation_rate = mutation_rate_start
        
            
    return p
    