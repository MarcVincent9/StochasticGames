# -*- coding: utf-8 -*-

from NullSum2PlayerStochasticGame import NullSum2PlayerStochasticGame


class Soccer(NullSum2PlayerStochasticGame):
    """
    Example of a null sum 2-player stochastic game: simplified football game (cf. Littman 1994)
    """
    
    movement = {"N":(-1, 0), "S":(1, 0), "E":(0, 1), "W":(0, -1), "stand":(0, 0)}
    list_actions = list(movement.keys())
    
    
    def __init__(self):
        self.cells = [(i, j) for i in range(1, 5) for j in range(1, 6)]    
        self.list_states = [(c1, c2, b) for c1 in self.cells for c2 in self.cells for b in [1, 2] if c1 != c2]
        self.starting_positions = ((3, 2), (2, 4))
        self.left_goal_positions = ((2, 0), (3, 0))
        self.right_goal_positions = ((2, 6), (3, 6))
        self.goal_positions = self.left_goal_positions + self.right_goal_positions
        
        
    def next_position(self, position, action):
        return tuple(map(sum, zip(position, self.movement[action])))
    
    
    def states(self):
        return self.list_states
    
    
    def actions(self, player, state):
        def allowed(action):
            position = self.next_position(state[player], action)
            return position in self.cells or (position in list(self.goal_positions) and state[2] == player+1)
        return [action for action in self.list_actions if allowed(action)]
    
    
    def gamma(self):
        return .9
    
    
    def initial_state(self):
        return {(*self.starting_positions, 1): .5, (*self.starting_positions, 2): .5}
    
    
    def transition(self, state, actions):
    
        # desired positions
        pos1, pos2, b = state
        dest1 = self.next_position(pos1, actions[0])
        dest2 = self.next_position(pos2, actions[1])
        
        # goal
        if (b == 1 and dest1 in self.goal_positions) or (b == 2 and dest2 in self.goal_positions):
            return self.initial_state()
        
        # frontal shock: players try to go to each other's position
        if dest1 == pos2 and dest2 == pos1:
            return {(pos1, pos2, 1): .5, (pos1, pos2, 2): .5}
        
        # blocking: players try to go to the same position
        if dest1 == dest2:
            
            # obstruction: one of the players chooses not to move
            if dest1 == pos1:
                return {(pos1, pos2, 1): 1}
            if dest2 == pos2:
                return {(pos1, pos2, 2): 1}
        
            # players rush to another position
            return {(dest1, pos2, 1): .5, (pos1, dest2, 2): .5}
        
        # one of the players "follows" the other
        if dest1 == pos2: # and dest2 not in [pos1, pos2]
            return {(dest1, dest2, b): .5, (pos1, dest2, 2): .5}
        if dest2 == pos1: # and dest1 not in [pos1, pos2]
            return {(dest1, dest2, b): .5, (dest1, pos2, 1): .5}
        
        # normal movement
        return {(dest1, dest2, b): 1}
    
    
    def player0_reward(self, state, actions):
    
        # desired positions
        pos1, pos2, b = state
        dest1 = self.next_position(pos1, actions[0])
        dest2 = self.next_position(pos2, actions[1])
        
        # goal
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
    