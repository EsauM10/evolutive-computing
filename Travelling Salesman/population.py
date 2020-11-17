import math
import matplotlib.pyplot as plt
from random import random, randint


def distance(city1, city2):
    x = city2.x-city1.x
    y = city2.y-city1.y
    return math.sqrt(x*x + y*y)


def fitness(cities:list):
    '''
    O fitness é calculado somando a distância de uma cidade para outra
    de acordo com a ordem do vetor inicial.\n
    Indivíduos com maior fitness devem ter uma distância total menor.
    '''
    total = 0
    for i in range(len(cities)-1):
        total += distance(cities[i], cities[i+1])
    return 1/total
    

class City():
    def __init__(self, x:float, y:float):
        self.x = x
        self.y = y



class Population():
    def __init__(self, chromosomes:list):
        self.chromosomes = chromosomes
        
    def elitist_selection(self):
        return sorted(self.chromosomes, key= lambda dna:dna.fitness)
        
    

class Individual():
    def __init__(self, cities:list):
         self.chromosome  = cities
         self.fitness = fitness(cities)
        
    
    def mutate(self, mutation_rate:float, permut:object):
        if(random() < mutation_rate):
            self.chromosome = permut(self.chromosome)
            self.fitness = fitness(self.chromosome)


    def plot(self, generation):
        x_points = []
        y_points = []

        for city in self.chromosome:
            x_points.append(city.x)
            y_points.append(city.y)

        plt.plot(x_points, y_points)
        plt.scatter(x_points, y_points, color='purple', label=f'Geração: {generation}')
        plt.legend(loc=2, prop={'size':11})
        plt.show()