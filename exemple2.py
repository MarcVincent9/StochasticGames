# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 15:55:04 2018
"""

from Test import Test
from PowerGrid import PowerGrid


class Graph:
    
    def __init__(self):
        self.list_links = [20, 10, 30, 55, 25]
        
    def nb_links(self):
        return len(self.list_links)
    
    def cost(self, state):
        pass
        

g = Graph()
game = PowerGrid(g, .5, 1, .6, 0, 2)

pi = {p: {s: {a: 1/len(game.actions(p, s)) for a in game.actions(p, s)} for s in game.states()} for p in game.players()}
test = Test(game, pi)

test.step(((1,2), (1,)))
#test.step(tuple(test.chooseAction(i) for i in range(game.nb_players())))game = Soccer()