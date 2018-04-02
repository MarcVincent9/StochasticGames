# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 20:38:50 2018

@author: Marc
"""


class StochasticGame:
        
    def states(self):
        """Return the list of all states.
        
        :rtype: list of (tuples of) integers/strings
        """
        raise(NotImplementedError)
    
    
    def actions(self, player, state):
        """Return the list of given player's actions in given state.
        
        :param player: player ID
        :param state: state
        :rtype: list of (tuples of) integers/strings
        """
        raise(NotImplementedError)
    
    
    def nb_players(self):
        """Return the number of players. Players are identified by their ID, starting from 0.
        
        :rtype: integer
        """
        raise(NotImplementedError)
        
        
    def players(self): # renvoie liste des joueurs (eg avec strings) : inverser abstraction ac nb_players ?
        """Return the list of all players.
        
        :rtype: list of...
        """
        return list(range(self.nb_players())) # actions et rewards de tous les joueurs seraient alors des dicos...
        # penser à modif la doc en conséquence, et Algo
    
    
    def gamma(self):
        """Return the discount factor.
        
        :rtype: float between 0 and 1 (default = 1)
        """
        return 1.
        
       
    def transition(self, state, actions):
        """Return a probability distribution for the next state.
        
        :param state: current state
        :param actions: tuple of each player's action (sorted by player ID)
        :rtype: dictionary {state: probability}
        """
        raise(NotImplementedError)
        
        
    def reward(self, player, state, actions): # player comme argument par coherence avec actions(), mais pas super pour l'optimisation en somme nulle
        """Return the reward of a player given a state and the actions of all players.
        
        :param player: player ID
        :param state: current state
        :param actions: tuple of each player's action (sorted by player ID)
        :rtype: integer or float
        """
        pass # plutôt que raise(NotImplementedError) ?
        
        
    def rewards(self, state, actions): # solution ?
        """Return the reward of all players given a state and the actions of all players.
        
        :param state: current state
        :param actions: tuple of each player's action (sorted by player ID)
        :rtype: tuple of integers/floats
        """
        # verif que reward est implementee...
        return tuple(self.reward(player, state, actions) for player in self.players())
        
        
    def initial_state(self):
        """Return a probability distribution for the initial state.
        
        :rtype: dictionary {state: probability}
        """
        raise(NotImplementedError)
        