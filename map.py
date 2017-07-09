#! /usr/bin/python3

#By Ismail Prada

import random
from collections import Counter
from city import City
from culture import start_Cultures
from interface import Application
from tkinter import *

class SimMap(object):
    
    def __init__(self, width, height):
        self.reach_limit = 15
        self.terrain_change_rate = 6
        self.height = height
        self.width = width
        self.sealevel = 75
        self.h_mountains = 190
        self.l_mountains = 170
        self.midlands = 120
        self.fields = [["O" for x in range(self.width)] for y in range(self.height)] 
        self.cities = []
        # generate culture data
        self.culture_models = start_Cultures()
        self.culture_models.load_all()
        self.game_map = None
            
            
    def fillfield(self):
        #~ self.terrain_chances = Counter({
            #~ 0:self.ocean_chance,
            #~ 1:self.coastal_chance,
            #~ 2:self.lowlands_chance,
            #~ 3:self.woodlands_chance,
            #~ 4:self.highlands_chance,
            #~ 5:self.lower_m_chance,
            #~ 6:self.higher_m_chance
        #~ })
        #~ self.sorted_terrain_chances = sorted(list(self.terrain_chances.elements()))
        self.fieldIDs = {}
        self.fieldIDcounter = 1
        for x in range(self.height):
            for y in range(self.width):
                newField = Field(self, self.fieldIDcounter, x, y)
                self.fieldIDs[newField.fieldID] = newField
                self.fields[x][y] = newField
                self.fieldIDcounter += 1
        
        # fill the "ocean" fields (10th of the map all around the corner)
        self._create_ocean()
        self.mountain_fields = []
        
        shuffled_IDs = list(range(1, self.fieldIDcounter))
        random.shuffle(shuffled_IDs)
        for fieldID in shuffled_IDs:
            if self.fieldIDs[fieldID].height is None:
                self.setlevel(self.fieldIDs[fieldID])
                
        self._create_rivers()
        
        shuffled_IDs = list(range(1, self.fieldIDcounter))
        random.shuffle(shuffled_IDs)
        for fieldID in shuffled_IDs:
            if self.fieldIDs[fieldID].terrain is None:
                self._set_terrain(self.fieldIDs[fieldID])
        
            #~ self._createCity(self.fieldIDs[fieldID])
            #~ self._createRessources(self.fieldIDs[fieldID])
        #~ for c in self.cities:
            #~ c.detect_ressources()
            #~ c.calculate_values()
            #~ c.calculate_growth()
        
    
    def _set_terrain(self, f):
        """
        Terrain Types:
        - High Mountains always count as Desert
        - Lower Mountains always count as Steppe
        - Grasslands (Steppe/Savanna/Tundra)
        - Woodlands (or Jungle, in case of southern region or Taiga for northern)
        - Deserts (Cold, hot, arid)
        - Swamps and Wetlands
        Similar to setlevel. This method chooses a random field. 
        Factors to decide Terrain Type:
        - Height (Only for mountains, swamps and wetlands)
        - Position (Northern, middle, southern region)
        - Neighbors (Same algorithm as height creation?)
        - Rivers and Lakes (Wetland instead of desert if river)
        """
        if f.height >= self.h_mountains:
            f.terrain = "High Mountains"
        elif f.height >= self.l_mountains:
            f.terrain = "Low Mountains"
        elif f.height >= self.sealevel:
            chance_list = ["Grassland"] * 5 + ["Woodland"] * 5 + ["Desert"] * 1
            if len(f.river) > 0:
                chance_list.extend(["Wetlands"]*10 + ["Swamps"]*2)
                chance_list.remove("Desert")
            for n in f.field_neighbor(1):
                if len(n.river) > 0:
                    chance_list.extend(["Wetlands"]*2 + ["Swamps"]*1)
                if n.terrain is not None and n.terrain != "Wetlands" and n.terrain != "Swamps":
                    chance_list.extend([n.terrain]*10)
            f.terrain = random.choice(chance_list)
        else:
            f.terrain = "Ocean"
                    
    
            
    def _create_rivers(self):
        #num_of_rivers = round((self.width*self.height)/200)
        num_of_rivers = 80
        for i in range(num_of_rivers):
            success = False
            while not success:
                curr = random.choice(self.mountain_fields)
                last = None
                path = [curr]
                dead_ends = []
                correct_start = True
                success = True
                for n in curr.field_neighbor(1):
                    if len(n.river) > 0:
                        correct_start = False
                        break
                if not correct_start:
                    success = False
                    continue
                while curr.height >= self.sealevel and len(curr.river) == 0:
                    possibles = []
                    #print("curr = {}".format(curr.fieldID))
                    for n in curr.field_neighbor(1):
                        #print(n.fieldID)
                        lake = False
                        if last is None and n.exact_height >= curr.exact_height:
                            #print("STARTERROR")
                            continue
                        elif n.exact_height < curr.exact_height:
                            pass
                        elif n.exact_height < last.exact_height:
                            lake = True
                        else:
                            continue
                        if n in path or n in dead_ends:
                            continue
                        else:
                            pass
                        good = True
                        #~ for i in n.field_neighbor(1):
                            #~ if i is curr:
                                #~ continue
                            #~ elif i in path:
                                #~ good = False
                                #~ break
                        if good:
                            #if lake:
                                #print("LAKE APPENDED")
                            #else:
                                #print("NORMAL APPENDED")
                            possibles.append((n, lake)) # Woohoo!
                    if len(possibles) > 0:
                        #print("APPENDED FOUND")
                        p_fields_no_lake = [p[0] for p in possibles if not p[1]]
                        p_fields_w_lake = [p[0] for p in possibles if p[1]]
                        if len(p_fields_no_lake) > 0:
                            #print("NORMAL FOUND")
                            next_f = random.choice(p_fields_no_lake)
                            curr.lake = False
                        else:
                            #print("LAKE FOUND")
                            next_f = min(p_fields_w_lake, key=lambda x: x.exact_height)
                            dead_ends.extend([p for p in p_fields_w_lake if p != next_f])
                            curr.lake = True
                        path.append(next_f)
                        last = curr
                        curr = next_f
                    else:
                        #print("NO APPENDED FOUND")
                        curr.lake = False
                        if path.index(curr)-2 >= 0:
                            last = path[path.index(curr)-2]
                        else:
                            last = None
                        if path.index(curr)-1 >= 0:
                            old = curr
                            curr = path[path.index(curr)-1]
                        else:
                            #print("ABORT")
                            success = False
                            break
                        path.remove(old)
                        dead_ends.append(old)
                
                if success:
                    #print("SUCCESS")
                    for i, f in enumerate(path):
                        if i == 0:
                            f.river.append((f.x, f.y, path[i+1].x, path[i+1].y))
                        elif i == len(path)-1:
                            f.river.append((path[i-1].x, path[i-1].y, f.x, f.y))
                        else:
                            f.river.append((path[i-1].x, path[i-1].y, path[i+1].x, path[i+1].y))
                
            
    def _create_ocean(self):
        self.ocean_fields = []
        
        distance = round(self.width/60)
        for n in range(distance):
            to_oceanize = self.fields[n]
            for col in to_oceanize:
                col.height = random.randint(0, 49)
                col.exact_height = random.randint(0, 49)
                self.ocean_fields.append(col)
            to_oceanize = self.fields[-n+1]
            for col in to_oceanize:
                col.height = random.randint(0, 49)
                col.exact_height = random.randint(0, 49)
                self.ocean_fields.append(col)
        
        for row in self.fields:
            for m in range(distance):
                col = row[n]
                col.height = random.randint(0, 49)
                col.exact_height = random.randint(0, 49)
                self.ocean_fields.append(col)
                col = row[-n+1]
                col.height = random.randint(0, 49)
                col.exact_height = random.randint(0, 49)
                self.ocean_fields.append(col)
                
                
    def _createCity(self, field):
        # check if no other city exists there yet.
        for nx, ny in field.dia_neighbors:
            try:
                if self.fields[nx][ny].city is not None:
                    return None
            except:
                pass
        city_gen = self.city_generation_chance*100
        m = random.randint(1,100)
        if (field.height == 2 or field.height == 3) and m <= city_gen:
            field.createCity(self, field.x, field.y)
        elif field.height == 4 and m <= city_gen*0.65:
            field.createCity(self, field.x, field.y)
        elif field.height == 5 and m <= city_gen*0.3:
            field.createCity(self, field.x, field.y)
        elif field.height == 6 and m <= city_gen*0.15:
            field.createCity(self, field.x, field.y)
        
        
    def setlevel(self, field):
        total = 0
        found_valids = 0
        reach = 1
        while found_valids == 0 and reach <= self.reach_limit:
            neighbors = field.field_neighbor(reach)
            try:
                neighbors = neighbors.remove(self)
            except:
                pass
            for n in neighbors:
                if n.exact_height is not None:
                    total += n.exact_height
                    found_valids += 1
            true_change_rate = reach*self.terrain_change_rate
            reach += 1 # search further
        if found_valids == 0:
            final = random.randint(self.sealevel-10,189)
        else:
            mean = (total/found_valids)
            if mean > 160:
                final = mean + random.uniform(-true_change_rate*1.5, true_change_rate)
            elif mean < 40:
                final = mean + random.uniform(-true_change_rate, true_change_rate*1.5)
            else:
                final = mean + random.uniform(-true_change_rate, true_change_rate)
            if final > 199:
                final = 199
            elif final < 0:
                final = 0
        field.exact_height = float(final)
        final = int(final) # round down
        field.height = final
        if field.height < self.sealevel:
            self.ocean_fields.append(field)
        elif field.height > 169:
            self.mountain_fields.append(field)
                
    def create_tkinter(self):
        self.interface = Application(self, self.fields)
        
        
    def _draw_city(self, field, city, width, height):
        field.create_rectangle(width/4, height/4, width*0.75, height*0.75, fill=city.color, tag="city")
        
    def _onFrameConfigure(self, canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    def _field_info(self, field):
        self._info_ID.set(str(field.fieldID))
        self._info_height.set(str(field.height))
        self._info_ress.set(str(field.ressource))
        if field.owner is not None:
            self._city_name.set(field.owner.name)
            city_atts = field.owner.getAttr()
            for attr, value in self.city_info.items():
                if attr == "pop":
                    value.set(round(city_atts[attr]))
                else:
                    value.set(city_atts[attr])
            self._city_ressources.set('\n'.join(field.owner.ressources))
            self._food.set(field.owner.values["f"])
            self._production.set(field.owner.values["p"])
            self._money.set(field.owner.values["m"])
            if field.owner.culture is not None:
                self._show_culture.set(field.owner.culture.name)
            else:
                self._show_culture.set("")
            if field.owner.leader is not None:
                self._show_leader.set(field.owner.leader.fullname)
            else:
                self._show_leader.set("")
        else:
            self._city_name.set("")
            for attr, value in self.city_info.items():
                value.set("")
            self._city_ressources.set("")
            self._food.set("")
            self._production.set("")
            self._money.set("")
            self._show_leader.set("")
            self._show_culture.set("")
        self.root.update()
        
    #~ def _on_mousewheel(self, canvas):
        #~ canvas.yview_scroll(-1*(event.delta/120), "units")
        
    #~ def show_field(self):
        #~ pass
        
    def _leave(self):
        exit()
                        
class Field(object):
    
    def __init__(self, simMap, id, x, y):
        self.fieldID = id
        self.x = x
        self.y = y
        #Höhe: 0: Sealevel 1: Coastal 2: Lowlands 3: Flatlands 4: Highlands 
        #5: Low mountains 6: High Mountains
        self.height = None
        self.exact_height = None
        self.city = None
        self._neighbors()
        self.ressource = None
        self.simMap = simMap
        self.owner = None # City
        self.river = []
        self.lake = False
        self.terrain = None
        
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
        #print = """%s""" % (sign)
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
            
        
    def color(self):
        # PLACEHOLDERS
        # THIS WILL INSTEAD REFER TO THE TERRAIN TYPE
        if self.height < self.simMap.sealevel-20:
            clr = "navy"
        elif self.height < self.simMap.sealevel:
            clr = "blue"
        elif self.height < 120:
            clr = "PaleGreen2"
        elif self.height < 160:
            clr = "green"
        elif self.height < 180:
            clr = "orange"
        elif self.height < 190:
            clr = "brown"
        else:
            clr = "gray60"
        return clr
        
    def createCity(self, simMap, x, y):
        city = City(simMap, self, x, y)
        self.city = city
        self.owner = self.city
        simMap.cities.append(self.city)

        
def main():
    newmap = SimMap(180,90)
    newmap.fillfield()
    newmap.create_tkinter()

if __name__ == "__main__":
    main()
