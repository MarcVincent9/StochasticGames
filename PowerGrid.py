# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 01:36:38 2018

@author: Marc
"""


from NullSum2PlayerStochasticGame import NullSum2PlayerStochasticGame
import itertools as it

class PowerGrid(NullSum2PlayerStochasticGame):
    
    def __init__(self, graph, p_pf, p_upf, p_pr, p_upr, budget): # parametres plus clairs...
        self.graph = graph
        self.p_pf = p_pf
        self.p_upf = p_upf
        self.p_pr = p_pr
        self.p_upr = p_upr
        self.budget = budget
        
        # link up = 1, down = 0
        self.list_states = list(it.product(range(2), repeat = graph.nb_links()))
        
        # on réduit l'espace d'actions aux actions dominantes, celles qui utilisent tout le budget
        self.list_actions = list(it.combinations(range(graph.nb_links()), budget))
    
    
    def states(self):
        return self.list_states
    
    
    def actions(self, player, state):
        return self.list_actions
    
    
    def gamma(self):
        return .9
    
    
    def initial_state(self):
        return {(1,) * self.graph.nb_links():1}
    
    
    def transition(self, state, actions):
        defense, attack = actions[0], actions[1]
        
        #if attack not in self.list_actions or defense not in self.list_actions:
        #    raise(ValueError)
        
        def next_status(link, status):
            if status == 1: # up
                if link in attack: # under attack
                    if link in defense: # reinforced
                        p_fail = self.p_pf
                    else:
                        p_fail = self.p_upf
                    return {0: p_fail, 1: 1-p_fail}
                else:
                    return {1: 1}
            else: # if status == 0: # down
                if link in defense: # repaired
                    p_recover = self.p_pr
                else:
                    p_recover = self.p_upr
                if link in attack: # under attack
                    p_recover *= (1 - self.p_upf)
                return {0: 1-p_recover, 1: p_recover}
            
        list_status_probability_distributions = [next_status(i, status) for i, status in enumerate(state)]
        list_possible_next_states = list(it.product(*tuple(tuple(d.keys()) for d in list_status_probability_distributions)))
        
        def state_probability(state):
            p = 1
            for i, status in enumerate(state):
                p *= list_status_probability_distributions[i][status]
            return p
        
        return {state: state_probability(state) for state in list_possible_next_states}
            
    
    def player0_reward(self, state, actions):
        return self.graph.cost(state)
    
    
    def toString(self, state):
        return ", ".join(str(i) + ":down" if status == 0 else str(i) + ":up" for i, status in enumerate(state))
