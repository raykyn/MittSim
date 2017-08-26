#! /usr/bin/python3

import random
from city import City

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
        self.food = 0
        self.production = 0
        self.money = 0
        
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
        simMap.cities.append(self.city)
        self.pop = city.pop
        
    
    def set_values(self):
        terrain_dict = {
            "Coast":{"f":2.5,"p":0,"m":0},
            "Grassland":{"f":2,"p":1,"m":0},
            "Woodland":{"f":1.5,"p":1.5,"m":0},
            "Low Mountains":{"f":1,"p":2,"m":0},
            "High Mountains":{"f":0.5,"p":0,"m":0},
            "Wetlands":{"f":3,"p":0,"m":0},
            "Swamps":{"f":1,"p":0,"m":0},
            "Steppe":{"f":1.5,"p":1.5,"m":0},
            "Desert":{"f":0,"p":0.5,"m":0},
            "Ocean":{"f":1.5,"p":0,"m":0}
        }
        resource_dict = {
            "Fish":{"f":2,"p":0,"m":0},
            "Clam":{"f":1,"p":0,"m":1},
            "Whale":{"f":1,"p":1,"m":1},
            "Horses":{"f":1,"p":2,"m":0}, # Bonus in Warfare
            "Ivory":{"f":0,"p":2,"m":1}, # Bonus in Warfare
            "Fruits":{"f":2,"p":0,"m":0},
            "Dyes":{"f":0,"p":1,"m":1},
            "Sugar":{"f":1,"p":0,"m":2},
            "Pasture":{"f":2,"p":1,"m":0},
            "Wheat":{"f":3,"p":0,"m":0},
            "Corn":{"f":2,"p":0,"m":0},
            "Rice":{"f":2,"p":0,"m":0},
            "Game":{"f":2,"p":0,"m":0},
            "Furs":{"f":1,"p":1,"m":1},
            "Silk":{"f":0,"p":1,"m":2},
            "Spices":{"f":1,"p":0,"m":2},
            "Woods":{"f":0,"p":3,"m":0}, # Bonus in Naval and Defensive Warfare
            "Wine":{"f":1,"p":0,"m":2},
            "Iron":{"f":0,"p":3,"m":0}, # Very important in Warfare
            "Gold":{"f":0,"p":0,"m":2},
            "Gems":{"f":0,"p":0,"m":3},
            "Silver":{"f":0,"p":0,"m":1},
            "Copper":{"f":0,"p":2,"m":0}, # Substitute for iron
            "Stone":{"f":0,"p":2,"m":0}, # Bonus in Defensive Warfare
            "Marble":{"f":0,"p":1,"m":2} # Bonus in Defensive Warfare
        }
        self.food += terrain_dict[self.terrain]["f"]
        self.production += terrain_dict[self.terrain]["p"]
        self.money += terrain_dict[self.terrain]["m"]
        if self.resource is not None:
            self.food += resource_dict[self.resource]["f"]
            self.production += resource_dict[self.resource]["p"]
            self.money += resource_dict[self.resource]["m"]
