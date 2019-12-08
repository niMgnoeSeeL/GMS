import random

from deap import base, creator, tools
from gym import Gym


def evaluate(individual, num_round, num_court, player_list, mo=True):
    sorted_player = [player_list[i] for i in individual]
    gym = Gym(num_round, num_court, sorted_player)
    if mo:
        return gym.evaluate()
    else:
        return gym.score(),


def mut_balance(individual, player_size):
    cnt_dict = dict(zip(range(player_size), [0] * player_size))
    for player_idx in individual:
        cnt_dict[player_idx] += 1
    max_cnt = max(cnt_dict.values())
    dup_player_idx_list = []
    for k, v in cnt_dict.items():
        dup_player_idx_list += [k] * (max_cnt - v + 1)
    for player_idx in range(player_size):
        if cnt_dict[player_idx] == max_cnt:
            ind_with_idx = zip(range(len(individual)), individual)
            player_idx_in_ind = [
                idx for idx, player in ind_with_idx if player == player_idx
            ]
            change_idx = random.choice(player_idx_in_ind)
            individual[change_idx] = random.choice(dup_player_idx_list)
    cnt_dict = dict(zip(range(player_size), [0] * player_size))
    for player_idx in individual:
        cnt_dict[player_idx] += 1
    return individual


def cx_team(ind1, ind2):
    size = min(len(ind1) / 4, len(ind2) / 4)
    cxpoint1 = random.randint(0, size - 1)
    cxpoint2 = random.randint(0, size - 1)

    ind1[cxpoint1 * 4:(cxpoint1 + 1) *
         4], ind2[cxpoint2 * 4:(cxpoint2 + 1) *
                  4] = ind2[cxpoint2 * 4:(cxpoint2 + 1) *
                            4], ind1[cxpoint1 * 4:(cxpoint1 + 1) * 4]

    return ind1, ind2


def get_toolbox(idx_size, ind_size, mo=True):

    if mo:
        creator.create('FitnessMin',
                       base.Fitness,
                       weights=(-1.0, -1.0, -1.0, -1.0, -1.0))
    else:
        creator.create('FitnessMin', base.Fitness, weights=(-1.0, ))
    creator.create('Individual', list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register('indices', random.choice, range(idx_size))
    toolbox.register('individual',
                     tools.initRepeat,
                     creator.Individual,
                     toolbox.indices,
                     n=ind_size)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)

    toolbox.register('matetwopoint', tools.cxTwoPoint)
    toolbox.register('mateteam', cx_team)
    toolbox.register('mutateuni',
                     tools.mutUniformInt,
                     low=0,
                     up=idx_size - 1,
                     indpb=0.1)
    toolbox.register('mutatebal', mut_balance)
    if mo:
        toolbox.register('select', tools.selNSGA2)
    else:
        toolbox.register('select', tools.selBest)
    toolbox.register('evaluate', evaluate, mo=mo)

    return toolbox
