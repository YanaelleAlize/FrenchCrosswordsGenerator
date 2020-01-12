# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 11:00:29 2019

@author: yoann
"""

class definition:
    
    def __init__(self, txt, coeff):
        self._txt = txt
        self._coeff = coeff
        
    def getTXT(self):
        return self._txt
    
    def getCoeff(self):
        return self._coeff

    def setTXT(self, txt):
        self._txt = txt
        
    def setCoeff(self, coeff):
        self._coeff = coeff
    
    def isdef():
        return True
    
    def __repr__(self):
        return "d{def : " + self._txt + ", coeff : " + str(self._coeff) + "}"
    
    def reprJSON(self):
        return {"__type__" : "__definition__", "txt" : self._txt, "coeff" : self._coeff}