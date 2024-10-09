import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from deap import base, creator, tools

np.random.seed(42)
X = np.random.randn(500, 1000)
y = np.random.randint(5, size=500)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("attr_bool", np.random.randint, 2)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=1000)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)
population = toolbox.population(n=50)
ngen, cxpb, mutpb = 10, 0.5, 0.2
for gen in range(ngen):
    offspring = toolbox.select(population, len(population))
    offspring = list(map(toolbox.clone, offspring))
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if np.random.rand() < cxpb:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values
    for mutant in offspring:
        if np.random.rand() < mutpb:
            toolbox.mutate(mutant)
            del mutant.fitness.values
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = [(accuracy_score(y_test, SVC(kernel='linear', C=1, decision_function_shape='ovo').fit(
        X_train[:, [i for i, bit in enumerate(ind) if bit]], y_train
    ).predict(X_test[:, [i for i, bit in enumerate(ind) if bit]])),) for ind in invalid_ind]
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    population[:] = toolbox.select(population + offspring, len(population))
    fits = [ind.fitness.values[0] for ind in population if ind.fitness.valid]
    print(f"  Min {min(fits)}, Max {max(fits)}, Avg {sum(fits) / len(fits)}, Std {abs(sum(x*x for x in fits) / len(fits) - (sum(fits) / len(fits))**2)**0.5}")
best_individual = tools.selBest(population, 1)[0]