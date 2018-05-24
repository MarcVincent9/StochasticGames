# -*- coding: utf-8 -*-

from StochasticGame import StochasticGame


class NullSum2PlayerStochasticGame(StochasticGame):
    """
    Specific class for null sum 2-player stochastic games
	Player 0 must maximize his rewards, player 1 must minimize them
    """
    
    def players(self):
        return [0, 1]
    
    
    def player0_reward(self, state, actions):
        raise(NotImplementedError)
     
        
    def rewards(self, state, actions):
        r = self.player0_reward(state, actions)
        return {0:r, 1:-r}