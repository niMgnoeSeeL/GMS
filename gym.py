MALE = 0
FEMALE = 1


class Player:
    def __init__(self, name, sex, level):
        self.name = name
        self.sex = sex
        self.level = level

    def __repr__(self):
        return '{}({},{})'.format(self.name, 'M' if self.sex == MALE else 'F',
                                  self.level)


class Court:
    def __init__(self, player_list):
        self.player_list = player_list

    def sex_score(self):
        sex_list = list(map(lambda player: player.sex, self.player_list))
        return abs((sex_list[0] + sex_list[1]) - (sex_list[2] + sex_list[3]))

    def level_score(self):
        level_list = list(map(lambda player: player.level, self.player_list))
        return abs((level_list[0] + level_list[1]) -
                   (level_list[2] + level_list[3]))

    def evaluate(self):
        return self.sex_score() + self.level_score()


class Gym:
    def __init__(self):
        super().__init__()
