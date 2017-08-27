#! /usr/bin/python3

import random


m_titles = {
    "Feudal":["Count", "Duke", "King", "Emperor"],
    "Republic":["Mayor", "Lord Mayor", "King-Mayor", "Serene King-Mayor"],
    "Theocracy":["High Priest", "Archpriest", "King-Priest", "Holy Emperor"]
    }
f_titles = {
    "Feudal":["Countess", "Duchess", "Queen", "Empress"],
    "Republic":["Mayoress", "Lady Mayoress", "Queen-Mayoress", "Serene Queen-Mayoress"],
    "Theocracy":["High Priestess", "Archpriestess", "Queen-Priestess", "Holy Empress"]
    }


class Title():
    def __init__(self, name, liege, vasalls, holdings, level):
        self.name = name
        self.liege = liege
        self.vasalls = vasalls
        self.holdings = holdings # Only lowest level usually
        self.level = level
        
        self.government_form = "Feudal"
        
        self.m_title = self.getMTitle()
        self.f_title = self.getFTitle()
        
    def getMTitle(self):
        return m_titles[self.government_form][self.level-1]
        
    def getFTitle(self):
        return f_titles[self.government_form][self.level-1]
        
    def setGovFormGameStart(self, focus):
        possibles = []
        if "Military" in focus:
            possibles.append("Feudal")
        if "Commerce" in focus:
            possibles.append("Republic")
        if "Scholarship" in focus:
            possibles.append("Theocracy")
        if len(possibles) > 0:
            self.government_form = random.choice(possibles)
        else:
            self.government_form = "Feudal"
