#! /usr/bin/python3

#By Ismail Prada

import random
from collections import Counter
from city import City
from culture import start_Cultures
from field import *
from interface import Application

class SimMap(object):
    
    def __init__(self, width, height):
        self.reach_limit = 15
        self.terrain_change_rate = 6
        self.height = height
        self.width = width
        self.sealevel = 75
        self.h_mountains = 190
        self.l_mountains = 170
        self.hills = 150
        self.midlands = 120
        self.fields = [["O" for x in range(self.width)] for y in range(self.height)] 
        self.cities = []
        self.inactive_cities = []
        # generate culture data
        self.culture_models = start_Cultures()
        self.culture_models.load_all()
        self.game_map = None
        self.max_ticks = 160 # would be 25 wealth
            
            
    def fillfield(self):
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
                self._createResources(self.fieldIDs[fieldID])
                self.fieldIDs[fieldID].set_values()
                
        # create potential cities
        starting_tick_dict = Counter()
        # loop through all fields
        for fieldID in shuffled_IDs:
            field = self.fieldIDs[fieldID]
            # only fields that are not oceans neither high mountains
            if field.terrain not in ["Ocean", "Coast", "High Mountains"]:
                # calc wealth of this field + all the other fields around/2
                fields = field.field_neighbor(1)
                fields.append(field) # append itself a second time so it counts double
                sum_wealth = 0
                for f in fields:
                    sum_wealth += f.wealth
                # based on that, calc a starting tick value
                # Really good city: e.g. 28
                # Really bad city: e.g. 5
                # Let's take 40 as best
                # And 6 as worst
                if sum_wealth > 20:
                    starting_tick_dict[field] = int(4000/sum_wealth)
        
        for field, start in reversed(starting_tick_dict.most_common()):
            #~ print("Working field", field, start)
            # check that no neighboring field has already a city
            nei = field.get_dia()
            nei_c = False
            for f in nei:
                if f.city is not None:
                    nei_c = True
                    break
            if not nei_c:
                #~ print("Clear!")
                self._createCity(field)
                city = field.city
                #~ print("City created", city)
                if start < self.max_ticks:
                    self.cities.append(city)
                    #~ print("City appended active!", city)
                else:
                    self.inactive_cities.append(city)
                    #~ print("City appended inactive!", city)
            #~ else:
                #~ print("Not clear!")
                    
        # Now loop through the cities and make them active
        print(len(self.cities))
        for n, c in enumerate(self.cities):
            if n % 25 == 0:
                print("Created {} cities".format(n))
            c.make_first_city(self.culture_models)
                
        
    def _createResources(self, field):
        """
        Each terrain type offers an own range of choice, as well as a 
        base chance to generate anything
        Btw, Woods mean "Wood that is very good quality and thus gives
        bonus in warfare"
        """
        if field.terrain == "Ocean":
            chance = 34 # 1 in 3 fields contain resources
            resources = ["Whale"]*4 + ["Clam"]*2 + ["Fish"]*8
        elif field.terrain == "Coast":
            chance = 34 # 1 in 3 fields contain resources
            resources = ["Whale"]*1 + ["Clam"]*2 + ["Fish"]*16
        elif field.terrain == "High Mountains":
            chance = 10
            resources = ["Iron"]*5 + ["Stone"]*10
        elif field.terrain == "Low Mountains":
            chance = 34
            resources = (["Copper"]*5 + ["Iron"]*3 + ["Marble"]*2 + ["Stone"]*5
                + ["Gems"]*1 + ["Gold"]*1 + ["Silver"]*2)
        elif field.terrain == "Wetlands":
            chance = 67
            resources = ["Spices"]*1 + ["Sugar"]*1 + ["Wheat"]*3 + ["Corn"]*3 + ["Rice"]*3
        elif field.terrain == "Swamps":
            chance = 5
            resources = ["Rice"]
        elif field.terrain == "Desert":
            chance = 10
            resources = ["Copper"]*5 + ["Marble"]*3 + ["Gems"]*1
        elif field.terrain == "Steppe":
            chance = 34
            resources = (["Corn"]*3 + ["Copper"]*1 + ["Horses"]*5 + ["Furs"]*3
                + ["Ivory"]*1 + ["Pasture"]*5)
        elif field.terrain == "Grassland":
            chance = 34
            resources = ["Horses"]*2 + ["Corn"]*5 + ["Wheat"]*5 + ["Pasture"]*3
        elif field.terrain == "Woodland":
            chance = 34
            resources = (["Dyes"]*1 + ["Furs"]*3 + ["Spices"]*1 + ["Sugar"]*1
                + ["Fruits"]*5 + ["Game"]*5 + ["Woods"]*5)
        if field.hill and field.terrain != "High Mountains" and field.terrain != "Low Mountains":
            resources.extend(["Copper"]*10 + ["Iron"]*5 + ["Marble"]*1 + ["Stone"]*3
                + ["Gems"]*1 + ["Gold"]*1 + ["Silver"]*1 + ["Wine"]*5 + ["Pasture"]*3)
        r = random.randint(0, 99)
        if r < chance:
            field.resource = random.choice(resources)   
        
    
    def _set_terrain(self, field):
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
        if field.exact_height > self.hills:
            field.hill = True
        if field.exact_height < self.sealevel:
            landborder = False
            for n in field.get_dia():
                if n.exact_height >= self.sealevel:
                    landborder = True
                    break
            if landborder:
                field.terrain = "Coast"
                return None
            else:
                field.terrain = "Ocean"
                return None
        elif field.exact_height > self.h_mountains:
            field.terrain = "High Mountains"
            return None
        elif field.exact_height > self.l_mountains:
            field.terrain = "Low Mountains"
            return None
        if len(field.river) == 0:
            terrains = ["Desert"]*2 + ["Steppe"]*18 + ["Grassland"]*30 + ["Woodland"]*50
        elif len(field.river) > 0 and not field.hill:
            terrains = ["Wetlands"]*50 + ["Swamps"]*5 + ["Grassland"]*30 + ["Woodland"]*15
            for f in field.field_neighbor(1):
                if f.exact_height < self.sealevel:
                    terrains = ["Swamps"]*10 + ["Wetlands"]*90
                    break
        elif len(field.river) > 0 and field.hill:
            terrains = ["Wetlands"]*10 + ["Swamps"]*5 + ["Grassland"]*55 + ["Woodland"]*30
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
                if n.humidity is not None:
                    total += n.humidity
                    found_valids += 1
            true_change_rate = reach*self.terrain_change_rate
            reach += 1 # search further
        if found_valids == 0:
            final = random.randint(0,99)
        else:
            mean = (total/found_valids)
            final = mean + random.uniform(-true_change_rate, true_change_rate)
            if final > 99:
                final = 99
            elif final < 0:
                final = 0
        field.humidity = float(final)
        final = int(final) # round down
        field.terrain = terrains[final]
    
            
    def _create_rivers(self):
        #~ num_of_rivers = round((self.width*self.height)/150)
        num_of_rivers = round(len(self.mountain_fields)/20)
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
                col = row[m]
                col.height = random.randint(0, 49)
                col.exact_height = random.randint(0, 49)
                self.ocean_fields.append(col)
                col = row[-m+1]
                col.height = random.randint(0, 49)
                col.exact_height = random.randint(0, 49)
                self.ocean_fields.append(col)
                
                
    def _createCity(self, field):
        """
        A village is created on every field at the start.
        """
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
        elif field.height >= self.hills:
            self.mountain_fields.append(field)
                
    def create_tkinter(self):
        self.interface = Application(self, self.fields)
        
    def _leave(self):
        exit()
                    
        
def main():
    newmap = SimMap(90,45) # 180 / 90 Standard
    newmap.fillfield()
    newmap.create_tkinter()

if __name__ == "__main__":
    main()
