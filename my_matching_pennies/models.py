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
    name_in_url = 'my_matching_pennies'
    players_per_group = 2   #sequentially split players into groups of size 2
    num_rounds = 4  #number of rounds (repeated game)
    stakes = c(100) #total payoff


class Player(BasePlayer):

    penny_side = models.CharField(  #getting an information of choices
        choices=['Heads', 'Tails'], #choice is used to constrain players to a predefined list
        widget=widgets.RadioSelect()    #providing a form to choose
    )

    is_winner = models.BooleanField()   #record 1, if this player won this round

    def role(self): #defining a role of the player
        if self.id_in_group ==1:    #id_in_group: an intager which indicates each player's attribute
            return 'Mismatcher'
        if self.id_in_group==2:
            return 'Matcher'


class Subsession(BaseSubsession):

    def before_session_starts(self):
        if self.round_number == 1:  #define the 'paying_round' in inital stage
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round
        if self.round_number == 3:  #reverse the roles in 3rd round
            # reverse the roles
            for group in self.get_groups():
                players = group.get_players()   #'group.get_player' gives the ordered list of players in each group (e.g. [P1, P2])
                players.reverse()   #[P1, P2) -> [P2, P1]
                group.set_players(players)  #Set this as the new group order
        if self.round_number > 3:
            self.group_like_round(3)    #In round4(or henceforth), we copy the group structure from round3


class Group(BaseGroup):


    def set_payoffs(self):
        matcher = self.get_player_by_role('Matcher')    #The argument to this method is a string that looks up the player by their role value.
        mismatcher = self.get_player_by_role('Mismatcher')

        #Decide the 'model.BooleanField()'
        if matcher.penny_side == mismatcher.penny_side:
            matcher.is_winner = True    #matcher has its boolean field of 'is_winner' as 1(True)
            mismatcher.is_winner = False    #matcher has its boolean field of 'is_winner' as 0(False)
        else:
            matcher.is_winner = False
            mismatcher.is_winner = True

        for player in [mismatcher, matcher]:
            if (self.subsession.round_number ==
                self.session.vars['paying_round'] and player.is_winner):
                    player.payoff = Constants.stakes
            else:
                player.payoff = c(0)