# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 21:15:49 2018

@author: Marc
"""

import numpy as np
import itertools as it
import copy
import StaticGameResolution as sgr



def shapley(game, epsilon):
    
    p0, p1 = game.players()[0], game.players()[1]
    
    
    def maj_G(V):
        
        def G_a(state, actions, V):
            R_s_a = game.player0_reward(state, actions)
            T_s_a = game.transition(state, actions)
            gamma = game.gamma()
            return R_s_a + gamma * sum(T_s_a[state2] * V[state2] for state2 in T_s_a.keys())
        
        return {state: \
                     {a1: \
                          np.array([G_a(state, {p0: a0, p1: a1}, V) for a0 in game.actions(p0, state)])\
                     for a1 in game.actions(p1, state)} \
                for state in game.states()}
                
                
    def convergence(V1, V2):
        for state in game.states():
            if abs(V1[state] - V2[state]) > epsilon:
                return False
        return True
        
        
    V = {state: np.random.rand() for state in game.states()}
    G = maj_G(V)
    V2 = {state: sgr.value(game, G, state) for state in game.states()}
    ite = 1
    
    while not(convergence(V, V2)):
        V = copy.deepcopy(V2)
        G = maj_G(V)
        V2 = {state: sgr.value(game, G, state) for state in game.states()}
        ite += 1
        
    G = maj_G(V2)
    pi = {state: sgr.strategy(game, G, state) for state in game.states()}
    print("Number of iterations: "+str(ite))
    
    return pi, V2







# tests
from RockPaperScissors import RockPaperScissors
from Soccer import Soccer
#game = RockPaperScissors()
game = Soccer()



# test maximin
"""
V = {s: np.random.rand() for s in game.states()}
p0, p1 = game.players()[0], game.players()[1]

def maj_G(V):
        
    def G_a(state, actions, V):
        R_s_a = game.player0_reward(state, actions)
        T_s_a = game.transition(state, actions)
        gamma = game.gamma()
        return R_s_a + gamma * sum(T_s_a[state2] * V[state2] for state2 in game.states())
    
    return {state: \
                 {a1: \
                      np.array([G_a(state, {p0: a0, p1: a1}, V) for a0 in game.actions(p0, state)])\
                 for a1 in game.actions(p1, state)} \
            for state in game.states()}

G = maj_G(V)
state = 1
print(sgr.maximin(game, G, state))
"""


# test shapley

print(shapley(game, epsilon = 1))