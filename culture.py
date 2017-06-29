#! /usr/bin/python3

import regex as re
import random
import csv
import math
import pickle
from collections import Counter

class start_Cultures():
    def __init__(self):
        # This build all models, so the cultures can later use them
        
        self.n = 3
        
        self.BOS_SYMBOL = "BOS"
        self.EOS_SYMBOL = "EOS"
        
    def load_all(self):
        with open('data/models.pkl', 'rb') as f:
            self.models = pickle.load(f)
        
    def build_all(self):
        path="data/person_names/"
        self.models = {
            "german":"p_germany.txt", #done
            "french":"p_france.txt", 
            "english":"p_england.txt", #done
            "spanish":"p_spain.txt",
            "russian":"p_russia.txt",
            "swedish":"p_sweden.txt", #1
            "finnish":"p_finland.txt", #2
            "greek":"p_greece.txt",
            "serbian":"p_serbia.txt",
            "irish":"p_ireland.txt",
            "bulgarian":"p_bulgaria.txt",
            "turkish":"p_turkey.txt",
            "steppes":"p_steppes.txt",
            "chinese":"p_china.txt", #3
            "indian":"p_india.txt", #4
            "vietnamese":"p_viet.txt",
            "korean":"p_korea.txt",
            "japanese":"p_japan.txt", #5
            "arabian":"p_arabia.txt", #done
            "hebrew":"p_israel.txt",
            "georgian":"p_georgia.txt",
            "italian":"p_italy.txt"
        }
        
        for key, value in self.models.items():
            self.models[key] = self._build_model(path+value, self.n)
            
        self.models["german_towns"] = self._build_town_model("data/towns_de.txt", self.n, "latin1")
        self.models["english_towns"] = self._build_town_model("data/GB_clear.txt", self.n, "utf8")
        self.models["arabian_towns"] = self._build_town_model("data/SY_clear.txt", self.n, "utf8")
        self.models["spanish_towns"] = self._build_town_model("data/ES_clear.txt", self.n, "utf8")
        self.models["finnish_towns"] = self._build_town_model("data/FI_clear.txt", self.n, "utf8")
        self.models["swedish_towns"] = self._build_town_model("data/SE_clear.txt", self.n, "utf8")
        self.models["japanese_towns"] = self._build_town_model("data/JP_clear.txt", self.n, "utf8")
        self.models["indian_towns"] = self._build_town_model("data/IN_clear.txt", self.n, "utf8")
        self.models["russian_towns"] = self._build_town_model("data/RU_clear.txt", self.n, "utf8")
        
        with open('data/models.pkl', 'wb') as f:
            pickle.dump(self.models, f, pickle.HIGHEST_PROTOCOL)
        
    def _build_model(self, infile, n):
        ngram_dict_m = Counter()
        ngram_dict_f = Counter()
        with open(infile, mode="r", encoding="utf8") as inf:
            reader = csv.reader(inf, delimiter="\t")
            for row in reader:
                ngrams = self._find_ngrams(row[1], n)
                for ngram in ngrams:
                    if row[0] == "M":
                        ngram_dict_m[ngram] += int(row[2])
                    elif row[0] == "F":
                        ngram_dict_f[ngram] += int(row[2])
        return (ngram_dict_m, ngram_dict_f)
        
    def _build_town_model(self, infile, n, enc="utf8"):
        ngram_dict = Counter()
        with open(infile, mode="r", encoding=enc) as inf:
            for line in inf:
                line = line.rstrip("\n")
                ngrams = self._find_ngrams(line, n)
                for ngram in ngrams:
                    ngram_dict[ngram] += 1
        return ngram_dict
                

    def _find_ngrams(self, name, n):
        """Returns the n-grams contained in @param sentence."""
        # beginning of sentence
        symbols = [self.BOS_SYMBOL] * (n-1)
        # actual characters; unknowns are not replaced (see exercise sheet)
        symbols += [char for char in name]
        # end of sentence
        symbols += [self.EOS_SYMBOL]
        # n-gram extraction, as in https://goo.gl/91x6P6
        return list(zip(*[symbols[i:] for i in range(n)]))
        
    def get_model(self, name):
        return self.models[name]
        
    def get_n(self):
        return self.n
        

class Culture(object):
    def __init__(self):
        self.BOS_SYMBOL = "BOS"
        self.EOS_SYMBOL = "EOS"
        
        self.name = ""
        
        # Choose a culture as model
        # At the moment
        # - german
        # - english
        
        possible = [
            ("german", "german_towns"),
            ("english", "english_towns"),
            ("arabian", "arabian_towns"),
            ("finnish", "finnish_towns"),
            ("swedish", "swedish_towns"),
            ("japanese", "japanese_towns"),
            ("indian", "indian_towns"),
            ("russian", "russian_towns"),
            ("spanish", "spanish_towns"),
        ]
        self.model = random.choice(possible)

        
    def generate_name(self, other, sex):
        n = other.n
        if sex == "m":
            ngram_dict = other.get_model(self.model[0])[0]
        elif sex == "f":
            ngram_dict = other.get_model(self.model[0])[1]
        elif sex == "t":
            ngram_dict = other.get_model(self.model[1])
        else:
            print("No sex!")
        last_body = []
        for i in range(0, n-1):
            last_body.append(other.BOS_SYMBOL)
        name = []
        name.extend(last_body)
        while True:
            possibles = []
            for key, value in ngram_dict.items():
                head = key[0:-1]
                tail = key[-1]
                if head == tuple(name[-n+1:]):
                    for i in range(0, value):
                        possibles.append(tail)
            chosen = random.choice(possibles)
            name.append(chosen)
            if chosen == other.EOS_SYMBOL:
                while True:
                    try:
                        name.remove(other.BOS_SYMBOL)
                    except:
                        break
                name.remove(other.EOS_SYMBOL)
                return ''.join(name)
    
def main():
    init = start_Cultures()
    init.load_all()
    culture = Culture()
    #print(culture.generate_name(init, "german", "m"))
    for i in range(0,10):
        name = culture.generate_name(init, "t") 
        while len(name) < 6 or len(name) > 15 or ' ' in name or '-' in name:
            name = culture.generate_name(init, "t")
        print(name)
    print(culture.model)
    
    
    #de_model = culture.build_model("data/person_names/p_ireland.txt", 3)
    #print(culture.generate_name(de_model[1], 3))
    #culture.read_namelist("data/nam_dict.txt","p_test.txt",57)
    
if __name__ == "__main__":
    main()
