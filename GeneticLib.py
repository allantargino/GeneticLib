from enum import Enum

class Solver(object):

    def __init__(self, maxGenerations, mutationRate, fitnessFunc, crossoverTechnique):
        self.maxGenerations = maxGenerations
        self.mutationRate = mutationRate
        self.fitnessFunc = fitnessFunc
        self.crossoverTechnique = crossoverTechnique

    def solve(self):
        return self.fitnessFunc()

# based on https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)#Techniques
class CrossoverTechnique(Enum):
    SinglePoint = 1
    TwoPoint = 2
    Uniform = 3 
    HalfUniform = 4
    ThreeParent = 5