import random

from deap import base, creator, tools
from gym import Gym


def evaluate(individual, num_round, num_court, player_list):
    sorted_player = [player_list[i] for i in individual]
    return Gym(num_round, num_court, sorted_player).evaluate()


def cxTeam(ind1, ind2):
    size = min(len(ind1) / 4, len(ind2) / 4)
    cxpoint1 = random.randint(0, size - 1)
    cxpoint2 = random.randint(0, size - 1)

    ind1[cxpoint1 * 4:(cxpoint1 + 1) *
         4], ind2[cxpoint2 * 4:(cxpoint2 + 1) *
                  4] = ind2[cxpoint2 * 4:(cxpoint2 + 1) *
                            4], ind1[cxpoint1 * 4:(cxpoint1 + 1) * 4]

    return ind1, ind2


def get_toolbox(idx_size, ind_size):

    creator.create('FitnessMulit',
                   base.Fitness,
                   weights=(-1.0, -1.0, -1.0, -1.0, -1.0))
    creator.create('Individual', list, fitness=creator.FitnessMulit)

    toolbox = base.Toolbox()
    toolbox.register('indices', random.choice, range(idx_size))
    toolbox.register('individual',
                     tools.initRepeat,
                     creator.Individual,
                     toolbox.indices,
                     n=ind_size)

    toolbox.register('population', tools.initRepeat, list, toolbox.individual)

    toolbox.register('twopointmate', tools.cxTwoPoint)
    toolbox.register('teammate', cxTeam)
    toolbox.register('mutate',
                     tools.mutUniformInt,
                     low=0,
                     up=idx_size - 1,
                     indpb=0.1)
    toolbox.register('select', tools.selNSGA2)
    toolbox.register('evaluate', evaluate)

    return toolbox
