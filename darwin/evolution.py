from darwin.selection import select_parents
from darwin.crossover import reproduce
from darwin.mutation import mutate
import copy



def evolve( population, 
            selection_method = None,
            tournament_size = None,
            T = None,
            elitism = None,
            elitism_percentage = None,
            crossover_rate = None,
            crossover_method = None,
            mutation_rate = None,
            mutation_method = None
          ):
    
    #we start with selecting the parents
    population.parents = select_parents(population, selection_method=selection_method, tournament_size=tournament_size, T=T)
    #then creating/reproducing the children
    population.children = reproduce(population, crossover_rate=crossover_rate, crossover_method=crossover_method)
    
    #mutating the children
    for i in range(population.size):
            population.children[i] = mutate(population.children[i], mutation_rate=mutation_rate, mutation_method=mutation_method)
    
    #getting the fitness for the individuals and the children
    population.get_fitnesses()
    population.get_fitnesses_for_children()
    
    #then sorting the fitness
    population.sort_individuals()
    population.sort_children()
    
    #if we have elitism we replace the worst children with the best individuals from the population
    if elitism:
        for i in range(int(round(population.size * elitism_percentage))):
            if population.individuals[i].fitness < population.children[-i].fitness:
                population.children[-i] = copy.deepcopy(population.individuals[i])

    #then our children become the new individuals
    for i in range(population.size):
        population.individuals[i] = copy.deepcopy(population.children[i])
    
    #we sort the fitness again
    population.sort_individuals()
    population.get_best_fitness()
    population.get_average_fitness()
        
    return population    
