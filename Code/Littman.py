# -*- coding: utf-8 -*-

import numpy as np
import random
import StaticGameResolution as sgr


def roulette(self, dict):
    """
    randomly return one of the dictionary's key according to its probability (its value)
    
    :param dict: dictionary {index: probability}
    :rtype: index
    """
    rnd = np.random.rand()
    tmp = 0
    for s, p in dict.items():
        tmp += p
        if tmp >= rnd:
            return s


def MinimaxQ(game, explor, decay, display, iteration, playerA, playerB, policyplayerB):
    """
    Minimax-Q-learning 
    
    :param game: NullSum2PlayerStochasticGame
    :param explor: float
    :param decay: float
    :param display: integer (the number of the current iteration will be printed at every 'display' iterations)
    :param iteration: number of iterations
    :param playerA: maximizing player ID
    :param playerB: minimizing player ID
    :param policyplayerB: player B strategy (dictionary: {state: {action: probability}})
    :rtype: player A strategy (dictionary: {state: {action: probability}}) and value fonction (dictionary: {state: float})
    """

    # initialize
    Q = {state: \
             {action_B: \
                  {action_A : 1.0 for action_A in game.actions(playerA, state)}\
             for action_B in game.actions(playerB, state)} \
        for state in game.states()}
    
    V = {state: 1 for state in game.states()}
    pi = {state: {action: 1/len(game.actions(playerA, state)) for action in game.actions(playerA, state)} for state in game.states()}
    alpha = 1.
    s = roulette(game.initial_state())
    k = 0
    
    
    while(k <= iteration): 
       
        k += 1
        if(k % display == 0):
            print("iteration: ", k)
            
        # choose an action
        a = random.choice(game.actions(playerA, s)) if np.random.rand() < explor else roulette(pi[s])
        o = roulette(policyplayerB[s])
        actions = {playerA: a, playerB: o}
        
        # learn
        R = game.rewards(s, actions)
        rew = R.get(playerA)
        s2 = roulette(game.transition(s, actions))
        Q[s][o][a] = (1-alpha) * Q[s][o][a] + alpha * (rew + game.gamma() * V[s2])
        
        V[s], pi[s] = sgr.maximin(game, Q[s], s, playerA, playerB)
        
        s = s2
        alpha *= decay
        
    print("Learning rate at the end of the run: ", alpha)  
    return pi, V
    
