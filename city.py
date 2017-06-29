#! /usr/bin/python3

import random
from culture import Culture
from characters import Character

class City():
    def __init__(self, simMap, field, x, y):
        self.name = "No Name Yet"
        self.empire = None
        self.county = "No Name Yet"
        self.culture = None
        self.culture_name = ""
        self.color = "purple"
        self.active = False
        self.pop = random.randint(100, 300)
        self.tech = 0
        self.simMap = simMap
        self.fields = simMap.fields
        self.field = field
        self.seed = random.randint(0, 9) # splits cities into ten groups
        self.x = x
        self.y = y
        self.ressources = []
        self.terrain = []
        self.values = {"f":0,"p":0,"m":0}
        self.growth = 0.0
        self.leader = None
        
    def detect_ressources(self):
        self.ressources = []
        self.terrain = []
        for f in self.field.field_neighbor(2):
            if f.ressource is not None and (f.owner is None or f.owner == self):
                self.ressources.append(f.ressource)
            elif (f.owner is None or f.owner == self):
                self.terrain.append(f.height)
                
    def calculate_values(self):
        # Dictionary for what terrain the city gets what
        # Three general ressources:
        # - food (important for growth)
        # - production (important if war and technology)
        # - money (important for trade, war and culture)
        terrain_dict = {
            0:{"f":1,"p":0,"m":3},
            1:{"f":3,"p":0,"m":1},
            2:{"f":2,"p":1,"m":1},
            3:{"f":2,"p":1,"m":1},
            4:{"f":1,"p":2,"m":1},
            5:{"f":1,"p":2,"m":1},
            6:{"f":0,"p":2,"m":2}
        }
        ressource_dict = {
            "fishes":{"f":2,"p":0,"m":0},
            "pearls":{"f":1,"p":0,"m":1},
            "crabs":{"f":2,"p":0,"m":0},
            "whales":{"f":1,"p":1,"m":1},
            "horses":{"f":1,"p":2,"m":0}, # Bonus in Warfare
            "fruits":{"f":2,"p":0,"m":0},
            "cotton":{"f":0,"p":1,"m":1},
            "sugar":{"f":1,"p":0,"m":2},
            "pasture":{"f":2,"p":1,"m":0},
            "wheats":{"f":3,"p":0,"m":0},
            "game":{"f":2,"p":0,"m":0},
            "fur":{"f":1,"p":1,"m":1},
            "mushroom":{"f":1,"p":0,"m":0},
            "silk":{"f":0,"p":1,"m":2},
            "spices":{"f":1,"p":0,"m":2},
            "woods":{"f":0,"p":3,"m":0}, # Bonus in Naval and Defensive Warfare
            "wine":{"f":1,"p":0,"m":2},
            "coal":{"f":0,"p":2,"m":0},
            "iron":{"f":0,"p":3,"m":0}, # Very important in Warfare
            "gold":{"f":0,"p":0,"m":2},
            "gems":{"f":0,"p":0,"m":3},
            "silver":{"f":0,"p":0,"m":1},
            "copper":{"f":0,"p":2,"m":0}, # Substitute for iron
            "stone":{"f":0,"p":2,"m":0} # Bonus in Defensive Warfare
        }
        for t in self.terrain:
            self.values["f"] += terrain_dict[t]["f"]
            self.values["p"] += terrain_dict[t]["p"]
            self.values["m"] += terrain_dict[t]["m"]
        for p in self.ressources:
            self.values["f"] += ressource_dict[p]["f"]
            self.values["p"] += ressource_dict[p]["p"]
            self.values["m"] += ressource_dict[p]["m"]
            
    def calculate_growth(self):
        # growth = 0.05 ist Maximum bei 40 Food
        # Jedes Food darunter senkt Growth um 0.005
        food = self.values["f"]
        max_growth = 0.05 
        missing_food = float((self.pop*0.1) - food)*0.00125
        self.growth = max_growth - missing_food
        
        
    def make_city(self, models, interface):
        self.active = True
        new_culture = False
        if self.culture == None:
            self.culture = Culture()
            new_culture = True
        self.name = self.culture.generate_name(models, "t")
        while len(self.name) < 6 or len(self.name) > 16 or ' ' in self.name or '-' in self.name:
            self.name = self.culture.generate_name(models, "t")
        if new_culture:
            self.culture.name = self.name + "ian"
        self.leader = Character(models, self.culture, self)
        r = lambda: random.randint(0,255)
        self.color = '#%02X%02X%02X' % (r(),r(),r())
        for f in self.field.field_neighbor(5):
            if f.city is not None:
                if f.city.culture == None:
                    f.city.culture = self.culture
        self.change_color(interface)
        for f in self.field.field_neighbor(2):
            if f.owner is None:
                f.owner = self
                self.claim_field(f, interface)
        interface.inner_map.update_idletasks()
                
    def change_color(self, interface):
        xpos = (self.x*interface.field_size)+interface.field_size/2
        ypos = (self.y*interface.field_size)+interface.field_size/2
        c = interface.inner_map.find_closest(ypos, xpos)[0]
        interface.inner_map.itemconfig(c, fill=self.color)
        
        
    def claim_field(self, field, interface):
        xpos = (field.x*interface.field_size)+1
        ypos = (field.y*interface.field_size)+1
        c = interface.inner_map.find_closest(ypos, xpos)[0]
        interface.inner_map.itemconfig(c, outline=self.color)
        
        
    def getAttr(self):
        return {"name":self.name,"empire":self.empire, "county":self.county,
            "pop":self.pop}
