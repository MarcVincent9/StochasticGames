# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 21:40:10 2018

@author: Marc
"""

import numpy as np
import random


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
    Q = {(s, a, o): 1 for s in game.states() for a in game.actions(p0, s) for o in game.actions(p1, s)}
    V = {s: 1 for s in game.states()}
    pi = {s: {a: 1/len(game.actions(p0, s)) for a in game.actions(p0, s)} for s in game.states()}
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
        Q[(s, a, o)] = (1-alpha) * Q[(s, a, o)] + alpha * (rew + game.gamma() * V[s2])
        pi[s] = # argmax(min(sum(pi[s][aa] * Q[(s, aa, oo)] for aa in game.actions(p0, s)) for oo in game.actions(p1, s))  for pi[s])
        V[s] = min(sum(pi[s][aa] * Q[(s, aa, oo)] for aa in game.actions(p0, s)) for oo in game.actions(p1, s))
        alpha *= decay
        
    return pi, V
    