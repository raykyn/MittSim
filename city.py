#! /usr/bin/python3

import random
from culture import Culture
from characters import Character
from collections import Counter
from title import Title

class City():
    def __init__(self, simMap, field, x, y):
        self.name = "No Name Yet"
        self.empire = None
        self.county = "No Name Yet"
        self.culture = None
        self.culture_name = ""
        self.color = "purple"
        self.active = False
        self.tech = 0
        self.simMap = simMap
        self.fields = simMap.fields
        self.field = field
        self.seed = random.randint(0, 9) # splits cities into ten groups
        self.x = x
        self.y = y
        self.resources = []
        self.wealth = 0
        self.wpc = 0
        self.growth = 0.0
        self.leader = None
        self.title = None
        self.territory = [field] # Keeps all fields that are owned by this city
        self.chars = [] # Keep a list of all characters that live in this city
        
        self.pop = 0
            
        
    def detect_resources(self):
        self.resources = []
        for field in self.territory:
            if field.resource is not None:
                self.resources.append(field.resource)
            
                
    def calculate_values(self):
        # Only Wealth as an abstract value of the cities productivity, food and luxury resources
        self.wealth = 0
        for field in self.territory:
            self.wealth += field.wealth
        if self.pop > 0:
            self.wpc = self.wealth / self.pop
            # bonus for big population (ppl per field)
            # The maximum bonus it can give is 10% (if 160 ppl/field)
            ppf = self.pop/len(self.territory)
            bonus = 0.1 * ppf/160
            self.wealth = self.wealth + self.wealth*bonus
        
            
    def calculate_growth(self):
        # wealth per capita is the most important thing at the beginning
        # we assume that at the start of the game, all the cities have
        # a medium WpC (Wealth per Capita)
        # As we calculate the starting pop as 10* wealth, the medium
        # WpC would be 0.1
        # minimum WpC is 0.05
        # maximum (usable) WpC is 0.2 (everything above is not really needed)
        # let's assume medium growth is 0.0025
        wpc = self.wealth / self.pop # WpC
        max_growth = 0.005
        self.growth = max_growth - (0.0025 / (wpc * 10))
                
        
    def make_city(self, models, interface):
        self.active = True
        r = lambda: random.randint(0,255)
        self.color = '#%02X%02X%02X' % (r(),r(),r())
        new_culture = False
        if self.culture == None:
            self.culture = Culture(self.color)
            new_culture = True
        self.name = self.culture.generate_name(models, "t")
        while len(self.name) < 4 or len(self.name) > 10 or ' ' in self.name or '-' in self.name or ')' in self.name:
            self.name = self.culture.generate_name(models, "t")
        if new_culture:
            self.culture.name = self.name + "ian"
        self.leader = Character(models, self.culture, self, 40)
        self.chars.append(self.leader)
        for f in self.field.field_neighbor(10):
            if f.city is not None:
                if f.city.culture == None:
                    f.city.culture = self.culture
                    #~ f.city.change_color(interface)
        if interface.mapmode != "t":
            self.change_color(interface)
        if interface.mapmode != "t":
            self.claim_field(self.field, interface)
        for f in self.field.field_neighbor(1):
            if f.owner is not None:
                if not f.owner.active:
                    f.owner = self
                    self.territory.append(f)
                    if interface.mapmode != "t":
                        self.claim_field(f, interface)
            else:
                f.owner = self
                self.territory.append(f)
                if interface.mapmode != "t":
                    self.claim_field(f, interface)
        interface.inner_map.update_idletasks()
                
    def change_color(self, interface):
        size = interface.field_size
        if interface.mapmode == "p":
            color = self.color
        elif interface.mapmode == "c":
            color = self.culture.color
        interface.inner_map.create_rectangle((self.field.y*size)+(size/4), (self.field.x*size)+(size/4), ((self.field.y+1)*size)-(size/4), (self.field.x+1)*size-size/4, fill=color, tag=("city", self.field.fieldID))
        interface.inner_map.update_idletasks()
        
    def claim_field(self, field, interface):
        xpos = (field.x*interface.field_size)
        ypos = (field.y*interface.field_size)
        c = interface.inner_map.find_overlapping(ypos, xpos, ypos+(3*interface.field_size/10), xpos+(3*interface.field_size/10))
        for item in c:
            if interface.inner_map.gettags(item)[0] == "border":
                d = item
                break
        if not interface.show_terrain:
            if interface.mapmode == "p":
                color = self.color
            elif interface.mapmode == "c":
                color = self.culture.color
            else:
                color = self.color
            interface.inner_map.itemconfig(field.graphic, fill=color)
        if interface.mapmode == "p":
            color = self.color
        elif interface.mapmode == "c":
            color = self.culture.color
        else:
            color = self.color
        interface.inner_map.itemconfig(d, outline=color)
        interface.inner_map.update_idletasks()
        
    def make_first_city(self, models):
        self.active = True
        r = lambda: random.randint(0,255)
        self.color = '#%02X%02X%02X' % (r(),r(),r())
        new_culture = False
        self.food_limit = 750
        if self.culture == None:
            self.culture = Culture(self.color)
            new_culture = True
        self.name = self.culture.generate_name(models, "t")
        while len(self.name) < 6 or len(self.name) > 10 or ' ' in self.name or '-' in self.name or ')' in self.name:
            self.name = self.culture.generate_name(models, "t")
        if new_culture:
            self.culture.name = self.name + "ian"
        self.leader = Character(models, self.culture, self, 40)
        ### CREATE TITLE
        self.title = Title(self.name, None, [], [self], 1)
        self.leader.titles.append(self.title)
        self.leader.refresh_fullname()
        self.chars.append(self.leader)
        for f in self.field.field_neighbor(10):
            if f.city is not None:
                if f.city.culture == None:
                    f.city.culture = self.culture
        for f in self.field.field_neighbor(1):
            if f.owner is not None:
                if not f.owner.active:
                    f.owner = self
                    self.territory.append(f)
            else:
                f.owner = self
                self.territory.append(f)
            
        self.calculate_values()
        self.detect_resources()
        self.pop = self.wealth*10 + random.randint(-100, 100)
        self.wpc = self.wealth/self.pop
                
    
    def grow_territory(self, interface):
        field_values = Counter()
        for t in self.territory:
            for f in t.field_neighbor(1):
                if f.fieldID not in field_values.keys():
                    if f.owner is None or not f.owner.active:
                        field_values[f.fieldID] = f.production + f.food + f.money
                        if f.resource in ["Horses", "Iron", "Copper", "Woods", "Stone"]:
                            field_values[f.fieldID] += 5 # prefer strategic resources
        # get the highest Counter-Entry. 
        # Check if at least two own fields are next to the new one (also diagonally)
        # this shall prevent of just taking all river fields
        print(field_values)
        for f in field_values:
            field = self.simMap.fieldIDs[f]
            neighboring = 0
            for n in field.get_dia():
                if n.owner == self:
                    neighboring += 1
            if neighboring > 1:
                field.owner = self
                self.territory.append(field)
                self.claim_field(field, interface)
                break
        self.food_limit = len(self.territory)*150
        
        
    def getAttr(self):
        return {"name":self.name,"empire":self.empire, "county":self.county,
            "pop":self.pop}
