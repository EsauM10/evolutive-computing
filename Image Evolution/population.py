from numpy import array_split


emoji = {0:'⬛️', 1:'⬜️'}

class Individual():
    def __init__(self, points:list, fitness:float):
        self.chromosome  = points
        self.fitness     = fitness
    
    def plot(self, rows):
        for row in array_split(self.chromosome, rows):
            for col in row:
                print(emoji[col], end='')
            print('')


class Population():
    def __init__(self, chromosomes:list):
        self.chromosomes = chromosomes
        
    def elitist_selection(self):
        return sorted(self.chromosomes, key= lambda dna:dna.fitness)
