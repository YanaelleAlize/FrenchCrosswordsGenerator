# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 10:56:56 2019

@author: yoann
"""

from src.DICO_package.definition import definition

import random as rd

class word:
              
    def __init__(self, id, word_txt, defs):
        # list_def_coeffpertinance stocké sous forme de tuples définition de quelques mots
        self._nb_defs = len(defs)
        self._sum_defs = sum([x.getCoeff() for x in defs])
        self._defs = defs
        self._id = id
        self._word_txt = word_txt
    
    def append_def(self, one_def):
        try :
            one_def.isdef()
        except Exception as e :
            print(e)
        if not(one_def in self._defs):
            self._defs.append(one_def)
            self._nb_defs += 1
            self._sum_defs += one_def.getCoeff()
        else :
            print("{} already in the definition list !".format(one_def))
        
    def delete_def(self, one_def):
        for i, xi in self._defs:
            if xi == one_def :
                del self._defs[i]
                break
    
    def getNBdefs(self):
        return self._nb_defs
    
    def getSUMdefs(self):
        return self._sum_defs
    
    def getDefs(self):
        return self._defs
    
    def getID(self):
        return self._id
    
    def _setID(self, id):
        self._id = id
        
    def getWordTXT(self):
        return self._word_txt
    
    def setWordTXT(self, word_txt):
        self._word_txt = word_txt
    
    def get_random_def(self):
        index = rd.randint(0, self._sum_defs - 1)
        tmp_sum_coeffs = 0
        for i in range(len(self._defs)):
            tmp_sum_coeffs += self._defs[i].getCoeff()
            if tmp_sum_coeffs > index:
                return self._defs[i].getTXT()
            
    def __repr__(self):
        return "d(id : {}, word_txt : {}, nb_defs : {}\n".format(self._id, self._word_txt, self._nb_defs) + "".join(("\t" + x.__str__() + "\n" for x in self._defs)) + ")"
    
    def reprJSON(self):
        return {"__type__" : "__word__",
                "id" : self._id, 
                "defs" : self._defs,
                "word_txt" : self._word_txt}