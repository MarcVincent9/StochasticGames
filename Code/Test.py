# -*- coding: utf-8 -*-

import numpy as np

class Test:
    """
    simulates a game between two policies
    """
    
    def __init__(self, game, nb_of_iterations, players_policies):
        """
        :param game: NullSum2PlayerStochasticGame
        :param nb_of_iterations: integer
        :param players_policies: dictionary {player: {state: {action: probability}}}
        """
        
        self.g = game
        self.current_state = self.roulette(game.initial_state())
        self.total_rewards = {player: 0 for player in game.players()}
        self.t = 0 # current iteration
        self.players_policies = players_policies
        self.nb_of_iterations = nb_of_iterations
        self.p0, self.p1 = game.players()[0], game.players()[1]
        
        # football game
        self.but = 0 # total number of goals
        self.w = {player: 0 for player in game.players()} # number of goals of each player
        

    def roulette(self, dict):
        """
        randomly return one of the dictionary's key according to its probability (its value)
        
        :param dict: dictionary {index: probability}
        :rtype: index
        """
        rnd = np.random.rand()
        tmp = 0
        for s, p in dict.items():
            tmp += p
            if tmp >= rnd:
                return s
    
    
    def discounted_rewards(self, state, actions):
        """
        return the gamma-discounted rewards
        
        :param state: state ID
        :param actions: action ID tuple
        :rtype: dictionary {player: reward}
        """
        
        rewards = self.g.rewards(state, actions)
        
        if rewards.get(self.p0) == 1:
            self.but += 1
            self.w[self.p0] += 1
        if rewards.get(self.p1) == 1:
            self.but += 1
            self.w[self.p1] += 1
        
        return {player: (self.g.gamma() ** self.t) * r for player, r in self.g.rewards(state, actions).items()}
    
    
    def step(self, actions):
        """
        pass one iteration of the simulation
        
        :param actions: action ID tuple
        """
        
        self.t += 1
        
        # rewards update
        def dict_sum(d1, d2):
            return {k: d1[k] + d2[k] for k in d1.keys()}
        self.total_rewards = dict_sum(self.total_rewards, self.discounted_rewards(self.current_state, actions))
        
        # random transition to next state
        self.current_state = self.roulette(self.g.transition(self.current_state, actions))
        
    
    def chooseAction(self, player): 
        """
        select an action for the player according to their strategy
        
        :param player: player ID
        :rtype: action ID
        """
        return self.roulette(self.players_policies[player][self.current_state])
    
    
    def simulation(self):
        """
        run the whole simulation
        """
        while self.t <= self.nb_of_iterations:
            actions = {p : self.chooseAction(p) for p in self.g.players()}
            self.step(actions)


    def get_winners(self):
        """
        [football game] return the goal ratio of each player
        """
        if self.but == 0:
            self.but = 1
        self.w[self.p0] /= (1.0 * self.but)  
        self.w[self.p1] /= (1.0 * self.but)  
        return self.w
    