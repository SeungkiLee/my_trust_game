# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'my_beauty'
    players_per_group = 5
    num_rounds = 1

    winner_payoff = c(100)
    guess_max = 100
    fixed_pay =c(10)

    training_question_1_win_pick_correct =10
    training_question_1_my_payoff_correct =c(50)
    training_1_question_maximum_pick = 100
    training_1_maximum_offered_points = c(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    two_third_guesses = models.FloatField()
    best_guess = models.FloatField()
    tie = models.BooleanField(initial=False)

    def set_payoffs(self):
        players = self.get_players()
        self.two_third_guesses = (
            (2/3) * sum(p.guess_value for p in players) / len(players)
        )

    candidates = []
    smallest_difference_so_far = Constants.guess_max + 1    # initialize to largest possible difference
    tie = False
    for p in self.get_players():
        p.payoff = 0
        p.is_winner = False     #initialize to false
        difference = abs(p.guess_value - self.two_third_guesses)
        if difference < smallest_difference_so_far:
            tie = False
            candidates = [p]
            smallest_difference_so_far = difference
        elif difference == smallest_difference_so_far:
            tie = True
            candidates.append(p)




class Player(BasePlayer):
    pass