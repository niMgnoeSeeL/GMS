from gym import Player, Gym
from gatool import get_toolbox
import random


def repr_best_sol(toolbox, player_list, num_round, num_court):
    best_sol = toolbox.selBest(pop)[0]
    sorted_player = [player_list[i] for i in best_sol]
    return str(Gym(num_round, num_court, sorted_player))


if __name__ == "__main__":
    num_round = 5
    num_court = 4
    num_player = 35
    player_list = []
    for idx in range(num_player):
        name = 'Player{}'.format(idx)
        sex = random.randint(0, 1)
        level = random.randint(1, 5)
        player_list.append(Player(name, sex, level))

    for player in player_list:
        print(player)

    toolbox = get_toolbox(num_player, num_round * num_court * 4)

    NPOP, NGEN, CXPB, MUTPB = 1000, 100, 0.5, 0.2
    pop = toolbox.population(n=NPOP)

    fitnesses = list(
        map(
            lambda ind: toolbox.evaluate(ind, num_round, num_court, player_list
                                         ), pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    for g in range(NGEN):
        print('GEN{}'.format(g + 1) + '\n' +
              repr_best_sol(toolbox, player_list, num_round, num_court))

        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(
            map(
                lambda ind: toolbox.evaluate(ind, num_round, num_court,
                                             player_list), invalid_ind))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring

    best_sol = toolbox.selBest(pop)[0]
    sorted_player = [player_list[i] for i in best_sol]
    print(Gym(num_round, num_court, sorted_player))
