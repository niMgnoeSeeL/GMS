import random

from deap import base, creator, tools
from gym import Gym


def evaluate(individual, num_round, num_court, player_list):
    sorted_player = [player_list[i] for i in individual]
    return Gym(num_round, num_court, sorted_player).evaluate(),


def get_toolbox(idx_size, ind_size):

    creator.create('FitnessMin', base.Fitness, weights=(-1.0, ))
    creator.create('Individual', list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register('indices', random.choice, range(idx_size))
    toolbox.register('individual', tools.initRepeat, creator.Individual,
                     toolbox.indices, n=ind_size)

    toolbox.register('population', tools.initRepeat, list, toolbox.individual)

    toolbox.register('mate', tools.cxTwoPoint)
    toolbox.register('mutate', tools.mutShuffleIndexes, indpb=0.1)
    toolbox.register('select', tools.selTournament, tournsize=3)
    toolbox.register('evaluate', evaluate)
    toolbox.register('selBest', tools.selBest, k=1)

    return toolbox
