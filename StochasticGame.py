# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 20:38:50 2018
"""

import itertools as it

class StochasticGame:
    
    # s'assurer d'un ordre sur états/actions/joueurs au cas où l'utilisateur utiliserait des sets (définir cet ordre dans init)
    # ou alors c'est son problème
    
        
    def states(self):
        """Return the list of all states.
        
        :rtype: list of (tuples of) integers/strings
        """
        raise(NotImplementedError)
        
        
    def players(self):
        """Return the list of all players.
        
        :rtype: list of integers/strings
        """
        raise(NotImplementedError)
    
    
    # ou alors actions(self, state) qui renvoie un dico joueur: liste_actions...
    def actions(self, player, state):
        """Return the list of given player's possible actions in given state.
        
        :param player: player ID
        :param state: state
        :rtype: list of (tuples of) integers/strings
        """
        raise(NotImplementedError)
    
    
    def nb_players(self):
        """Return the number of players.
        
        :rtype: integer
        """
        return len(self.players())
    
    
    def gamma(self):
        """Return the discount factor.
        
        :rtype: float in [0, 1[
        """
        raise(NotImplementedError)
        
       
    def transition(self, state, actions):
        """Return a probability distribution for the next state.
        
        :param state: current state
        :param actions: dictionary (key: player; value: action)
        :rtype: dictionary {state: probability}
        """
        raise(NotImplementedError)
        
        
    # _reward n'est finalement rien d'autre qu'une fonction auxiliaire. Pourquoi ne pas laisser à l'utilisateur le soin d'en utiliser une s'il le veut, pour ne garder que rewards ?
    def _reward(self, player, state, actions):
        """Return the immediate reward of a player given a state and the actions of all players. You should implement either this function or rewards(self, state, actions)
        
        :param player: player ID
        :param state: current state
        :param actions: dictionary (key: player; value: action)
        :rtype: integer or float
        """
        raise(NotImplementedError)
        
        
    def rewards(self, state, actions):
        """Return the immediate reward of all players given a state and the actions of all players. You should implement either this function or _reward(self, player, state, actions)
        
        :param state: current state
        :param actions:  dictionary (key: player; value: action)
        :rtype:  dictionary (key: player; value: reward)
        """
        return {player: self._reward(player, state, actions) for player in self.players()}
        
        
    def initial_state(self):
        """Return a probability distribution for the initial state.
        
        :rtype: dictionary {state: probability}
        """
        raise(NotImplementedError)
        
        
    def check_transitions(self, epsilon):
        for state in self.states():
            for actions in it.product(self.actions(player, state) for player in self.players()):
                if abs(1 - sum(self.transition(state, actions).values())) > epsilon:
                    return False
        return True
        