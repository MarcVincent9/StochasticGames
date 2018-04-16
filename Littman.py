# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 21:40:10 2018
"""

import numpy as np
import random
import StaticGameResolution as sgr


def roulette(dict):
    rnd = np.random.rand()
    tmp = 0
    for s, p in dict.items():
        tmp += p
        if tmp >= rnd:
            return s


def littman(game, explor, decay):
    
    # initialize
    p0, p1 = game.players[0], game.players[1]
    
    Q = {state: \
             {a1: \
                  {a0 : 1 for a0 in game.actions(p0, state)}\
             for a1 in game.actions(p1, state)} \
        for state in game.states()}
    
    V = {state: 1 for state in game.states()}
    pi = {state: {action: 1/len(game.actions(p0, state)) for action in game.actions(p0, state)} for state in game.states()}
    alpha = 1.
    s = roulette(game.initial_state())
    
    while(): # condition d'arrêt ?
        
        # choose an action
        a = random.choice(game.actions(p0, s)) if np.random.rand() < explor else roulette(pi[s])
        o = random.choice(game.actions(p1, s)) # je suppose...
        actions = {p0: a, p1: o}
        
        # learn
        rew = game.player0_reward(s, actions)
        s2 = roulette(game.transition(s, actions))
        Q[s][a][o] = (1-alpha) * Q[s][a][o] + alpha * (rew + game.gamma() * V[s2])
        
        V[s], pi[s] = sgr.maximin(game, Q[s], s)
        
        alpha *= decay
        
    return pi, V
    