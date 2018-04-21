# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 21:19:57 2018
"""

import numpy as np
from gurobipy import *


# pour un jeu stochastique à somme nulle à deux joueurs 'game', résout le jeu statique associé à l'état 'state'
# avec G le gain espéré pour cet état sous la forme {action du joueur 1 : {action du joueur 0 : gain}}
# le joueur 0 cherche à maximiser son gain
def maximin(game, expected_rewards, state,playerA,playerB):
    
    try:
        
       
        
        # Création du modèle
        mod = Model("jeu_simple")
        mod.setParam('OutputFlag', False) # pas d'affichage console
        
        # Variables
        V = mod.addVar(lb = -GRB.INFINITY, vtype=GRB.CONTINUOUS, name="V") # V peut être < 0
        pi_s = np.array([mod.addVar(vtype=GRB.CONTINUOUS, name="p_"+str(action0)) for action0 in game.actions(playerA, state)])
        mod.update()
        
        # Objectif
        mod.setObjective(V, GRB.MAXIMIZE)
        
        # Contraintes
        for action1 in game.actions(playerB, state):
            # conversion dictionnaire > np.array en respectant l'ordre des actions
            expected_rewards_action1 = np.array([expected_rewards[action1][action0] for action0 in game.actions(playerA, state)])
            mod.addConstr(V <= np.dot(pi_s, expected_rewards_action1), "")
            
        mod.addConstr(sum(pi_s) >= 1.0, "")
        mod.addConstr(sum(pi_s) <= 1.0, "")
        mod.addConstr(sum(pi_s) ,GRB.EQUAL,1.0, "")
        for pi_s_a in pi_s:
            mod.addConstr(pi_s_a >= 0, "")
        
        # Résolution
        mod.optimize()
        
        return(V.x, {action0: pi_s[i].x for i, action0 in enumerate(game.actions(playerA, state))})
    
    except GurobiError:
        print('Error reported')