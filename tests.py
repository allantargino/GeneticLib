from GeneticLib import CrossoverTechnique, Solver

verbose = False

maxGenerations = 100
mutationRate = 0.1
populationInit = 50
crossoverChild = 10
crossoverTechnique = CrossoverTechnique.TwoPoint

def fitnessFunc():
    return 1

solver = Solver(maxGenerations,mutationRate,fitnessFunc)
ret = solver.solve()
print ret