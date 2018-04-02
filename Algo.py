# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 23:13:47 2018

@author: Marc
"""

class Algo:
    
    def __init__(self, game):
        self.game = game
        
        # strategies of all players (other initializations possible):
        # list (for each player) of dictionaries (for each state) of dictionaries (probability of each action for given state)
        self.pi = [{s: {a: 1/len(self.game.actions()[i]) for a in self.game.actions()[i]}\
                    for s in self.game.states()} for i in range(self.game.nb_players())]
        
        # value of the game for each state
        self.V = {s:0 for s in self.game.states()}
        