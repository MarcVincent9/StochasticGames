# -*- coding: utf-8 -*-

import numpy as np
from NullSum2PlayerStochasticGame import NullSum2PlayerStochasticGame


class RockPaperScissors(NullSum2PlayerStochasticGame):
    
    dict = {"pierre":0, "papier":1, "ciseaux":2}
    list_actions = list(dict.keys())
    rewards_matrix = np.array([[0, -1, 1],
                               [1, 0, -1],
                               [-1, 1, 0]])


    def states(self):
        return [1]
    
    
    def actions(self, player, state):
        return self.list_actions
    
    
    def gamma(self):
        return .9
    
    
    def initial_state(self):
        return {1:1}        
    
    
    def transition(self, state, actions):
        return {1:1}
    
    
    def player0_reward(self, state, actions):
        return self.rewards_matrix[self.dict[actions[0]], self.dict[actions[1]]]
    
    
    def toString(self, state):
        return ""
