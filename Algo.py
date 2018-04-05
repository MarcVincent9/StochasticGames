# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 23:13:47 2018

@author: Marc
"""

class Algo:
    
    def __init__(self, game):
        self.game = game
        
        # strategies of all players (other initializations possible):
        # dictionary (for each player) of dictionaries (for each state) of dictionaries (probability of each possible action)
        self.pi = {p: {s: {a: 1/len(self.game.actions(p, s)) for a in self.game.actions(p, s)}\
                    for s in self.game.states()} for p in self.game.players()}
        
        # value of the game for each state
        self.V = {s:0 for s in self.game.states()}
        