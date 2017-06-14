from GeneticLib import Solver

maxGenerations = 100
mutationRate = 0.1
def fitnessFunc():
    return 1

solver = Solver(maxGenerations,mutationRate,fitnessFunc)
ret = solver.solve()
print ret