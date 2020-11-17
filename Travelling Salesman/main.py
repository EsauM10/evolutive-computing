import math
from population import City, Individual, Population
import matplotlib.pyplot as plt
from random import random, randint

WIDTH  = 500
HEIGHT = 500


def generate_cities(max_cities:int)->list:
    '''
    Retorna uma lista com pontos aleatórios representando cidades
    '''
    return [City(randint(0, WIDTH), randint(0, HEIGHT)) for i in range(max_cities)]


def random_bits(size:int)->list:
    '''
    Retorna uma lista de bits aleatórios
    '''
    return [randint(0,1) for i in range(size)]



class GeneticAlgorithm():
    def __init__(self, cities:list, max_population:int, generations:int, crossover_rate:float, mutation_rate:float):
        self.cities          = cities           # Lista de pontos
        self.max_population  = max_population   # Tamanho da populacao
        self.generations     = generations      # Numero de geracoes
        self.crossover_rate  = crossover_rate   # Taxa de crossover
        self.mutation_rate   = mutation_rate    # Taxa de mutacao
        self.population      = self.generate_population(max_population)
        
    
    def generate_population(self, max_population:int)->Population:
        '''
        Gera uma população inicial aleatória.\n
        Cada indivíduo na população é representado por um conjunto de cidades
        que devem ser percorridas respeitando o arranjo inicial.\n
        Para criar indivíduos diferentes é necessário permutar a ordem que
        as cidades devem ser percorridas.
        '''
        permut_rate = 1.0
        population  = []
        while(len(population) < max_population):
            if(random() < permut_rate):
                cities = self.permut(self.cities)
                population.append(Individual(cities))
        return Population(population)
            

    def permut(self, chromosome:list)->list:
        '''
        Permuta duas posições escolhidas aleatoriamente dentro de um cromossomo.
        '''
        dna = chromosome
        index1, index2 = None, None
        while (index1 == index2):
            index1 = randint(0, len(dna)-1)
            index2 = randint(0, len(dna)-1)
        dna[index1], dna[index2] = dna[index2], dna[index1]
        return dna


    def crossover(self, dna1:Individual, dna2:Individual)->Individual:
        '''
        O crossover baseado em ordem utiliza uma máscara de bits gerada aleatoriamente.\n
        Os genes do dna1 são copiados para o filho referentes às posições onde a 
        máscara de bits é igual a 1.
        Uma sublista é criada para mapear os genes do dna1 onde a máscara é igual a 0.
        Essa sublista é ordenada de acordo com a ordem que aparece no dna1.\n
        Os genes dessa sublista são colocados nos espaços vazios do filho formando um
        novo cromossomo.
        '''
        if(random() > self.crossover_rate): return dna1

        dna1, dna2 = dna1.chromosome, dna2.chromosome
        mask     = random_bits(len(dna1))
        child    = [gene if(bit==1) else None for (gene,bit) in zip(dna1,mask)]
        sub_list = [num for num in dna2 if(num not in child)]
        sub_list.reverse()

        for i in range(len(child)):
            if(child[i]==None): child[i] = sub_list.pop()
        return Individual(child)


    def new_generation(self)->Population:
        '''
        Retorna uma nova população de indivíduos mais adaptados.
        '''
        wheel = self.population.elitist_selection() 
        best_dnas = int(0.8*len(wheel)) # 20% dos melhores indivíduos
        new_population = wheel[best_dnas:]

        while(len(new_population) < self.max_population):
            index1 = randint(0, (len(wheel)-1))
            index2 = randint(0, (len(wheel)-1))
            father = wheel[index1]
            mother = wheel[index2]
            child1 = self.crossover(father, mother)
            child2 = self.crossover(mother, father)
            child1.mutate(self.mutation_rate, self.permut)
            child2.mutate(self.mutation_rate, self.permut)
            
            new_population.append(child1)
            new_population.append(child2)
        return Population(new_population)

    def run(self):
        generation = 0
        for i in range(self.generations):
            generation = i+1
            self.population = self.new_generation()
        
        best = self.population.elitist_selection()[-1]
        best.plot(generation) 
 

if(__name__=='__main__'):
    # Cidades geradas aleatoriamente
    #cities = generate_cities(20)
    cities = [City(200,100),City(150,120),City(120,150),City(110,200),City(120,250),City(150,280),City(200,300),City(250,280),City(280,250),City(300,200)]
    
    ga = GeneticAlgorithm(cities=cities, max_population=100, generations=1000, crossover_rate=0.8, mutation_rate=0.01)
    ga.run()
    