# -*- coding: utf-8 -*-

import numpy as np
import copy
import StaticGameResolution as sgr


def new_V_and_pi(game, V, playerA, playerB):
    """
    compute the next value of V based on its current value
    
    :param game: NullSum2PlayerStochasticGame
    :param V: current value fonction (dictionary: {state: float})
    :param playerA: maximizing player ID
    :param playerB: minimizing player ID
    :rtype: player A strategy (dictionary: {state: {action: probability}}) and value fonction (dictionary: {state: float})
    """
    
    # auxiliary function that computes the expected rewards for given state and actions
    def G_a(state, actions, V):
        R = game.rewards(state, actions)
        R_s_a = R.get(playerA)
        
        T_s_a = game.transition(state, actions)
        gamma = game.gamma()
        return R_s_a + gamma * sum(T_s_a[state2] * V[state2] for state2 in T_s_a.keys())
        
    # expected rewards matrix
    G = {state: \
             {actionB: \
                  {actionA : \
                       G_a(state, {playerA: actionA, playerB: actionB}, V) \
                  for actionA in game.actions(playerA, state)} \
             for actionB in game.actions(playerB, state)} \
        for state in game.states()}
                    
    # for each state the associated static game is solved with linear programming to get the new V and pi
    new_V, pi = {}, {}
    for state in game.states():
        new_V[state], pi[state] = sgr.maximin(game, G[state], state, playerA, playerB)
        
    return pi, new_V
            

            
            
def ecart(V1, V2):
    """
    return the maximal difference between the same-key values of two dictionaries and the sum of all differences
    
    :param V1, V2: dictionary {index: float}
    :rtype: maximal difference, sum of differences
    """
    m = max(abs(V1[state] - V2[state]) for state in V1.keys())
    s = sum(abs(V1[state] - V2[state]) for state in V1.keys())
    return m, s




def shapley(game, epsilon, playerA, playerB):
    """
    Shapley's algorithm
    
    :param game: NullSum2PlayerStochasticGame
    :param epsilon: convergence limit (float)
    :param playerA: maximizing player ID
    :param playerB: minimizing player ID
    :rtype: player A strategy (dictionary: {state: {action: probability}}) and value fonction (dictionary: {state: float})
    """
      
    # V initialized
    V = {state: np.random.rand() for state in game.states()}
    
    # first iteration on value
    pi, V2 = new_V_and_pi(game, V, playerA, playerB)
    ite = 1
    
    # repeat until convergence
    m, _ = ecart(V, V2) 
    while m > epsilon:
        V = copy.deepcopy(V2)
        pi, V2 = new_V_and_pi(game, V, playerA, playerB)
        ite += 1
        m, _ = ecart(V, V2) 
    print("Number of iterations: "+str(ite))
    
    return pi, V2





