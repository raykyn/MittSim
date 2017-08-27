#! /usr/bin/python3

from culture import Culture
import random

class Character():
    def __init__(self, models, culture, residence, age):
        self.culture = culture
        self.models = models
        self.place = residence
        # Fullname will later always be set to highest title
        self.age = age
        self.state = "alive" # alive or dead
        self.titles = []
        g = random.randint(0,1)
        if g == 0:
            self.gender = "m"
            self.firstname = culture.generate_name(models, "m")
        else:
            self.gender = "f"
            self.firstname = culture.generate_name(models, "f")
        self.fullname = ""
        self.refresh_fullname()
        
        self.skills = {
            "Diplomacy":0,
            "Military":0,
            "Commerce":0,
            "Intrigue":0,
            "Scholarship":0
            }
        
        self.competence = 0
        
        self.assign_skillpoints()
        
        self.focus = []
        
        self.setfocus()
        
        
    def refresh_fullname(self):
        highest_title = self.get_highest_title()
        self.fullname = "{} {}".format(highest_title, self.firstname)
        
    
    def assign_skillpoints(self):
        free_points = 0
        for i in range(4):
            free_points += random.randint(1,6)
        self.competence = free_points
        for i in range(free_points):
            while True:
                r = random.randint(1,5)
                if r == 1 and self.skills["Diplomacy"] < 5:
                    self.skills["Diplomacy"] += 1
                    break
                elif r == 2 and self.skills["Military"] < 5:
                    self.skills["Military"] += 1
                    break
                elif r == 3 and self.skills["Commerce"] < 5:
                    self.skills["Commerce"] += 1
                    break
                elif r == 4 and self.skills["Intrigue"] < 5:
                    self.skills["Intrigue"] += 1
                    break
                elif r == 5 and self.skills["Scholarship"] < 5:
                    self.skills["Scholarship"] += 1
                    break
                    
    
    def setfocus(self):
        """ Returns a list of the highest skills."""
        highest = [k for k,v in self.skills.items() if v == max(self.skills.values())]
        self.focus = highest

        
    def get_highest_title(self):
        if len(self.titles) > 0:
            titles_levels = []
            for t in self.titles:
                titles_levels.append((t, t.level))
            h_title = sorted(titles_levels, key=lambda x: x[1], reverse=True)[0][0]
            if self.gender == "m":
                return h_title.getMTitle()
            else:
                return h_title.getFTitle()
        else:
            if self.gender == "m":
                return "Sir"
            else:
                return "Lady"
                
            
    def _age(self):
        self.age += 1
        if self.age > 50: # Age 100 100% dead, 50 0.1 % dead chance
            chance_to_die = (self.age - 50)*0.2
            m = random.randint(1,100)
            if m <= chance_to_die:
                self.die()
        
        
    def die(self):
        # Lose title if has any and distribute them to successors
        # Standard succession type is Gavelkind => depending on Culture
        # Next line is only a placeholder until a proper system is implemented
        successor = Character(models, self.culture, self.place, random.randint(30,60))
        self.state = "dead"
