from player import *
import random
random.seed(1)

if __name__ == "__main__":

    num_player = 12
    player_list = []
    for idx in range(num_player):
        name = 'Player{}'.format(idx)
        sex = random.randint(0, 1)
        level = random.randint(1, 5)
        player_list.append(Player(name, sex, level))

    for player in player_list:
        print(player)