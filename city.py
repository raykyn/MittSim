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
        self.pop = random.randint(150, 450)
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
        if self.field.ressource is not None:
            self.ressources.append(self.field.ressource)
        self.terrain.append(self.field.height)
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
            1:{"f":2.5,"p":0,"m":1.5},
            2:{"f":2,"p":1,"m":1},
            3:{"f":2,"p":1,"m":1},
            4:{"f":1.5,"p":1.5,"m":1},
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
        self.values = {"f":0,"p":0,"m":0}
        for t in self.terrain:
            self.values["f"] += terrain_dict[t]["f"]
            self.values["p"] += terrain_dict[t]["p"]
            self.values["m"] += terrain_dict[t]["m"]
        for p in self.ressources:
            self.values["f"] += ressource_dict[p]["f"]
            self.values["p"] += ressource_dict[p]["p"]
            self.values["m"] += ressource_dict[p]["m"]
            
    def calculate_growth(self):
        # We assume a maximum population growth a little higher then 
        # the high medieval ages (doubled pop in 300 yrs).
        # In 10 Ticks (Months), the population grows by 0.5% at max
        # With this model, most cities will reach active status around
        # Tick 140 (around 12 yrs), depending on food (around 20 food is
        # needed to get max_growth wiht 500 Pop) 1000 pop is the ceiling
        # for a city with 20 Food.
        food = self.values["f"]
        max_growth = 0.005 
        # Each person consumes 0.02 Food units
        # The more food is accessible per Person, the higher the max
        # growth is.
        # if food == pop*0.02 => growth = 0
        # elif food == pop*0.02 => growth = 0.005
        # Check first if enough food to sustain pop
        # (This can lead to some cities never becoming real cities bc of
        # missing food if other cities grab their fields)
        nec_food =  self.pop*0.02
        remaining_food = food-nec_food
        if remaining_food > nec_food:
            remaining_food = nec_food # Excess food can and should be 
            # traded off. Villages in the mountains will try to get food,
            # While villages in the plains will try to get metals and stone.
            # If a city lacks food to grow further, it will also more likely
            # go to war to steal food or conquer villages with excess food.
        self.growth = max_growth * (remaining_food/nec_food)
        
        
    def make_city(self, models, interface):
        self.active = True
        r = lambda: random.randint(0,255)
        self.color = '#%02X%02X%02X' % (r(),r(),r())
        new_culture = False
        if self.culture == None:
            self.culture = Culture(self.color)
            new_culture = True
        self.name = self.culture.generate_name(models, "t")
        while len(self.name) < 6 or len(self.name) > 16 or ' ' in self.name or '-' in self.name:
            self.name = self.culture.generate_name(models, "t")
        if new_culture:
            self.culture.name = self.name + "ian"
        self.leader = Character(models, self.culture, self, 40)
        for f in self.field.field_neighbor(5):
            if f.city is not None:
                if f.city.culture == None:
                    f.city.culture = self.culture
        if interface.mapmode != "t":
            self.change_color(interface)
        for f in self.field.field_neighbor(2):
            if f.owner is None:
                f.owner = self
                if interface.mapmode != "t":
                    self.claim_field(f, interface)
        interface.inner_map.update_idletasks()
                
    def change_color(self, interface):
        xpos = (self.x*interface.field_size)+interface.field_size/2
        ypos = (self.y*interface.field_size)+interface.field_size/2
        c = interface.inner_map.find_closest(ypos, xpos)[0]
        if interface.mapmode == "p":
            color = self.color
        elif interface.mapmode == "c":
            color = self.culture.color
        interface.inner_map.itemconfig(c, fill=color)
        interface.inner_map.update_idletasks()
        
        
    def claim_field(self, field, interface):
        xpos = (field.x*interface.field_size)+1
        ypos = (field.y*interface.field_size)+1
        c = interface.inner_map.find_closest(ypos, xpos)[0]
        if interface.mapmode == "p":
            color = self.color
        elif interface.mapmode == "c":
            color = self.culture.color
        interface.inner_map.itemconfig(c, outline=color)
        
        
    def getAttr(self):
        return {"name":self.name,"empire":self.empire, "county":self.county,
            "pop":self.pop}
