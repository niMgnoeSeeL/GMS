import math
from scipy import stats

MALE = 0
FEMALE = 1


class Player:
    def __init__(self, idx, name, sex, level):
        self.idx = idx
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

    def get_sex_score(self):
        sex_list = list(map(lambda player: player.sex, self.player_list))
        return abs((sex_list[0] + sex_list[1]) - (sex_list[2] + sex_list[3]))

    def get_level_score(self):
        level_list = list(map(lambda player: player.level, self.player_list))
        return abs((level_list[0] + level_list[1]) -
                   (level_list[2] + level_list[3]))

    def get_set(self):
        return frozenset([player.idx for player in self.player_list])

    def __repr__(self):
        return 'Court{}: [{},{}] vs. [{},{}]'.format(self.court_idx,
                                                     *self.player_list)


class Round:
    def __init__(self, round_idx, num_court, player_list):
        self.round_idx = round_idx
        self.num_court = num_court
        self.court_list = []
        self.player_list = player_list
        self.assign_player()

    def assign_player(self, ):
        for i in range(self.num_court):
            self.court_list.append(
                Court(self.round_idx, i + 1,
                      self.player_list[4 * i:4 * (i + 1)]))

    def get_sex_score(self):
        return sum(map(Court.get_sex_score, self.court_list))

    def get_level_score(self):
        return sum(map(Court.get_level_score, self.court_list))

    def get_dup_score(self):
        dup_dict = {}
        for player in self.player_list:
            if player.name in dup_dict:
                dup_dict[player.name] += 1
            else:
                dup_dict[player.name] = 0
        return sum([v for k, v in dup_dict.items()])

    def get_round_set(self):
        return [court.get_set() for court in self.court_list]

    def __repr__(self):
        ret = 'Round{} (Dup:{}, Sex:{}, Level:{})\n'.format(
            self.round_idx, self.get_dup_score(), self.get_sex_score(),
            self.get_level_score())
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

    def get_sex_score(self):
        return sum(map(Round.get_sex_score, self.round_list))

    def get_level_score(self):
        return sum(map(Round.get_level_score, self.round_list))

    def get_dup_score(self):
        return sum(map(Round.get_dup_score, self.round_list))

    def get_rematch_score(self):
        court_tup_list = []
        for round in self.round_list:
            court_tup_list += round.get_round_set()
        return len(court_tup_list) - len(set(court_tup_list))

    def get_balance_score(self):
        game_cnt_list = list(map(lambda player: player.game, self.player_list))
        return max(game_cnt_list) - min(game_cnt_list)

    def evaluate(self):
        return (self.get_dup_score(), self.get_balance_score(),
                self.get_sex_score(), self.get_rematch_score(),
                self.get_level_score())

    def score(self):
        (dup_score, balance_score, sex_score, rematch_score,
         level_score) = self.evaluate()
        if dup_score:
            return math.inf
        else:
            balance_score += 1
            sex_score += 1
            rematch_score += 1
            level_score += 1
            return (3 / ((1 / sex_score) + (1 / rematch_score) +
                         (1 / level_score))) * (balance_score**2)

    def __repr__(self):
        ret = 'score:{:.2f}'.format(self.score())
        ret += ' (Dup:{}, Balance:{}, Sex:{}, Rematch:{}, Level:{})'.format(
            *self.evaluate())
        # for round in self.round_list:
        #     ret += '\n' + str(round)
        return ret
