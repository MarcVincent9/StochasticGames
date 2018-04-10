# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 21:19:57 2018

@author: Marc
"""

import numpy as np
from gurobipy import *


# pour un jeu stochastique à somme nulle à deux joueurs 'game', résout le jeu statique associé à l'état 'state'
# avec G le gain espéré sous la forme {état : {action du joueur 1 : np.array[gain pour les actions du joueur 0]}}
# le joueur 0 cherche à maximiser son gain
def maximin(game, G, state):
    #print(state)
    
    try:
        
        p0, p1 = game.players()[0], game.players()[1]
        
        # Création du modèle
        mod = Model("jeu_simple")
        mod.setParam('OutputFlag', False)
        
        # Variables
        V = mod.addVar(lb = -GRB.INFINITY, vtype=GRB.CONTINUOUS, name="V") # V peut être < 0
        pi_s = np.array([mod.addVar(vtype=GRB.CONTINUOUS, name="p_"+str(action0)) for action0 in game.actions(p0, state)])
        mod.update()
        #print(pi_s)
        
        # Objectif
        mod.setObjective(V, GRB.MAXIMIZE)
        
        # Contraintes
        for action1 in game.actions(p1, state):
            #print(G[state][action1])
            mod.addConstr(V <= np.dot(pi_s, G[state][action1]), "")
            
        mod.addConstr(sum(pi_s) == 1, "")
        
        for pi_s_a in pi_s:
            mod.addConstr(pi_s_a >= 0, "")
        
        # Résolution
        mod.optimize()
        
        return(V.x, {action0: pi_s[i].x for i, action0 in enumerate(game.actions(p0, state))})
    
    except GurobiError:
        print('Error reported')
        
        
def value(game, G, state):
    return maximin(game, G, state)[0]


def strategy(game, G, state):
    return maximin(game, G, state)[1]