# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 20:38:50 2018

@author: Marc
"""

import numpy as np

# prévoir généricité pour plus de joueurs !
class StochasticGame:
    
    def __init__(self, states, initial_state, actions, transition, reward, resources, gamma = 1):
        self.states = states
        self.actions = actions
        self.transition = transition
        self.reward = reward
        self.rsc = resources
        self.gamma = gamma
        
        self.pi1 = np.ones((len(states), len(actions))) / len(actions)
        self.pi2 = np.ones((len(states), len(actions))) / len(actions)
        self.V = np.array([0] * len(states))
        
        self.total_reward = 0
        self.current_state = initial_state(resources)
        
        
    def step(self, action1, action2):
        
        def roulette(l):
            rnd = np.random.rand()
            i = 0
            tmp = l[i][1]
            while tmp < rnd:
                i += 1
                tmp += l[i][1]
            return l[i][0]
        
        self.total_reward += reward(self.current_state, action1, action2, self.rsc)
        l = transition(self.current_state, action1, action2, self.rsc)
        self.current_state = roulette(l)
        
        #print(l)
        print(self.total_reward)
        print(self)
        
        
    def choice(self): 
        return # renvoie action choisie selon pi
        
        
    # illégal
    def __str__(self):
        pos1, pos2, b = self.current_state
        cells = [(i, j) for i in range(1, 5) for j in range(1, 6)]  
        s = ""
        for c in cells:
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


class Resources:

    deplacement = {"N":(-1, 0), "S":(1, 0), "E":(0, 1), "W":(0, -1), "stand":(0, 0)}
    starting_positions = ((3, 2), (2, 4))
    left_goal_positions = [(2, 0), (3, 0)]
    right_goal_positions = [(2, 6), (3, 6)]
    goal_positions = left_goal_positions + right_goal_positions
    cells = [(i, j) for i in range(1, 5) for j in range(1, 6)]    
    states = [(c1, c2, b) for c1 in cells for c2 in cells for b in [1, 2] if c1 != c2]
    actions = ["N", "S", "E", "W", "stand"]
    
    
def initial_state(rsc):
    if np.random.rand() > .5 :
        return (*rsc.starting_positions, 1)
    return (*rsc.starting_positions, 2)


def transition(state, action1, action2, rsc):
    
    # positions voulues
    pos1, pos2, b = state
    dest1 = tuple(map(sum, zip(pos1, rsc.deplacement[action1])))
    dest2 = tuple(map(sum, zip(pos2, rsc.deplacement[action2])))
    
    # but
    if (b == 1 and dest1 in rsc.goal_positions) or (b == 2 and dest2 in rsc.goal_positions):
        return [((*rsc.starting_positions, 1), .5), ((*rsc.starting_positions, 2), .5)]
    
    # position invalide
    if dest1 not in rsc.cells or dest2 not in rsc.cells:
        return [((state), 1)]
    
    # choc frontal
    if dest1 == pos2 and dest2 == pos1:
        return [((state), 1)]
    
    # blocage
    if dest1 == dest2:
        
        # obstruction
        if action1 == "stand":
            return [((pos1, pos2, 1), 1)]
        if action2 == "stand":
            return [((pos1, pos2, 2), 1)]
    
        # ruée
        return [((dest1, pos2, 1), .5), ((pos1, dest2, 2), .5)]
    
    # déplacement normal
    return [((dest1, dest2, b), 1)]


def reward(state, action1, action2, rsc):
    
    # positions voulues
    pos1, pos2, b = state
    dest1 = tuple(map(sum, zip(pos1, rsc.deplacement[action1])))
    dest2 = tuple(map(sum, zip(pos2, rsc.deplacement[action2])))
    
    # but
    if (b == 1 and dest1 in rsc.right_goal_positions): #or (b == 2 and dest2 in rsc.right_goal_positions):
        return 1
    
    if (b == 2 and dest2 in rsc.left_goal_positions): #or (b == 1 and dest1 in rsc.left_goal_positions):
        return -1
    
    # position invalide
    if dest1 not in rsc.cells:
        return - 1000
    
    if dest2 not in rsc.cells:
        return + 1000
    
    return 0
    


rsc = Resources()
sg = StochasticGame(rsc.states, initial_state, rsc.actions, transition, reward, rsc)
sg.step("N", "W")