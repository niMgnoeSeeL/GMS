import math
from scipy import stats

MALE = 0
FEMALE = 1


class Player:
    def __init__(self, name, sex, level):
        self.name = name
        self.sex = sex
        self.level = level
        self.game = 0

    def __repr__(self):
        return '[{}]{}({},{})'.format('M' if self.sex == MALE else 'F',
                                      self.name, self.level, self.game)

    def inc_game(self):
        self.game += 1

    def reset_game(self):
        self.game = 0


class Court:
    def __init__(self, round_idx, court_idx, player_list):
        self.round_idx = round_idx
        self.court_idx = court_idx
        self.player_list = player_list
        for player in player_list:
            player.inc_game()

    def sex_score(self):
        sex_list = list(map(lambda player: player.sex, self.player_list))
        return abs((sex_list[0] + sex_list[1]) - (sex_list[2] + sex_list[3]))

    def level_score(self):
        level_list = list(map(lambda player: player.level, self.player_list))
        return abs((level_list[0] + level_list[1]) -
                   (level_list[2] + level_list[3]))

    def evaluate(self):
        return self.sex_score() + self.level_score()

    def __repr__(self):
        return 'Court{}: [{},{}] vs. [{},{}] (fitness: {})'.format(
            self.court_idx, *self.player_list, self.evaluate())


class Round:
    def __init__(self, round_idx, num_court, player_list):
        self.round_idx = round_idx
        self.num_court = num_court
        self.court_list = []
        self.assign_player(player_list)

    def assign_player(self, player_list):
        for i in range(self.num_court):
            self.court_list.append(
                Court(self.round_idx, i + 1, player_list[4 * i:4 * (i + 1)]))

    def evaluate(self):
        return sum(map(Court.evaluate, self.court_list))

    def __repr__(self):
        ret = 'Round{} (fitness:{})\n'.format(self.round_idx, self.evaluate())
        cnt = 1
        for court in self.court_list:
            ret += str(court) + '\n'
            cnt += 1
        return ret


class Gym:
    def __init__(self, num_round, num_court, player_list):
        self.num_round = num_round
        self.num_court = num_court
        self.player_list = player_list
        self.round_list = []
        self.assign_player()

    def assign_player(self):
        for player in self.player_list:
            player.reset_game()

        for i in range(self.num_round):
            self.round_list.append(
                Round(
                    i + 1, self.num_court,
                    self.player_list[(4 * self.num_court) *
                                     i:(4 * self.num_court) * (i + 1)]))

    def get_round_score(self):
        return sum(map(Round.evaluate, self.round_list))

    def get_balance_score(self):
        game_cnt_list = list(map(lambda player: player.game, self.player_list))
        return max(game_cnt_list) - min(game_cnt_list)

    def evaluate(self):
        round_score = self.get_round_score()
        balance_score = self.get_balance_score()
        if not round_score or not balance_score:
            score = math.inf
        else:
            score = stats.hmean(
                [self.get_round_score(),
                 self.get_balance_score()])
        return score

    def __repr__(self):
        ret = 'fitness:{} (Round:{} + Balance:{})\n'.format(
            self.evaluate(), self.get_round_score(), self.get_balance_score())
        for round in self.round_list:
            ret += str(round) + '\n'
        return ret
