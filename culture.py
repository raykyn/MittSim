#! /usr/bin/python3

import regex as re
import random
import csv
from collections import Counter

class start_Cultures():
    def __init__(self):
        # This build all models, so the cultures can later use them
        
        self.n = 3
        
        self.BOS_SYMBOL = object()
        self.EOS_SYMBOL = object()
        
        path="data/person_names/"
        
        self.models = {
            "german":"p_germany.txt",
            "french":"p_france.txt",
            "english":"p_england.txt",
            "spanish":"p_spain.txt",
            "russian":"p_russia.txt",
            "swedish":"p_sweden.txt",
            "finnish":"p_finland.txt",
            "greek":"p_greece.txt",
            "serbian":"p_serbia.txt",
            "irish":"p_ireland.txt",
            "bulgarian":"p_bulgaria.txt",
            "turkish":"p_turkey.txt",
            "steppes":"p_steppes.txt",
            "chinese":"p_china.txt",
            "indian":"p_india.txt",
            "vietnamese":"p_viet.txt",
            "korean":"p_korea.txt",
            "japanese":"p_japan.txt",
            "arabian":"p_arabia.txt",
            "hebrew":"p_israel.txt",
            "georgian":"p_georgia.txt",
            "italian":"p_italy.txt"
        }
        
        for key, value in self.models.items():
            self.models[key] = self._build_model(path+value, self.n)
            
        self.models["german_towns"] = self._build_town_model("data/towns_de.txt", self.n, "latin1")
        self.models["english_towns"] = self._build_town_model("data/towns.csv", self.n, "utf8")
        self.models["arabian_towns"] = self._build_town_model("data/SY_clear.txt", self.n, "utf8")
        
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
        self.BOS_SYMBOL = object()
        self.EOS_SYMBOL = object()
        
        self.name = ""
        
        # Choose a culture as model
        # At the moment
        # - german
        # - english
        
        possible = [
            ("german", "german_towns"),
            ("english", "english_towns"),
            ("arabian", "arabian_towns")
        ]
        self.model = random.choice(possible)

        
    #~ def read_namelist(self, infile, outfile, pos):
        #~ genders = r'M|=|F|?'
        #~ with open(infile, mode="r", encoding="latin1") as inf, \
            #~ open(outfile, mode="w", encoding="utf8") as outf:
            #~ for line in inf:
                #~ if not line.startswith("#"):
                    #~ m = re.match(r"(\??1?["+genders+"])\s+(\S+\s?\S+)\s+(.+)\$", line)
                    #~ if m:
                        #~ sex = m.group(1)
                        #~ name = m.group(2)
                        #~ name = self._replace_iso(name)
                        #~ occ = m.group(3)
                        #~ if sex == "?M" or sex == "1M":
                            #~ sex = "M"
                        #~ elif sex == "?F" or sex == "1F":
                            #~ sex = "F"
                        #~ elif sex == "=":
                            #~ sex = lastsex
                        #~ try:
                            #~ if int(occ[-pos]) > 0:
                                #~ print(sex, name)
                                #~ outf.write("{}\t{}\t{}\n".format(sex, name, occ[-pos]))
                        #~ except:
                            #~ pass
                        #~ lastsex = sex
                    #~ else:
                        #~ print(line)
    
    #~ def _replace_iso(self, name):
        #~ repl_dict = {
            #~ "<A/>":"\u0100",
            #~ "<a/>":"\u0101",
            #~ "<Â>":"\u0102",                                                     
            #~ "<â>":"\u0103",                                                      
            #~ "<A,>":"\u0104",                                                           
            #~ "<a,>":"\u0105",
            #~ "<C´>":"\u0106",                                                         
            #~ "<c´>":"\u0107",                                                           
            #~ "<C^>":"\u010C", 
            #~ "<CH>":"\u010C",                                                     
            #~ "<c^>":"\u010D", 
            #~ "<ch>":"\u010D",
            #~ "<d´>":"\u010F",                                                            
            #~ "<Ð>":"\u0110",
            #~ "<DJ>":"\u0110",                                                     
            #~ "<ð>":"\u0111",
            #~ "<dj>":"\u0111",                                                     
            #~ "<E/>":"\u0112",                                                            
            #~ "<e/>":"\u0113",                                                            
            #~ "<E°>":"\u0116",                                                            
            #~ "<e°>":"\u0117",                                                            
            #~ "<E,>":"\u0118",                                                            
            #~ "<e,>":"\u0119",                                                            
            #~ "<Ê>":"\u011A",                                                             
            #~ "<ê>":"\u011B",                                                           
            #~ "<G\^>":"\u011E",                                                          
            #~ "<g\^>":"\u011F",                                                            
            #~ "<G,>":"\u0122",                                                            
            #~ "<g´>":"\u0123",                                                            
            #~ "<I/>":"\u012A",                                                            
            #~ "<i/>":"\u012B",                                                            
            #~ "<I°>":"\u0130",                                                            
            #~ "<i>":"\u0131",                                                             
            #~ "<IJ>":"\u0132",                                                            
            #~ "<ij>":"\u0133",                                                            
            #~ "<K,>":"\u0136",                                                            
            #~ "<k,>":"\u0137",                                                            
            #~ "<L,>":"\u013B",                                                            
            #~ "<l,>":"\u013C",                                                            
            #~ "<L´>":"\u013D",                                                            
            #~ "<l´>":"\u013E",                                                            
            #~ "<L/>":"\u0141",                                                            
            #~ "<l/>":"\u0142",                                                            
            #~ "<N,>":"\u0145",                                                            
            #~ "<n,>":"\u0146",                                                            
            #~ "<N\^>":"\u0147",                                                            
            #~ "<n\^>":"\u0148",                                                            
            #~ "<Ö>":"\u0150",                                                             
            #~ "<ö>":"\u0151",                                                             
            #~ "":"\u0152", 
            #~ "<OE>":"\u0152",                                             
            #~ "":"\u0153", 
            #~ "<oe>":"\u0153",                                                       
            #~ "<R\^>":"\u0158",                                                            
            #~ "<r\^>":"\u0159",                                                            
            #~ "<S,>":"\u015E",                                                            
            #~ "<s,>":"\u015F",                                                            
            #~ "":"\u0160",
            #~ "<S\^>":"\u0160",
            #~ "<SCH>":"\u0160", 
            #~ "<SH>":"\u0160",                                 
            #~ "":"\u0161", 
            #~ "<s\^>":"\u0161", 
            #~ "<sch>":"\u0161", 
            #~ "<sh>":"\u0161",                                    
            #~ "<T,>":"\u0162",                                                            
            #~ "<t,>":"\u0163",                                                            
            #~ "<t´>":"\u0165",                                                            
            #~ "<U/>":"\u016A",                                                            
            #~ "<u/>":"\u016B",                                                            
            #~ "<U°>":"\u016E",                                                            
            #~ "<u°>":"\u016F",                                                            
            #~ "<U,>":"\u0172",                                                            
            #~ "<u,>":"\u0173",                                                             
            #~ "<Z°>":"\u017B",                                                             
            #~ "<z°>":"\u017C",                                                             
            #~ "<Z\^>":"\u017D",                                                             
            #~ "<z\^>":"\u017E",                                                             
            #~ "<ß>":"\u1E9E",  
        #~ }
        #~ for key, value in repl_dict.items():
            #~ name = re.sub(key, value, name)
        #~ return name
        
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
    culture = Culture()
    #print(culture.generate_name(init, "german", "m"))
    name = culture.generate_name(init, "t") 
    while len(name) < 6 or len(name) > 15 or ' ' in name or '-' in name:
        name = culture.generate_name(init, "t")
    print(name)
    
    #de_model = culture.build_model("data/person_names/p_ireland.txt", 3)
    #print(culture.generate_name(de_model[1], 3))
    #culture.read_namelist("data/nam_dict.txt","p_test.txt",57)
    
if __name__ == "__main__":
    main()
