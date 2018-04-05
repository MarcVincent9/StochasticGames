# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 21:15:49 2018

@author: Marc
"""

import numpy as np
import itertools as it
import copy

def shapley(game, epsilon):
    
    #def valeur:
        
    #def ecart:
    
    #def equilibre:
    
    def dict_sum(dicts):
        return {k: sum(d[k] for d in dicts) for k in d1.keys()}
        
    def dict_prod(c, d):
        return {k: c * v for k, v in d.items()}
        
    def ga(s, a):
        T = game.transition(s, a)
        stu = dict_sum(tuple(dict_prod(T[s2], U[s2]) for s2 in game.states()))
        gstu = dict_prod(game.gamma(), stu)
        return dict_sum((game.rewards(s, a), gstu))
        
    p0, p1 = game.players[0], game.players[1]
    U = {s: np.random.rand() for s in game.states()}
    G = {s: {a: ga(s, a) for a in it.product(game.actions(p0, s), game.actions(p1, s))} for s in game.states()}
    U2 = {s: valeur(G[s]) for s in game.states()}
    
    while ecart(U, U2) < epsilon:
        U = copy.deepcopy(U2)
        G = {s: {a: ga(s, a) for a in it.product(game.actions(p0, s), game.actions(p1, s))} for s in game.states()}
        U2 = {s: valeur(G[s]) for s in game.states()}
        
    G = {s: {a: ga(s, a) for a in it.product(game.actions(p0, s), game.actions(p1, s))} for s in game.states()}
    pi = {s: equilibre(G[s]) for s in game.states()}
    
    return pi, U