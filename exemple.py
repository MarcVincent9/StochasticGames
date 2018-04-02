# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 20:58:06 2018

@author: Marc
"""

from Soccer import Soccer
from RockPaperScissors import RockPaperScissors
from Test import Test


game = RockPaperScissors()
#game = Soccer()

pi = [{s: {a: 1/len(game.actions(p, s)) for a in game.actions(p, s)} for s in game.states()} for p in range(game.nb_players())]
test = Test(game, pi)

#test.step(("pierre", "papier"))
#test.step(("N", "W"))

#test.step(tuple(test.chooseAction(i) for i in range(game.nb_players())))game = Soccer()
