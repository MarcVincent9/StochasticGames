# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 21:15:49 2018
"""

import numpy as np
import copy
import StaticGameResolution as sgr



# calcule la prochaine valeur de V à partir du V actuel
def new_V_and_pi(game, V,playerA,playerB):
    
    # fonction auxiliaire de calcul du gain espéré pour un état et des actions donnés
    def G_a(state, actions, V):
        R = game.rewards(state, actions)
        R_s_a = R.get(playerA)
        
        T_s_a = game.transition(state, actions)
        gamma = game.gamma()
        return R_s_a + gamma * sum(T_s_a[state2] * V[state2] for state2 in T_s_a.keys())
        
    # matrice des gains espérés
    G = {state: \
             {action1: \
                  {action0 : \
                       G_a(state, {playerA: action0, playerB: action1}, V) \
                  for action0 in game.actions(playerA, state)} \
             for action1 in game.actions(playerB, state)} \
        for state in game.states()}
                    
    # pour chaque état on résout le jeu statique associé par PL pour obtenir les nouveaux V et pi
    new_V, pi = {}, {}
    for state in game.states():
        new_V[state], pi[state] = sgr.maximin(game, G[state], state,playerA,playerB)
        
    return pi,new_V
            

            
            
# renvoie la différence maximale entre les valeurs de deux dictionnaires de mêmes clefs
def ecart(V1, V2):
    m = max(abs(V1[state] - V2[state]) for state in V1.keys())
    s = sum(abs(V1[state] - V2[state]) for state in V1.keys())
    return m ,s




def shapley(game, epsilon,playerA,playerB):
      
    # initialisation de V
    V = {state: np.random.rand() for state in game.states()}
    
    # première itération sur la valeur
    pi,V2 = new_V_and_pi(game, V,playerA,playerB)
    ite = 1
    
    # on répète jusqu'à converger
    m , _ = ecart(V, V2) 
    while  m> epsilon:
        V = copy.deepcopy(V2)
        pi,V2 = new_V_and_pi(game, V,playerA,playerB)
        ite += 1
        m , _ = ecart(V, V2) 
    print("Number of iterations: "+str(ite))
    
    return pi,V2





