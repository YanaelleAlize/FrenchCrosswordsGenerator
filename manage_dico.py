# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 21:00:28 2019

@author: yoann
"""

import json
import os
import pickle

from src.DICO_package.definition import definition
from src.DICO_package.word import word
from src.In_package.In_utilities import *
from src.Utilities.file import file

dico_path = os.path.join("data", "Dicos")

c2i = {chr(ord("a") + i) : i for i in range(0, 26)}
i2c = {i : chr(ord("a") + i) for i in range(0, 26)}

class JSON_Custom_Encoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)
        

class JSON_Custom_Decoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "__type__" in obj:
            type = obj["__type__"]
            if type == "__definition__" :
                return definition(obj["txt"], obj["coeff"])
            if type == "__word__" :
                return word(obj["id"], obj["word_txt"], obj["defs"])
            return obj
        return obj
    

class dico_entries:
    
    def __init__(self):
        self._dico = {}
        
    def append_word(self, w, id_w):
        if not w in self._dico.values() and not id_w in self._dico :
            self._dico[id_w] = w
            return True
        return False
        
    def delete_word(self, id_w):
        if id_w in self._dico :
            del self._dico[id_w]
    
    def merge(self, other, trans_index):
        for id_w in other:
            self._dico[trans_index + id_w] = other[id_w]
        
    def json_load(self, filepath):
        with open(filepath, "r") as f :
            json_string = f.read()
            f.close()
        self._dico = json.loads(json_string, cls = JSON_Custom_Decoder)

    def json_save(self, filepath):
        with open(filepath, "w") as f :
            json_string = json.dumps(self._dico, cls = JSON_Custom_Encoder)
            f.write(json_string)
            f.flush()
            f.close()
    
    def __repr__(self):
        return self._dico.__repr__()
    
class dico_search_tree:
    
    def __init__(self):
        self._fils = {}
        self._liste_etq = []
        
    def is_w_in(self, list_str_w, profondeur = 0):
        """
        if profondeur >= len(list_str_w):
            return self._liste_etq
        ret_list = []
        for x in self._fils.values():
            ret_list += x.is_w_in(list_str_w, profondeur + 1)
        return ret_list
        """
        if profondeur >= len(list_str_w):
            return self._liste_etq
        if list_str_w[profondeur] in self._fils :
            return self._fils[list_str_w[profondeur]].is_w_in(list_str_w, profondeur + 1)
        return []
        
    def insert_word(self, id_w, list_str_w, profondeur = 0):
        if profondeur >= len(list_str_w):
            if not id_w in self._liste_etq :
                self._liste_etq.append(id_w)
                return True
        else :
            if list_str_w[profondeur] in self._fils :
                self._fils[list_str_w[profondeur]].insert_word(id_w, list_str_w, profondeur + 1)
            else :
                new_dico = dico_search_tree()
                new_dico.insert_word(id_w, list_str_w, profondeur + 1)
                self._fils[list_str_w[profondeur]] = new_dico
        return False
    
    def delete_word(self, id_w, list_str_w, profondeur = 0):
        if profondeur >= len(list_str_w):
            if id_w in self._liste_etq :
                self._liste_etq.remove(id_w)
        else :
            if list_str_w[profondeur] in self._fils :
                self._fils[list_str_w[profondeur]].delete_word(id_w, list_str_w, profondeur + 1)

    def merge(self, search_tree, trans_index):
        # Parcours en largeur, il nous faut une file de priorites
        for etq in search_tree._liste_etq :
            if not etq in self._liste_etq :
                self._liste_etq.append(etq + trans_index)
        for fils_other in search_tree._fils :
            if fils_other in self._fils :
                self._fils[fils_other].merge(search_tree._fils[fils_other], trans_index)
            else :
                # il faut deplacer les index du fils
                self._fils[fils_other] = dico_search_tree().merge(search_tree._fils[fils_other], trans_index)        
    
    def b_load(self, filepath):
        s = pickle.load(open(filepath, "rb"))
        self.__dict__.update(s.__dict__)
    
    def b_save(self, filepath):
        pickle.dump(self, open(filepath, "wb"))
    
    def __repr__(self):       
        return "Parcours de l'arbre de recherche :\n" + self.parcours__repr__()
            
    def parcours__repr__(self, base_str = ""):
        # Largeur
        msg = ""
        for x in self._liste_etq :
            msg += "\t{" + base_str + " : " + str(x) + "}\n"
        for f in self._fils :
            msg += self._fils[f].parcours__repr__(base_str + f)
        return msg
    
class dico:
    
    def __init__(self):
        self._nb = 0
        self._entries = dico_entries()
        self._search_tree = dico_search_tree()
    
    def append_word(self, w):
        if self._entries.append_word(w, str(self._nb)):
            self._search_tree.insert_word(str(self._nb), list(w.getWordTXT()))
            self._nb += 1
            return True
        return False
    
    def load(self, filename):
        load_path = os.path.join(dico_path, filename)
        # LOAD ARGS
        args = pickle.load(open(os.path.join(load_path, "args"), "rb"))
        self._nb = args[0]
        # LOAD ENTRIES
        self._entries.json_load(os.path.join(load_path, "entries"))
        # LOAD SEARCH TREE
        self._search_tree.b_load(os.path.join(load_path, "tree"))

    def load_multi(self, filenames):
        dicos = []
        temp_dico = dico()
        for filename in filenames:
            try :
                temp_dico.load(filename)
                dicos.append(temp_dico)
            except Exception as e:
                print("Can't load {} because of :\n\t{}".format(filename, e))
                
        self.merge_multi(dicos)
    
    def merge_multi(self, dicos):
        for x in dicos :
            self.merge(x)
        
    def merge(self, other):
        self._nb += other._nb
        self._entries.merge(other._entries, self._nb)
        self._search_tree.merge(other._search_tree, self._nb)
        
    def save(self, filename):
        save_path = os.path.join(dico_path, filename)
        abort = False
        try :
            os.mkdir(save_path)
        except FileExistsError :
            abort = not ask_Y_or_N("The dictionnary {} already exists, do you want to overwrite it ?".format(filename))
        if abort :
            print("Abortion of the saving procedure.")
        else :
            # SAVE ARGS
            pickle.dump([self._nb], open(os.path.join(save_path, "args"), "wb"))
            # SAVE ENTRIES
            self._entries.json_save(os.path.join(save_path, "entries"))
            # SAVE SEARCH TREE
            self._search_tree.b_save(os.path.join(save_path, "tree"))
            
    def __repr__(self):
        return self._search_tree.__repr__() + "\nDictionnaire des entrées :\n" + self._entries.__str__()

def handle_dico_creation():
    print("Bienvenido in the dictionnary creation process for custom crosswords :")
    while True:
        pass
        
if __name__ == "__main__" :
    au = definition("De l'or d'après Mendeleiev", 100)
    wrd = word(str(0), "au", [au])
    d = dico()
    d.append_word(wrd)
    print(d)