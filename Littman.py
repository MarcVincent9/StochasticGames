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


def MinimaxQ(game, explor, decay,display,iteration,choiceActPlayerB,playerA,playerB,policyplayerB):

    # initialize
   
    
    Q = {state: \
             {a1: \
                  {a0 : 1.0 for a0 in game.actions(playerA, state)}\
             for a1 in game.actions(playerB, state)} \
        for state in game.states()}
    
    V = {state: 1 for state in game.states()}
    pi = {state: {action: 1/len(game.actions(playerA, state)) for action in game.actions(playerA, state)} for state in game.states()}
    #initail_state = game.initial_state();
    alpha = 1.
    s = roulette(game.initial_state())
    k = 0
    #tanque on est arrive iteration fois au etat but
    while(k <= iteration): 
       
        k+=1
        
        if(k% display == 0):
            print("iteration : ",k)
        # choose an action
        a = random.choice(game.actions(playerA, s)) if np.random.rand() < explor else roulette(pi[s])
        o =  choiceActPlayerB(game,s,policyplayerB)
        actions = {playerA: a, playerB: o}
        
        # learn
        R = game.rewards(s, actions)
        rew = R.get(playerA)
        s2 = roulette(game.transition(s, actions))
        Q[s][o][a] = (1-alpha) * Q[s][o][a] + alpha * (rew + game.gamma() * V[s2])
        V[s], pi[s] = sgr.maximin(game, Q[s], s,playerA,playerB)
        s = s2
        alpha *= decay
    print("learnin rate at the end of the run : ",alpha)  
    return pi, V
    
