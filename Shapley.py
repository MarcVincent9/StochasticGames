# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 21:15:49 2018
"""

import numpy as np
import itertools as it
import copy
import StaticGameResolution as sgr



# calcule la prochaine valeur de V à partir du V actuel
def new_V_and_pi(game, V):
    
    p0, p1 = game.players()[0], game.players()[1]
        
    # fonction auxiliaire de calcul du gain espéré pour un état et des actions donnés
    def G_a(state, actions, V):
        R_s_a = game.player0_reward(state, actions)
        T_s_a = game.transition(state, actions)
        gamma = game.gamma()
        return R_s_a + gamma * sum(T_s_a[state2] * V[state2] for state2 in T_s_a.keys())
        
    # matrice des gains espérés
    G = {state: \
             {action1: \
                  {action0 : \
                       G_a(state, {p0: action0, p1: action1}, V) \
                  for action0 in game.actions(p0, state)} \
             for action1 in game.actions(p1, state)} \
        for state in game.states()}
                    
    # pour chaque état on résout le jeu statique associé par PL pour obtenir les nouveaux V et pi
    new_V, pi = {}, {}
    for state in game.states():
        new_V[state], pi[state] = sgr.maximin(game, G[state], state)
        
    return new_V, pi
            

            
            
# renvoie la différence maximale entre les valeurs de deux dictionnaires de mêmes clefs
def ecart(V1, V2):
    return max(abs(V1[state] - V2[state]) for state in V1.keys())




def shapley(game, epsilon):
      
    # initialisation de V
    V = {state: np.random.rand() for state in game.states()}
    
    # première itération sur la valeur
    V2, pi = new_V_and_pi(game, V)
    ite = 1
    
    # on répète jusqu'à converger
    while ecart(V, V2) > epsilon:
        V = copy.deepcopy(V2)
        V2, pi = new_V_and_pi(game, V)
        ite += 1
    print("Number of iterations: "+str(ite))
    
    return V2, pi





# tests
from RockPaperScissors import RockPaperScissors
from Soccer import Soccer
game = RockPaperScissors()
#game = Soccer()



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