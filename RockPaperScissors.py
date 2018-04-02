# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 01:02:42 2018

@author: Marc
"""

import numpy as np
from StochasticGame import StochasticGame

class RockPaperScissors(StochasticGame):
    
    list_states = [1]
    dict = {"pierre":0, "papier":1, "ciseaux":2}
    list_actions = list(dict.keys())
    rewards_matrix = np.array([[0, -1, 1],
                        [1, 0, -1],
                        [-1, 1, 0]])


    def states(self):
        return self.list_states
    
    
    def actions(self, player, state):
        return self.list_actions
    
    
    def nb_players(self):
        return 2
    
    
    def initial_state(self):
        return {1:1}        
    
    
    def transition(self, state, actions):
        return {1:1}
    
    
    def reward(self, player, state, actions):
        a1, a2 = actions
        return self.rewards_matrix[self.dict[a1], self.dict[a2]]
    
    
    def toString(self, state):
        return ""
