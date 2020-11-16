from random import randint, random
from population import Population, Individual
from points import images

WIDTH  = 13
HEIGHT = 13

def random_image(size:int):
    return [randint(0,1) for i in range(size)]
        

class GeneticImage():
    def __init__(self, image:list, max_population:int, generations:int, crossover_rate:float, mutation_rate:float):
        self.target         = image             # Lista de pontos representando a imagem
        self.max_population = max_population    # Tamanho da populacao
        self.generations    = generations       # Numero de geracoes
        self.crossover_rate = crossover_rate    # Taxa de crossover
        self.mutation_rate  = mutation_rate     # Taxa de mutacao
        self.population     = self.generate_population(max_population)


    def get_fitness(self, target:list, image:list):
        '''
        O fitness e calculado comparando cada pixel dos dois vetores.\n
        Cada pixel e representado por um bit (0-Preto, 1-Branco)
        '''
        fitness = 0
        for pixel1, pixel2 in zip(target, image):
            if(pixel1==pixel2):
                fitness+=1
        return fitness 
    
    def generate_population(self, max_population:int)->Population:
        '''
        Gera uma populacao inicial completamente aleatoria.\n
        Uma populacao e composta por solucoes diferentes representando individuos,
        para esse caso cada solucao representa uma imagem.
        '''
        population = []
        for i in range(self.max_population):
            points  = random_image(len(self.target))
            fitness = self.get_fitness(self.target, points)
            population.append(Individual(points, fitness))
        return Population(population)


    def mutate(self, dna:Individual):
        '''
        O operador de mutacao inverte um bit escolhido aleatoriamente dentro\n
        do cromossomo de um individuo, respeitando uma taxa de mutacao.
        '''
        if(random() < self.mutation_rate):
            num1 = randint(0, len(dna.chromosome)-1)
            gene = dna.chromosome[num1]
            dna.chromosome[num1] = abs(gene-1)
            dna.fitness = self.get_fitness(target, dna.chromosome)


    def crossover(self, dna1:Individual, dna2:Individual)->Individual:
        '''
        O operador de crossover utiliza dois cromossomos para gerar um novo cromossomo
        representando um filho.\n 
        Um ponto de corte e escolhido aleatoriamente para separar a cadeia
        de bits dos pais e o filho e formado com parte dos genes de cada pai.
        '''
        if(random() > self.crossover_rate): return dna1
        
        cutoff = randint(0, len(dna1.chromosome)-1)
        father_genes = dna1.chromosome[0:cutoff]
        mother_genes = dna2.chromosome[cutoff:]
        chromosome   = father_genes + mother_genes
        fitness      = self.get_fitness(target, chromosome)
        return Individual(points=chromosome, fitness=fitness)


    def new_generation(self)->Population:
        '''
        Obtem uma nova populacao de individuos melhorados.\n
        O metodo de selecao elitista e utilizado para preservar uma pequena
        parcela dos melhores individuos da geracao anterior.\n
        Dois individuos sao escolhidos aleatoriamente dentro da populacao e 
        os operadores de crossover e mutacao sao aplicados para gerar dois 
        novos individuos respeitando o tamanho da populacao inicial.
        '''
        wheel = self.population.elitist_selection() 
        # Seleciona 20% dos melhores individuos da roleta
        best_dnas = int(0.8*len(wheel))
        new_population = wheel[best_dnas:]

        while(len(new_population) < self.max_population):
            index1 = randint(0, (len(wheel)-1))
            index2 = randint(0, (len(wheel)-1))
            father = wheel[index1]
            mother = wheel[index2]
            child1 = self.crossover(father, mother)
            child2 = self.crossover(mother, father)
            self.mutate(child1)
            self.mutate(child2)
            
            new_population.append(child1)
            new_population.append(child2)
        return Population(new_population)


    def run(self):
        print(f'\n{self.generations} generations')
        for i in range(self.generations):
            self.population = self.new_generation()

        best = self.population.elitist_selection()[-1]
        best.plot(rows=WIDTH)


if(__name__=='__main__'):
    target = images['alien']
    
    for i in range(1,4):
        GeneticImage(image=target, max_population=100, generations=100*i, crossover_rate=0.75, mutation_rate=0.08).run()