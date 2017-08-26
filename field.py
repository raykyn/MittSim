#! /usr/bin/python3

import random
from city import City

terrain_dict = {
        "Coast":4,
        "Grassland":4,
        "Woodland":3,
        "Low Mountains":3,
        "High Mountains":2,
        "Wetlands":5, #Highest
        "Swamps":2,
        "Steppe":3,
        "Desert":1, #Lowest
        "Ocean":1
        }
resource_dict = {
        "Fish":3,
        "Clam":2,
        "Whale":2,
        "Horses":2, # Bonus in Warfare
        "Ivory":2, # Bonus in Warfare
        "Fruits":2,
        "Dyes":2,
        "Sugar":2,
        "Pasture":2,
        "Wheat":3,
        "Corn":2,
        "Rice":2,
        "Game":2,
        "Furs":2,
        "Silk":2,
        "Spices":2,
        "Woods":2, # Bonus in Naval and Defensive Warfare
        "Wine":2,
        "Iron":2, # Very important in Warfare
        "Gold":3,
        "Gems":3,
        "Silver":2,
        "Copper":1, # Substitute for iron
        "Stone":2, # Bonus in Defensive Warfare
        "Marble":2 # Bonus in Defensive Warfare
        }


class Field(object):
    
    def __init__(self, simMap, id, x, y):
        self.fieldID = id
        self.x = x
        self.y = y
        self.height = None
        self.exact_height = None
        self.city = None
        self._neighbors()
        self.resource = None
        self.simMap = simMap
        self.owner = None # City
        self.river = []
        self.lake = False
        self.terrain = None
        self.humidity = None
        self.hill = False
        self.graphic = None
        self.seed = random.randint(0,99)
        self.wealth = 0
        
        
    def __str__(self):
        if self.height == 0:
            sign = "O"
        elif self.height == 1:
            sign = "o"
        elif self.height == 2:
            sign = "_"
        elif self.height == 3:
            sign = "-"
        elif self.height == 4:
            sign = "~"
        elif self.height == 5:
            sign = "+"
        else:
            sign = "^"
        return str(self.fieldID)
        
    def __repr__(self):
        return str(self.fieldID)
        
    def _neighbors(self):
        """This method is still in use on one field, but is subject to 
        change as soon as I've got a better method of only getting
        the direct neighbors"""
        self.neighbors = []
        self.upN = (self.x,self.y-1)
        self.neighbors.append(self.upN)
        self.rightN = (self.x+1, self.y)
        self.neighbors.append(self.rightN)
        self.downN = (self.x, self.y+1)
        self.neighbors.append(self.downN)
        self.leftN = (self.x-1, self.y)
        self.neighbors.append(self.leftN)
        self.dia_neighbors = []
        self.upleftN = (self.x-1,self.y-1)
        self.dia_neighbors.append(self.upleftN)
        self.uprightN = (self.x+1,self.y-1)
        self.dia_neighbors.append(self.uprightN)
        self.botleftN = (self.x-1,self.y+1)
        self.dia_neighbors.append(self.botleftN)
        self.botrightN = (self.x+1, self.y+1)
        self.dia_neighbors.append(self.botrightN)
        self.dia_neighbors.extend(self.neighbors)
        
    def get_dia(self):
        dia = []
        positions = [
            (-1,-1),
            (-1,0),
            (0,-1),
            (1,0),
            (1,1),
            (0,1),
            (1,-1),
            (-1,1)
        ]
        for x, y in positions:
            xpos = self.x+x
            ypos = self.y+y
            if xpos >= 0 and ypos >= 0 and xpos < self.simMap.height and ypos < self.simMap.width:
                dia.append(self.simMap.fields[xpos][ypos])
        return dia
        
    def field_neighbor(self, reach):
        field_neighbors = []
        fields = self.simMap.fields
        all_coord = []
        for n in range(1, reach+1): # n is current distance
            combinations = []
            # generate possible coordinates
            for m in range(0,n+1):
                k = n-m
                combinations.append((k, m))
                combinations.append((-k, m))
                combinations.append((k, -m))
                combinations.append((-k, -m))
            all_coord.extend(combinations)
        for x, y in set(all_coord):
            xpos = self.x+x
            ypos = self.y+y
            if xpos >= 0 and ypos >= 0 and xpos < self.simMap.height and ypos < self.simMap.width:
                field_neighbors.append(fields[xpos][ypos])
        return field_neighbors

        
    def createCity(self, simMap, x, y):
        city = City(simMap, self, x, y)
        self.city = city
        self.owner = city
        self.pop = city.pop
        
    
    def set_values(self):
        """Assign wealth values to terrain and ressources"""
        self.wealth += terrain_dict[self.terrain]
        if self.resource is not None:
            self.wealth += resource_dict[self.resource]
