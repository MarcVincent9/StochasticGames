# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 23:19:16 2018
"""

import numpy as np

class Test:
    
    def __init__(self, game, iteration,policyPlayers):
        self.g = game
        self.current_state = self.roulette(game.initial_state())
        self.total_rewards = {player: 0 for player in game.players()}
        self.t = 0
        self.policyPlayers = policyPlayers
        self.iteration = iteration
        self.but = 0
        self.w = {player: 0 for player in game.players()}
        self.p0, self.p1 = game.players()[0], game.players()[1]
        

    def roulette(self, dict):
        """
        randomly return one of the dictionary's key according to its probability (its value)
        """
        rnd = np.random.rand()
        tmp = 0
        for s, p in dict.items():
            tmp += p
            if tmp >= rnd:
                return s
            
    def getWiners(self):
        if self.but == 0:
            self.but = 1
        self.w[self.p0] /= (1.0 * self.but)  
        self.w[self.p1] /= (1.0 * self.but)  
        return self.w
    
    def discounted_rewards(self, state, actions):
        rewards = self.g.rewards(state, actions)
        if rewards.get(self.p0) == 1:
            self.but += 1
            self.w[self.p0] += 1
        if rewards.get(self.p1) == 1:
            self.but += 1
            self.w[self.p1] += 1
        
        return {player: (self.g.gamma() ** self.t) * r for player, r in self.g.rewards(state, actions).items()}
    
    
    def step(self, actions):
        
        self.t += 1
        
        # rewards update
        def dict_sum(d1, d2):
            return {k: d1[k] + d2[k] for k in d1.keys()}
        self.total_rewards = dict_sum(self.total_rewards, self.discounted_rewards(self.current_state, actions))
        
        # random transition to next state
        self.current_state = self.roulette(self.g.transition(self.current_state, actions))
        
        #print(self.total_rewards)
    
        
        
    def chooseAction(self, player): 
        """
        select an action for the player according to their strategy
        """
        return self.roulette(self.policyPlayers[player][self.current_state])
    
    def gaming(self):
        while self.t <= self.iteration:
            actions = {p : self.chooseAction(p) for p in self.g.players()}
            self.step(actions)


# Test Game RPS



from RockPaperScissors import RockPaperScissors
from Soccer import Soccer
from Shapley import new_V_and_pi
from Shapley import ecart
from Shapley import shapley
from Littman import MinimaxQ
import time
import random

def testRPS(shapleyepsilon,iterationlittman,nbplay):
    print("\ngame RPS")
    game = RockPaperScissors()
    p0, p1 = game.players()[0], game.players()[1]
    print("run shapley  epsilon = ",shapleyepsilon)
    start_time = time.time()
    pi_shap,V_shap = shapley(game, epsilon = shapleyepsilon,playerA = p1,playerB = p0)
    print("Time shapley : ",time.time() - start_time)
    print("Game value by Shapley :  \n",V_shap,"\noptimal policy for playerB by Shapley :\n ",pi_shap)
    new_pi , new_V= new_V_and_pi(game, V_shap,playerA = p1,playerB = p0)
    print("ecart entre new_V et val de Shapley : ")
    print(ecart(new_V,V_shap))
    def choiceActOfPlayerType2(game,s,pi_playerB):
        return random.choice(game.actions(p1,s))
    
    print("run Littman with  ",iterationlittman," iteration" )
    start_time = time.time()
    pi_l , V_l = MinimaxQ(game,explor = .3,decay = .01 ** (1. / ( 2 *10**4)),display = 10000,iteration = 2* 10**4, choiceActPlayerB=choiceActOfPlayerType2,playerA = p0,playerB = p1 ,policyplayerB = pi_shap )
    print("Time Littman : ",time.time() - start_time)
    print("Game value by Littman : \n",V_l,"\noptimal policy for playerA by Littman  :\n",pi_l)
    new_pi , new_V= new_V_and_pi(game, V_l,playerA = p0,playerB = p1)
    print("ecart entre new_V et val de littman : ")
    print(ecart(new_V,V_l))
    print("ecart entre val de shapley et littman")
    print(ecart(V_shap,V_l))
    
    print("Test ",nbplay," game")
    randompolicy = {state: {action: 1/len(game.actions(p0, state)) for action in game.actions(p0, state)} for state in game.states()}
    policy  = {p0 : randompolicy , p1 :randompolicy }
    test = Test(game,nbplay,policyPlayers =policy )
    test.gaming()
    print("total_rewards")
    print(test.total_rewards)
    print("winers :",test.getWiners()," nombre fois arrive en etat but",test.but )
    
def testGameSoccer(shapleyepsilon,iterationlittman,nbplay):
    
    print("\ngame Soccer")
    game = Soccer()
    p0, p1 = game.players()[0], game.players()[1]
    print("\nrun shapley for player 0 \n")
    start_time = time.time()
    pi_shap_p0,V_shap_p0 = shapley(game, epsilon = shapleyepsilon,playerA = p0,playerB = p1)
    print("Time shapley : ",time.time() - start_time)
    print("Game value by Shapley : \n ",V_shap_p0," \n optimal policy for playerB by Shapley :\n",pi_shap_p0)
    new_pi , new_V= new_V_and_pi(game, V_shap_p0,playerA = p0,playerB = p1)
    print("\necart entre new_V et val de Shapley : ")
    print(ecart(new_V,V_shap_p0))
    
    print("\nrun shapley for player 1 \n")
    start_time = time.time()
    pi_shap_p1,V_shap_p1 = shapley(game, epsilon = shapleyepsilon,playerA = p1,playerB = p0)
    print("Time shapley : ",time.time() - start_time)
    print("Game value by Shapley : \n ",V_shap_p1," \n optimal policy for playerB by Shapley :\n",pi_shap_p1)
    new_pi , new_V= new_V_and_pi(game, V_shap_p1,playerA = p1,playerB = p0)
    print("\necart entre new_V et val de Shapley : ")
    print(ecart(new_V,V_shap_p1))
    
    print("aperentissage pour player 0  contre random choice pour player 1")
    policyRandomPlayer1 =  {state: {action: 1/len(game.actions(p1, state)) for action in game.actions(p1, state)} for state in game.states()}

    def choiceActOfPlayerType2(game,s,pi_playerB):
        return random.choice(game.actions(p1,s))
    start_time = time.time()
    pi_l_rand_p0 , V_l_rand_p0 = MinimaxQ(game,explor = .3,decay = .01 ** (1. / iterationlittman),display = 1000000,iteration =  iterationlittman, choiceActPlayerB=choiceActOfPlayerType2,playerA = p0,playerB = p1,policyplayerB = policyRandomPlayer1  )
    print("Time Littman : ",time.time() - start_time)
    print("Game value by Littman :  \n",V_l_rand_p0," \n optimal policy for playerA by Littman  :\n",pi_l_rand_p0)
    new_pi , new_V= new_V_and_pi(game, V_l_rand_p0,playerA = p0,playerB = p1)
    print("ecart entre new_V et val de littman : ")
    print(ecart(new_V,V_l_rand_p0))
    print("ecart entre val de player 0 trouve par shpaley  et val de player 0 trouve par littman")
    print(ecart(V_shap_p0,V_l_rand_p0))
    
    
    def choiceActOfPlayerType3(game,s,pi_playerB):
        a = pi_playerB.get(s)
        rnd = np.random.rand()
        tmp = 0
        for s, p in a.items():
            tmp += p
            if tmp >= rnd:
                return s
    print("aperentissage pour player 0  contre policy trouve pour player 1 avec shapley avec fon,ction choic de type 3")   
    start_time = time.time()
    pi_l_p0_type3 , V_l_p0_type3 = MinimaxQ(game,explor = .3,decay = .01 ** (1. / iterationlittman),display = 1000000,iteration =  iterationlittman, choiceActPlayerB=choiceActOfPlayerType3,playerA = p0,playerB = p1,policyplayerB = pi_shap_p1  )
    print("Time Littman : ",time.time() - start_time)
    print("Game value by Littman :  \n",V_l_p0_type3," \n optimal policy for playerA by Littman  :\n",pi_l_p0_type3)
    new_pi , new_V= new_V_and_pi(game, V_l_p0_type3,playerA = p0,playerB = p1)
    print("ecart entre new_V et val de littman : ")
    print(ecart(new_V,V_l_p0_type3))
    print("ecart entre val de player 0 trouve par shpaley  et val de player 0 trouve par littman")
    print(ecart(V_shap_p0,V_l_p0_type3))
    

    
    print("Test shapley player with littman player (apprentissage contre policy trouve par shapler pour player B avec fonction type 3",nbplay," fois")
    print("p0 avec littman player (apprentissage contre shapley player avec fonction type 3  et p1  avec  shapley player")
    policy = {p0: pi_l_p0_type3  , p1: pi_shap_p1 }
    test = Test(game,nbplay,policyPlayers =policy )
    test.gaming()
    print("total_rewards")
    print(test.total_rewards)
    print("winers :",test.getWiners()," nombre fois arrive en etat but",test.but )
    
    
    print("Test shapley player with littman player (apprentissage contre random player) ",nbplay," fois")
    print("p0 avec littman player (apprentissage contre random player) et p1  avec  shapley player")
    policy = {p0: pi_l_rand_p0  , p1: pi_shap_p1 }
    test = Test(game,nbplay,policyPlayers =policy )
    test.gaming()
    print("total_rewards")
    print(test.total_rewards)
    print("winers :",test.getWiners()," nombre fois arrive en etat but",test.but )
    
    
    print("Test shapley player contre random player",nbplay," fois")
    print("p0 shapley player et p1  random player")
    policy = {p0: pi_shap_p0  , p1: policyRandomPlayer1 }
    test = Test(game,nbplay,policyPlayers =policy )
    test.gaming()
    print("total_rewards")
    print(test.total_rewards)
    print("winers :",test.getWiners()," nombre fois arrive en etat but",test.but )
    
    
    print("Test littman player (apprentissage contre random player)  contre random player",nbplay," fois")
    print("p0 littman player (apprentissage contre random player) et p1  random player")
    policy = {p0: pi_l_rand_p0  , p1: policyRandomPlayer1 }
    test = Test(game,nbplay,policyPlayers =policy )
    test.gaming()
    print("total_rewards")
    print(test.total_rewards)
    print("winers :",test.getWiners()," nombre fois arrive en etat but",test.but )

    
    print("Test littman player (apprentissage contre shapley player avec fonction type 3)  contre random player",nbplay," fois")
    print("p0 littman player (apprentissage contre shapley player avec fonction type 3) et p1  random player")
    policy = {p0: pi_l_p0_type3  , p1: policyRandomPlayer1 }
    test = Test(game,nbplay,policyPlayers =policy )
    test.gaming()
    print("total_rewards")
    print(test.total_rewards)
    print("winers :",test.getWiners()," nombre fois arrive en etat but",test.but )
    
    
    print("Test shapley player contre shapley player",nbplay," fois")
    print("p0 shapley player et p1  shapley player")
    policy = {p0: pi_shap_p0  , p1: pi_shap_p1 }
    test = Test(game,nbplay,policyPlayers =policy )
    test.gaming()
    print("total_rewards")
    print(test.total_rewards)
    print("winers :",test.getWiners()," nombre fois arrive en etat but",test.but )


#testRPS(shapleyepsilon = 0.0,iterationlittman = 2 *  10 ** 4,nbplay = 10**7)
    
testGameSoccer(shapleyepsilon = 10** -13 ,iterationlittman = 2 * 10**7 ,nbplay = 10 ** 6)







