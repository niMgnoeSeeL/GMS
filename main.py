from gym import Player, Gym
from gatool import get_toolbox
import random


def repr_best_sol(pop, player_list, num_round, num_court, num_sol=20):
    gym_list = []
    for ind in pop:
        sorted_player = [player_list[i] for i in ind]
        gym_list.append(Gym(num_round, num_court, sorted_player))
    gym_list.sort(key=lambda x: x.score())
    for idx in range(num_sol):
        print('Sol{}: '.format(idx + 1) + str(gym_list[idx]))


if __name__ == "__main__":
    num_round = 5
    num_court = 4
    num_player = 35
    player_list = []
    for idx in range(num_player):
        name = 'Player{}'.format(idx)
        sex = random.randint(0, 1)
        if sex:
            level = random.randint(1, 4)
        else:
            level = random.randint(3, 6)
        player_list.append(Player(idx, name, sex, level))

    for player in player_list:
        print(player)

    toolbox = get_toolbox(num_player, num_round * num_court * 4)

    pop_size, gen_num = 100, 1000
    cx_twopoint_prob, cx_team_prob, mut_prob, next_gen_prob = 0.5, 0, 0.5, 0.2
    pop = toolbox.population(n=pop_size)

    fitnesses = list(
        map(
            lambda ind: toolbox.evaluate(ind, num_round, num_court, player_list
                                         ), pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    for g in range(gen_num):
        if g % 10 == 0:
            print('GEN{}'.format(g))
            repr_best_sol(pop, player_list, num_round, num_court)

        offspring = list(map(toolbox.clone, pop))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cx_twopoint_prob:
                toolbox.twopointmate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cx_team_prob:
                toolbox.teammate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mut_prob:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(
            map(
                lambda ind: toolbox.evaluate(ind, num_round, num_court,
                                             player_list), invalid_ind))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop_survivor = toolbox.select(pop, int(pop_size * next_gen_prob))
        offspring_survivor = toolbox.select(
            offspring, pop_size - int(pop_size * next_gen_prob))
        pop = pop_survivor + offspring_survivor

    print('[FINAL]')
    repr_best_sol(pop, player_list, num_round, num_court)
