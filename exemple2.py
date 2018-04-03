# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 15:55:04 2018

@author: Marc
"""

from Test import Test
from PowerGrid import PowerGrid


class Graph:
    
    def __init__(self):
        self.list_links = []
        self.list_buses = {}
    
    def addLink(self, bus1, bus2):
        if bus1 in self.list_buses.keys() and bus2 in self.list_buses.keys() and\
           (bus1, bus2) not in self.list_links and (bus2, bus1) not in self.list_links:
            self.list_links.append((bus1, bus2))
        else:
            raise(ValueError)
            
    def addBus(self, value):
        self.list_buses[len(self.list_buses)] = value # positive: supply; negative: load
        
    def nb_links(self):
        return len(self.list_links)
    
    def cost(self, state):
        
        

g = Graph()
g.addBus(-160)
g.addBus(-200)
g.addBus(-370)
g.addBus(500)
g.addBus(257.8)
g.addLink(0, 2)
g.addLink(0, 1)
g.addLink(1, 2)
g.addLink(1, 3)
g.addLink(2, 4)




game = PowerGrid(g, .5, 1, .6, 0, 2)

pi = [{s: {a: 1/len(game.actions()[i]) for a in game.actions()[i]} for s in game.states()} for i in range(game.nb_players())]
test = Test(game, pi)

test.step(((1,2), (1,)))
#test.step(tuple(test.chooseAction(i) for i in range(game.nb_players())))game = Soccer()