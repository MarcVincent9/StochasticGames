# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 20:07:51 2018
"""

from StochasticGame import StochasticGame

class NullSum2PlayerStochasticGame(StochasticGame):
    
    def players(self):
        return [0, 1]
    
    
    def player0_reward(self, state, actions):
        raise(NotImplementedError)
     
        
    def rewards(self, state, actions):
        r = self.player0_reward(state, actions)
        return {0:r, 1:-r}