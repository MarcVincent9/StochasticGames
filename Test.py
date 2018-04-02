# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 23:19:16 2018

@author: Marc
"""

import numpy as np

class Test:
    
    def __init__(self, game, pi):
        self.g = game
        self.current_state = self.roulette(game.initial_state())
        self.total_rewards = (0,) * game.nb_players()
        self.t = 0
        self.pi = pi
    

    def roulette(self, dict):
        """
        randomly return one of the dictionary's key according to its probability (its value)
        """
        rnd = np.random.rand()
        tmp = 0
        for s, p in dict.items():
            tmp += p
            if tmp >= rnd:
                return s
            
            
    def discounted_rewards(self, state, actions):
        return tuple((self.g.gamma() ** self.t) * r for r in self.g.rewards(state, actions))
    
        
    def step(self, actions):
        
        self.t += 1
        
        # rewards update
        self.total_rewards = tuple(map(sum, zip(self.total_rewards, self.discounted_rewards(self.current_state, actions))))
        
        # random transition to next state
        self.current_state = self.roulette(self.g.transition(self.current_state, actions))
        
        print(self.total_rewards)
        print(self.g.toString(self.current_state))
        
        
    def chooseAction(self, player): 
        """
        select an action for the player according to their strategy
        """
        return self.roulette(self.pi[player][self.current_state])
