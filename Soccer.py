# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 18:49:12 2018

@author: Marc
"""

from NullSum2PlayerStochasticGame import NullSum2PlayerStochasticGame

class Soccer(NullSum2PlayerStochasticGame):
    
    deplacement = {"N":(-1, 0), "S":(1, 0), "E":(0, 1), "W":(0, -1), "stand":(0, 0)}
    list_actions = list(deplacement.keys())
    
    
    def __init__(self):
        self.cells = [(i, j) for i in range(1, 5) for j in range(1, 6)]    
        self.list_states = [(c1, c2, b) for c1 in self.cells for c2 in self.cells for b in [1, 2] if c1 != c2]
        self.starting_positions = ((3, 2), (2, 4))
        self.left_goal_positions = ((2, 0), (3, 0))
        self.right_goal_positions = ((2, 6), (3, 6))
        self.goal_positions = self.left_goal_positions + self.right_goal_positions
        
        
    def next_position(self, position, action):
        return tuple(map(sum, zip(position, self.deplacement[action])))
    
    
    def states(self):
        return self.list_states
    
    
    def actions(self, player, state): # ya peut-être plus propre à faire
        def allowed(action):
            position = self.next_position(state[player], action)
            return position in self.cells or (position in list(self.goal_positions) and state[2] == player+1)
        return [action for action in self.list_actions if allowed(action)]
    
    
    def gamma(self):
        return .9
    
    
    def initial_state(self):
        return {(*self.starting_positions, 1): .5, (*self.starting_positions, 2): .5}
    
    
    def transition(self, state, actions):
    
        # positions voulues
        pos1, pos2, b = state
        dest1 = self.next_position(pos1, actions[0])
        dest2 = self.next_position(pos2, actions[1])
        
        # but
        if (b == 1 and dest1 in self.goal_positions) or (b == 2 and dest2 in self.goal_positions):
            return self.initial_state()
        
        # choc frontal
        if dest1 == pos2 and dest2 == pos1:
            return {(pos1, pos2, 1): .5, (pos1, pos2, 2): .5}
        
        # blocage
        if dest1 == dest2:
            
            # obstruction
            if dest1 == pos1:
                return {(pos1, pos2, 1): 1}
            if dest2 == pos2:
                return {(pos1, pos2, 2): 1}
        
            # ruée
            return {(dest1, pos2, 1): .5, (pos1, dest2, 2): .5}
        
        # poursuite
        if dest1 == pos2: # and dest2 not in [pos1, pos2]
            return {(dest1, dest2, b): .5, (pos1, dest2, 2): .5}
        if dest2 == pos1: # and dest1 not in [pos1, pos2]
            return {(dest1, dest2, b): .5, (dest1, pos2, 1): .5}
        
        # déplacement normal
        return {(dest1, dest2, b): 1}
    
    
    def player0_reward(self, state, actions):
    
        # positions voulues
        pos1, pos2, b = state
        dest1 = self.next_position(pos1, actions[0])
        dest2 = self.next_position(pos2, actions[1])
        
        # but
        if (b == 1 and dest1 in self.right_goal_positions) or (b == 2 and dest2 in self.right_goal_positions):
            return 1
        
        if (b == 2 and dest2 in self.left_goal_positions) or (b == 1 and dest1 in self.left_goal_positions):
            return -1
        
        return 0
    
    
    def toString(self, state):
        pos1, pos2, b = state
        s = ""
        for c in self.cells:
            if c[1] == 1:
                s += "\n"
            if c == pos1 and b == 1:
                s += "A "
            elif c == pos1 and b == 2:
                s += "a "
            elif c == pos2 and b == 1:
                s += "b "
            elif c == pos2 and b == 2:
                s += "B "
            else:
                s += "_ "
        return s
    