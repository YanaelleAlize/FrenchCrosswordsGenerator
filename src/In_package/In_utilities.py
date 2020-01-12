# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 13:16:24 2019

@author: yoann
"""

Y_or_N_possibles = {"Y" : ["Y", "y", "Yes", "yes", "O", "o", "Oui", "oui"], "N" : ["N", "n", "No", "no", "Non", "non"]}

def add_slashes(L):
    str = ""
    n = len(L)
    for i, x in enumerate(L):
        str += x
        if i < n - 1 :
            str += "/"
    return str

class UnRecoAnswer(Exception):
    
    def __init__(self, answer, possibles):
        self._a = answer
        self._p = possibles
        
    def __str__(self):
        msg = "Unrecognized answer : << {} >>. Please answer with ".format(self._a)
        n = len(self._p)
        for i, x in enumerate(self._p) :
            if i == n - 1 :
                break
            elif i != 0 :
                msg += ", "
            msg += add_slashes(x)
        msg += " or " + add_slashes(x)
        return msg

def ask_Y_or_N(question):
    while True :
        try :
            answer = input(question + " (Y/N)\n\t")
            if answer in Y_or_N_possibles["Y"]:
                return True
            elif answer in Y_or_N_possibles["N"]:
                return False
            else :
                raise UnRecoAnswer(answer, Y_or_N_possibles.values())
        except UnRecoAnswer as e:
            print(e)

def ask_dico(question, dico):
    """
    Function that takes a dictionnary of commands that call other functions.
    """
    while True :
        try :
            answer = input(question + " :\n\t")
            list_answer = answer.strip().split(" ")
            if list_answer[0] == "help" :
                if list_answer[0] in dico :
                    dico[list_answer.pop(0)](list_answer)
                else :
                    for x in dico.values() :
                        help(x)
            elif list_answer[0] in dico :
                foo = list_answer.pop(0)
                return dico[foo](list_answer)
            else :
                raise UnRecoAnswer(answer, dico.keys())
        except UnRecoAnswer as e:
            print(e)