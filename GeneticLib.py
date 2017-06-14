class Solver(object):

    def __init__(self, maxGenerations, mutationRate, fitnessFunc):
        self.maxGenerations = maxGenerations
        self.mutationRate = mutationRate
        self.fitnessFunc = fitnessFunc

    def solve(self):
        return self.fitnessFunc()