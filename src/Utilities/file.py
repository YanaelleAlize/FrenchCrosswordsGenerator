# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 18:13:02 2019

@author: yoann
"""

class file :
    
    def __init__(self):
        self._contenu = []
        
    def enfile(self, element):
        self._contenu.append(element)
        
    def defile(self):
        self._contenu.pop(0)
        
    def __repr__(self):
        return self._contenu.__str__()