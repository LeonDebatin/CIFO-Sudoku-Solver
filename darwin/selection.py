import random
import copy
import math

def select_parents(population, selection_method=None, tournament_size = None, T=None):
    #function that selects parents based on the selection method
    
    parents = []
    
    if selection_method == 'fps':
        for i in range(population.size):
            parents.append(fps(population))
    
    if selection_method == 'tournament':
        for i in range(population.size):
                parents.append(tournament_selection(population, tournament_size))
    
    if selection_method == 'boltzmann':
        for i in range(population.size):
            parents.append(boltzmann_selection(population, T))
    
    return parents


def fps(population):
    # Fitness proportionate selection implementation
    # To realize the 'roulette wheel' for parent selection, we adapt the template from the practicals for minimization problems

    # Therefore we get the total fitness
    total_fitness = sum([1 / individual.fitness for individual in population.individuals])

    # A random float between 0 and 1 (0-100%)
    r = random.uniform(0, 1)

    # Initialize position
    position = 0

    #loop to simulate roulette wheel
    for individual in population.individuals: 
        # While iterating over all individuals, we calculate their probability of being chosen
        prob = (1 / individual.fitness) / total_fitness

        # Add probabilities to the position
        position += prob

        # If the position exceeds the random value, we return the individual
        if position > r:
            return copy.deepcopy(individual)
        
        

def tournament_selection(population, tournament_proportional_size):
    
    #first we get the absolute tournament size based on the given proportion
    tournament_size = int(population.size * tournament_proportional_size)
    
    selected_individuals = []
    
    #we randomly select individuals for the tournament
    for i in range(tournament_size):
        selected_individuals.append(random.randint(0, population.size -1))
        
    #we sort the selected individuals based on their fitness
    selected_individuals = sorted(selected_individuals)
    
    #and return the best
    return copy.deepcopy(population.individuals[selected_individuals[0]])



def boltzmann_selection(population, T):
    
    #the main idea behind the boltzmann is the same as in the fps, except that the size of the slices for the roulette wheel are adapted according to the temperature T
    # for high T, the probabilities are more equal (leads to more exploration), for low T, the probabilities are more unequal (more exploitation)
    #also there is a cooling rate implemented for the solve sudoku function, to adapt the temperature (usually decreases over time)
    
    for _ in range(population.size ):
        fitnesses = [individual.fitness for individual in population.individuals]
    
        min_fitness = min(fitnesses)
        #normalize using the minimum fitness (best fitness) and substracting the fitness of each individual from it, therefore transforming it into maximization problem
        normalized_fitnesses = [min_fitness - fitness for fitness in fitnesses]
        
        #resizing the slices using the exponential function
        exponentials = [math.exp(fitness / T) for fitness in normalized_fitnesses]

        #calculating propabilities for each in individual
        total_exponential = sum(exponentials)
        probabilities = [exp / total_exponential for exp in exponentials]
        
        
        position = 0
        r = random.uniform(0,1)
        index = 0
        
        #roulette wheel for the propabilities regarding the changes through the boltzmann selection
        for prob in probabilities:
            # While iterating over all individuals, we calculate their probability of being chosen
            position += prob

            # If the position exceeds the random value, we return the individual
            if position > r:
                return copy.deepcopy(population.individuals[index])
            
            index +=1