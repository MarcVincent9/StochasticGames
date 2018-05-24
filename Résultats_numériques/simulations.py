# -*- coding: utf-8 -*-

# Test Game RPS

from RockPaperScissors import RockPaperScissors
from Soccer import Soccer
from Shapley import new_V_and_pi
from Shapley import ecart
from Shapley import shapley
from Littman import MinimaxQ
from Test import Test
import time
import random
import numpy as np




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
    
    
    policyRandomPlayer1 =  {state: {action: 1/len(game.actions(p1, state)) for action in game.actions(p1, state)} for state in game.states()}
    
    print("run Littman with  ",iterationlittman," iteration" )
    start_time = time.time()
    pi_l , V_l = MinimaxQ(game,explor = .3,decay = .01 ** (1. / ( 2 *10**4)),display = 10000,iteration = 2* 10**4, playerA = p0,playerB = p1 ,policyplayerB = policyRandomPlayer1 )
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
    test.simulation()
    print("total_rewards")
    print(test.total_rewards)
    print("winers :",test.get_winners()," nombre fois arrive en etat but",test.but )
    
    
    
    
    
    
def testGameSoccer(shapleyepsilon, iterationlittman, nbplay):
    
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

    start_time = time.time()
    pi_l_rand_p0 , V_l_rand_p0 = MinimaxQ(game,explor = .3,decay = .01 ** (1. / iterationlittman),display = 1000000,iteration =  iterationlittman,playerA = p0,playerB = p1,policyplayerB = policyRandomPlayer1  )
    print("Time Littman : ",time.time() - start_time)
    print("Game value by Littman :  \n",V_l_rand_p0," \n optimal policy for playerA by Littman  :\n",pi_l_rand_p0)
    new_pi , new_V= new_V_and_pi(game, V_l_rand_p0,playerA = p0,playerB = p1)
    print("ecart entre new_V et val de littman : ")
    print(ecart(new_V,V_l_rand_p0))
    print("ecart entre val de player 0 trouve par shpaley  et val de player 0 trouve par littman")
    print(ecart(V_shap_p0,V_l_rand_p0))
    
     
    print("aperentissage pour player 0  contre policy trouve pour player 1 avec shapley avec fon,ction choic de type 3")   
    start_time = time.time()
    pi_l_p0_type3 , V_l_p0_type3 = MinimaxQ(game,explor = .3,decay = .01 ** (1. / iterationlittman),display = 1000000,iteration =  iterationlittman, playerA = p0,playerB = p1,policyplayerB = pi_shap_p1  )
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
    test.simulation()
    print("total_rewards")
    print(test.total_rewards)
    print("winers :",test.get_winners()," nombre fois arrive en etat but",test.but )
    
    
    print("Test shapley player with littman player (apprentissage contre random player) ",nbplay," fois")
    print("p0 avec littman player (apprentissage contre random player) et p1  avec  shapley player")
    policy = {p0: pi_l_rand_p0  , p1: pi_shap_p1 }
    test = Test(game,nbplay,policyPlayers =policy )
    test.simulation()
    print("total_rewards")
    print(test.total_rewards)
    print("winers :",test.get_winners()," nombre fois arrive en etat but",test.but )
    
    
    print("Test shapley player contre random player",nbplay," fois")
    print("p0 shapley player et p1  random player")
    policy = {p0: pi_shap_p0  , p1: policyRandomPlayer1 }
    test = Test(game,nbplay,policyPlayers =policy )
    test.simulation()
    print("total_rewards")
    print(test.total_rewards)
    print("winers :",test.get_winners()," nombre fois arrive en etat but",test.but )
    
    
    print("Test littman player (apprentissage contre random player)  contre random player",nbplay," fois")
    print("p0 littman player (apprentissage contre random player) et p1  random player")
    policy = {p0: pi_l_rand_p0  , p1: policyRandomPlayer1 }
    test = Test(game,nbplay,policyPlayers =policy )
    test.simulation()
    print("total_rewards")
    print(test.total_rewards)
    print("winers :",test.get_winners()," nombre fois arrive en etat but",test.but )

    
    print("Test littman player (apprentissage contre shapley player avec fonction type 3)  contre random player",nbplay," fois")
    print("p0 littman player (apprentissage contre shapley player avec fonction type 3) et p1  random player")
    policy = {p0: pi_l_p0_type3  , p1: policyRandomPlayer1 }
    test = Test(game,nbplay,policyPlayers =policy )
    test.simulation()
    print("total_rewards")
    print(test.total_rewards)
    print("winers :",test.get_winners()," nombre fois arrive en etat but",test.but )
    
    
    print("Test shapley player contre shapley player",nbplay," fois")
    print("p0 shapley player et p1  shapley player")
    policy = {p0: pi_shap_p0  , p1: pi_shap_p1 }
    test = Test(game,nbplay,policyPlayers =policy )
    test.simulation()
    print("total_rewards")
    print(test.total_rewards)
    print("winers :",test.get_winners()," nombre fois arrive en etat but",test.but )


#testRPS(shapleyepsilon = 0.0,iterationlittman = 2 *  10 ** 4,nbplay = 10**7)
    
testGameSoccer(shapleyepsilon = 10** -13 ,iterationlittman = 2 * 10**7 ,nbplay = 10 ** 6)


