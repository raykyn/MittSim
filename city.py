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
        self.tech = 0
        self.simMap = simMap
        self.fields = simMap.fields
        self.field = field
        self.seed = random.randint(0, 9) # splits cities into ten groups
        self.x = x
        self.y = y
        self.resources = []
        self.values = {"f":0,"p":0,"m":0}
        self.growth = 0.0
        self.leader = None
        self.territory = [field] # Keeps all fields that are owned by this city
        self.pop = random.randint(1, 10)
            
        
    def detect_resources(self):
        self.resources = []
        for field in self.territory:
            if field.resource is not None:
                self.resources.append(field.resource)
            
                
    def calculate_values(self):
        # Dictionary for what terrain the city gets what
        # Three general resources:
        # - food (important for growth)
        # - production (important if war and technology)
        # - money (buying this and trading. Buying: Mercenaries for example)
        for field in self.territory:
            self.values["f"] += field.food
            self.values["p"] += field.production
            self.values["m"] += field.money
        if len(self.territory) == 1:
            for n in field.field_neighbor(1):
                self.values["f"] += n.food/2
                self.values["p"] += n.production/2
                self.values["m"] += n.money/2
        
            
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
        while len(self.name) < 6 or len(self.name) > 16 or ' ' in self.name or '-' in self.name or ')' in self.name:
            self.name = self.culture.generate_name(models, "t")
        if new_culture:
            self.culture.name = self.name + "ian"
        self.leader = Character(models, self.culture, self, 40)
        for f in self.field.field_neighbor(5):
            if f.city is not None:
                if f.city.culture == None:
                    f.city.culture = self.culture
                    #~ f.city.change_color(interface)
        if interface.mapmode != "t":
            self.change_color(interface)
        for f in self.field.field_neighbor(2):
            if f.owner is not None:
                if not f.owner.active:
                    f.owner = self
                    if interface.mapmode != "t":
                        self.claim_field(f, interface)
            else:
                f.owner = self
                if interface.mapmode != "t":
                    self.claim_field(f, interface)
        interface.inner_map.update_idletasks()
                
    def change_color(self, interface):
        #~ xpos = (self.x*interface.field_size)+interface.field_size/2
        #~ ypos = (self.y*interface.field_size)+interface.field_size/2
        #~ c = interface.game_window.find_closest(ypos, xpos)
        #~ if interface.mapmode == "p":
            #~ color = self.color
        #~ elif interface.mapmode == "c":
            #~ color = self.culture.color
        #~ interface.game_window.itemconfig(c, fill=color)
        #~ interface.game_window.update_idletasks()
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
        c = interface.inner_map.find_overlapping(ypos, xpos, ypos+(2*interface.field_size/10), xpos+(2*interface.field_size/10))
        for item in c:
            if interface.inner_map.gettags(item)[0] == "border":
                d = item
                break
        #~ c = interface.inner_map.find_closest(ypos, xpos)
        if interface.mapmode == "p":
            color = self.color
        elif interface.mapmode == "c":
            color = self.culture.color
        interface.inner_map.itemconfig(d, outline=color)
        
    def make_first_city(self, models):
        self.active = True
        r = lambda: random.randint(0,255)
        self.color = '#%02X%02X%02X' % (r(),r(),r())
        new_culture = False
        if self.culture == None:
            self.culture = Culture(self.color)
            new_culture = True
        self.name = self.culture.generate_name(models, "t")
        while len(self.name) < 6 or len(self.name) > 16 or ' ' in self.name or '-' in self.name or ')' in self.name:
            self.name = self.culture.generate_name(models, "t")
        if new_culture:
            self.culture.name = self.name + "ian"
        self.leader = Character(models, self.culture, self, 40)
        for f in self.field.field_neighbor(5):
            if f.city is not None:
                if f.city.culture == None:
                    f.city.culture = self.culture
        for f in self.field.field_neighbor(2):
            f.owner = self
        
        
    def getAttr(self):
        return {"name":self.name,"empire":self.empire, "county":self.county,
            "pop":self.pop}
