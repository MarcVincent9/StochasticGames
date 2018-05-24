# -*- coding: utf-8 -*-

import numpy as np
from gurobipy import *


def maximin(game, expected_rewards, state, playerA, playerB):
    """
    solve the static game associated with one state of a null sum 2-player stochastic game
    
    :param game: NullSum2PlayerStochasticGame
    :param expected_rewards: dictionary {player B action : {player A action : reward}}
    :param state: state ID
    :param playerA: maximizing player ID
    :param playerB: minimizing player ID
    :rtype: state value (float) and player A strategy (dictionary: {action: probability})
    """
    
    try:
        
        # Model created
        mod = Model("jeu_simple")
        mod.setParam('OutputFlag', False) # no console print
        
        # Variables
        V = mod.addVar(lb = -GRB.INFINITY, vtype=GRB.CONTINUOUS, name="V") # V can be negative
        pi_s = np.array([mod.addVar(vtype=GRB.CONTINUOUS, name="p_"+str(action0)) for action0 in game.actions(playerA, state)])
        mod.update()
        
        # Objective
        mod.setObjective(V, GRB.MAXIMIZE)
        
        # Constraints
        for action1 in game.actions(playerB, state):
            # conversion dictionary > np.array while preserving the same order for actions
            expected_rewards_action1 = np.array([expected_rewards[action1][action0] for action0 in game.actions(playerA, state)])
            mod.addConstr(V <= np.dot(pi_s, expected_rewards_action1), "")
            
        mod.addConstr(sum(pi_s) >= 1.0, "")
        mod.addConstr(sum(pi_s) <= 1.0, "")
        mod.addConstr(sum(pi_s), GRB.EQUAL, 1.0, "")
        
        for pi_s_a in pi_s:
            mod.addConstr(pi_s_a >= 0, "")
        
        # Solving
        mod.optimize()
        
        return(V.x, {action0: pi_s[i].x for i, action0 in enumerate(game.actions(playerA, state))})
    
    except GurobiError:
        print('Error reported')