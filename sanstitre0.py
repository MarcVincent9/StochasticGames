# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 18:33:03 2018

@author: Marc
"""

# preuve qu'on ne peut pas surcharger les methodes...
# a la limite : methode de verification des parametres dans SG...

import abc

class A:
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def f(a):
        return
    

class B(A):
    
    def f(a, b):
        print(a+b)
        

B.f(1)