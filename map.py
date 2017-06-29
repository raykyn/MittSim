#! /usr/bin/python3

#By Ismail Prada

import random
from city import City
from culture import start_Cultures
from tkinter import *

class SimMap(object):
    
    def __init__(self, width, height):
        self.reach_limit = 8
        self.terrain_change_rate = 0.1
        self.height = height
        self.width = width
        self.fields = [["O" for x in range(self.width)] for y in range(self.height)] 
        self._job = None
        self.ressourceList()
        self.cities = []
        # generate culture data
        self.culture_models = start_Cultures()
        self.game_map = None

    def printfield(self):
        for x in range(len(self.fields)):
            for y in range(len(self.fields[x])):
                print(self.fields[x][y], end=' ')
            print()
            
            
    def fillfield(self):
        self.fieldIDs = {}
        self.fieldIDcounter = 1
        for x in range(self.height):
            for y in range(self.width):
                newField = Field(self, self.fieldIDcounter, x, y)
                self.fieldIDs[newField.fieldID] = newField
                self.fields[x][y] = newField
                self.fieldIDcounter += 1
        
        shuffled_IDs = list(range(1, self.fieldIDcounter))
        random.shuffle(shuffled_IDs)
        for fieldID in shuffled_IDs:
            self.setlevel(self.fieldIDs[fieldID])
            self._createCity(self.fieldIDs[fieldID])
            self._createRessources(self.fieldIDs[fieldID])
        for c in self.cities:
            c.detect_ressources()
            c.calculate_values()
            c.calculate_growth()
                
                
    def _createCity(self, field):
        # check if no other city exists there yet.
        for nx, ny in field.dia_neighbors:
            try:
                if self.fields[nx][ny].city is not None:
                    return None
            except:
                pass
        m = random.randint(1,100)
        if (field.height == 2 or field.height == 3) and m < 16:
            field.createCity(self, field.x, field.y)
        elif field.height == 4 and m < 10:
            field.createCity(self, field.x, field.y)
        elif field.height == 5 and m < 6:
            field.createCity(self, field.x, field.y)
        elif field.height == 6 and m < 3:
            field.createCity(self, field.x, field.y)
            
    def ressourceList(self):
        sea_ress = {
            "fishes":10,
            "whales":4,
            "pearls":4,
            "crabs":6
        }
        self.sea_ress = []
        for key, value in sea_ress.items():
            for i in range(0, value):
                self.sea_ress.append(key)
        coast_ress = {
            "fishes":13,
            "pearls":4,
            "crabs":7
        }
        self.coast_ress = []
        for key, value in coast_ress.items():
            for i in range(0, value):
                self.coast_ress.append(key)
        low_ress = {
            "horses":4,
            "fruits":4,
            "cotton":2,
            "sugar":2,
            "pasture":6,
            "wheats":6
        }
        self.low_ress = []
        for key, value in low_ress.items():
            for i in range(0, value):
                self.low_ress.append(key)
        wood_ress = {
            "game":4,
            "fur":4,
            "mushroom":1,
            "silk":1,
            "spices":1,
            "fruits":3,
            "pasture":3,
            "wheats":3,
            "woods":5
        }
        self.wood_ress = []
        for key, value in wood_ress.items():
            for i in range(0, value):
                self.wood_ress.append(key)
        high_ress = {
            "pasture":4,
            "game":4,
            "wine":2,
            "coal":3,
            "iron":3,
            "gold":1,
            "gems":1,
            "silver":1,
            "copper":2,
            "stone":3
        }
        self.high_ress = []
        for key, value in high_ress.items():
            for i in range(0, value):
                self.high_ress.append(key)
        low_m_ress = {
            "iron":3,
            "gold":2,
            "pasture":4,
            "game":2,
            "wine":1,
            "silver":2,
            "gems":2,
            "copper":3,
            "stone":4,
            "coal":1
        }
        self.low_m_ress = []
        for key, value in low_m_ress.items():
            for i in range(0, value):
                self.low_m_ress.append(key)
        high_m_ress = {
            "iron":4,
            "gold":4,
            "silver":4,
            "copper":4,
            "gems":3,
            "stone":5
        }
        self.high_m_ress = []
        for key, value in high_m_ress.items():
            for i in range(0, value):
                self.high_m_ress.append(key)
        self.ress_dict = {
            0:self.sea_ress,
            1:self.coast_ress,
            2:self.low_ress,
            3:self.wood_ress,
            4:self.high_ress,
            5:self.low_m_ress,
            6:self.high_m_ress
        }

            
    def _createRessources(self, field):
        n = random.randint(0,3)
        if n == 3:
            m = random.randint(0,23)
            ressource_list = self.ress_dict[field.height]
            field.ressource = ressource_list[m]
        
        
    def setlevel(self, field):
        # 20 level system:
        # - 0-1 ocean
        # - 2-4 coastal
        # - 5-8 lowlands
        # - 9-13 grasslands
        # - 14-16 highlands
        # - 17-18 lower mountains
        # - 19 high mountains
        # The starting value is always the mean value of all neigbours
        # (with dia?)
        
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
            reach += 1 # search further
        if found_valids == 0:
            final = random.randint(0,19)
        else:
            mean = (total/found_valids)
            final = mean + random.uniform(-0.2, 0.2)
            if final > 19:
                final = 19
            elif final < 0:
                final = 0
        field.exact_height = float(final)
        final = int(final) # round down
        h_dict = {
            0:0,
            1:0,
            2:1,
            3:1,
            4:1,
            5:2,
            6:2,
            7:2,
            8:2,
            9:3,
            10:3,
            11:3,
            12:3,
            13:3,
            14:4,
            15:4,
            16:4,
            17:5,
            18:5,
            19:6
        }
        field.height = h_dict[final]
        
    def _draw_map(self, canvas_stat):
        self.canvas_width = canvas_stat
        self.canvas_height = canvas_stat
        if self.game_map is not None:
            self.game_map.destroy()
        self.game_window = Canvas(self.root, borderwidth=0, width=1500, height=800)
        self.game_map = Frame(self.game_window)
        self.vsb = Scrollbar(self.root, orient="vertical", command=self.game_window.yview)
        self.hsb = Scrollbar(self.root, orient="horizontal", command=self.game_window.xview)
        self.game_window.configure(yscrollcommand=self.vsb.set)
        self.game_window.configure(xscrollcommand=self.hsb.set)
        self.game_window.grid(row=0, column=0)
        self.game_window.create_window((8,8), window=self.game_map, anchor="nw")
        self.game_map.bind("<Configure>", lambda event, canvas=self.game_window: self._onFrameConfigure(self.game_window))
        frame = self.game_map
        self.canvas_fields = {}
        for x in range(len(self.fields)):
            for y in range(len(self.fields[x])):
                #f = Button(self.root, text=str(x)+str(y), command=self.show_field).grid(row=x, column=y)
                f = Canvas(frame, width=self.canvas_width, height=self.canvas_height)
                f.bind("<Button-1>", lambda event, field=self.fields[x][y]: self._field_info(field))
                f.grid(row=x, column=y, padx=0, pady=0, ipadx=0, ipady=0)
                #enter color
                color = self.fields[x][y].color()
                f.configure(background=color, highlightthickness=0)
                #f.create_text(canvas_width/2, canvas_height/2, text=str(x)+str(y))
                self.canvas_fields[self.fields[x][y].fieldID] = f
                if self.fields[x][y].city is not None:
                    self._draw_city(f, self.fields[x][y].city, self.canvas_width, self.canvas_height)
                elif self.fields[x][y].owner is not None:
                    f.create_rectangle(1, 1, self.canvas_width-2, self.canvas_height-2, outline=self.fields[x][y].owner.color)
        
                
    def create_tkinter(self):
        self.root = Tk()
        menu = Menu(self.root)
        self.root.config(menu=menu)
        filemenu = Menu(menu)
        zoommenu = Menu(menu)
        menu.add_cascade(label="Game", menu=filemenu)
        menu.add_cascade(label="Zoom", menu=zoommenu)
        zoommenu.add_command(label="100%", command=lambda c=8: self._draw_map(c))
        zoommenu.add_command(label="150%", command=lambda c=12: self._draw_map(c))
        zoommenu.add_command(label="200%", command=lambda c=16: self._draw_map(c))
        filemenu.add_command(label="Exit", command=self._leave)
        self._draw_map(12)
        self.vsb.grid(row=0,column=1,sticky=N+E+S)
        self.hsb.grid(row=1,column=0, sticky=W+S+E)
        #Set up a Box for all infos and description
        desc = Frame(self.root)
        desc.grid(row=0, column=2)
        self._info_ID = StringVar(desc, "")
        info_ID1 = Label(desc, justify=LEFT, text="FIELD ID:")
        info_ID1.grid(row=0, column=0)
        info_ID = Label(desc, justify=LEFT, textvariable=self._info_ID, anchor=NW)
        info_ID.grid(row=0, column=1)
        self._info_height = StringVar(desc, "")
        info_height = Label(desc, justify=LEFT, textvariable=self._info_height, anchor=NW)
        info_height1 = Label(desc, justify=LEFT, text="FIELD HEIGHT:")
        info_height.grid(row=1, column=1)
        info_height1.grid(row=1, column=0)
        self._info_ress = StringVar(desc, "")
        info_ressL = Label(desc, justify=LEFT, text="RESSOURCE:")
        info_ressL.grid(row=2, column=0)
        info_ress = Label(desc, justify=LEFT, textvariable=self._info_ress, anchor=NW)
        info_ress.grid(row=2, column=1)
        self._city_name = StringVar(desc, "")
        city_name = Message(desc, justify=LEFT, textvariable=self._city_name, anchor=NW, font="Verdana 30 bold", width=300)
        city_name.grid(pady=20, columnspan=2)
        city_attr = ["name", "empire", "county", "pop"]
        self.city_info = {}
        last_grid_row = 0
        for i, attr in enumerate(city_attr):
            self.city_info[attr] = StringVar(desc, "")
            l1 = Label(desc, justify=LEFT, text=attr)
            l1.grid(row=i+4, column=0)
            l2 = Label(desc, justify=LEFT, textvariable=self.city_info[attr])
            l2.grid(row=i+4, column=1)
            last_grid_row = i+4
        city_ressources_desc = Label(desc, justify=LEFT, text="City ressources:")
        city_ressources_desc.grid(row=last_grid_row+1, column=0)
        self._city_ressources = StringVar(desc, "")
        city_ressources = Label(desc, justify=LEFT, textvariable=self._city_ressources)
        city_ressources.grid(row=last_grid_row+1, column=1, sticky=W+E)
        ######################SHOW VALUES####################
        city_ressources_desc = Label(desc, justify=LEFT, text="Food:")
        city_ressources_desc.grid(row=last_grid_row+2, column=0)
        self._food = StringVar(desc, "")
        city_ressources = Label(desc, justify=LEFT, textvariable=self._food)
        city_ressources.grid(row=last_grid_row+2, column=1, sticky=W+E)
        city_ressources_desc = Label(desc, justify=LEFT, text="Production:")
        city_ressources_desc.grid(row=last_grid_row+3, column=0)
        self._production = StringVar(desc, "")
        city_ressources = Label(desc, justify=LEFT, textvariable=self._production)
        city_ressources.grid(row=last_grid_row+3, column=1, sticky=W+E)
        city_ressources_desc = Label(desc, justify=LEFT, text="Money:")
        city_ressources_desc.grid(row=last_grid_row+4, column=0)
        self._money = StringVar(desc, "")
        city_ressources = Label(desc, justify=LEFT, textvariable=self._money)
        city_ressources.grid(row=last_grid_row+4, column=1, sticky=W+E)
        ########################LEADER#########################
        show_leader_desc = Label(desc, justify=LEFT, text="Leader:")
        show_leader_desc.grid(row=last_grid_row+5, column=0)
        self._show_leader = StringVar(desc, "")
        show_leader = Label(desc, justify=LEFT, textvariable=self._show_leader)
        show_leader.grid(row=last_grid_row+5, column=1)
        ##################CULTURE###########################
        show_culture_desc = Label(desc, justify=LEFT, text="Culture:")
        show_culture_desc.grid(row=last_grid_row+6, column=0)
        self._show_culture = StringVar(desc, "")
        show_culture = Label(desc, justify=LEFT, textvariable=self._show_culture)
        show_culture.grid(row=last_grid_row+6, column=1)
        ########################CLOCK#############################
        date_frame = Frame(self.root)
        date_frame.grid(row=2, column=2)
        self.date = Label(date_frame)
        self.date.grid(sticky=W+E, columnspan=4)
        self.counter = 0 
        self.speed = 1000
        
        self.counter_label()
        # Buttons to control game speed
        speeds = [(100, "FAST"), (1000, "NORMAL"), (2000, "SLOW")]
        col = 0
        for sp, d in speeds:
            btn = Button(date_frame, text=d, command= lambda speed=sp: self._set_speed(speed), width=5)
            btn.grid(row=1, column=col)
            col += 1
        pause = Button(date_frame, text="PAUSE", command=self.cancel, width=5)
        pause.grid(row=1, column=3)
        
        news_frame = Frame(self.root)
        news_frame.grid(row=2, column=0)
        self._news = StringVar(desc, "No news yet")
        l = Label(news_frame, textvariable=self._news)
        l.grid(row=1, column=0)
            
        mainloop()
        
    def cancel(self):
        if self._job is not None:
            self.date.after_cancel(self._job)
            self._job = None
        
        
    def counter_label(self):
        def count():
            # Add things happening here
            self._events(self.counter)
            self.counter += 1
            self.date.config(text=str(self.counter))
            self._job = self.date.after(self.speed, count)
        count()
    
    def _set_speed(self, speed):
        self.cancel()
        self.speed = speed
        self.counter_label()
        
    def _events(self, month):
        #~ # grow cities every 10 seconds
        for c in self.cities:
            if int(str(month)[0]) == c.seed:
                c.detect_ressources()
                c.pop += (c.pop * c.growth)
                if not c.active and c.pop > 50:
                    c.make_city(self.culture_models)
                    self.alert_new_city(c)
                    
    def alert_new_city(self, city):
        self._news.set("{} just became a city!".format(city.name))
        self.root.update()
        
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
        toPrint = """%s""" % (sign)
        return toPrint
        
    def _neighbors(self):
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
        #~ closest_neighbors = [
            #~ (x+1, y),
            #~ (x-1, y),
            #~ (x, y+1),
            #~ (x, y-1)
        #~ ]
        #~ field_neighbors.append(self)
        #~ for xpos, ypos in closest_neighbors:
            #~ # check that pos is not outside of the map
            #~ if xpos >= 0 and ypos >= 0 and xpos < self.simMap.height and ypos < self.simMap.width:
                #~ if reach >= 1:
                    #~ field_neighbors.extend(fields[xpos][ypos].field_neighbor(reach-1))
        #~ return list(set(field_neighbors))
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
        if self.height == 0:
            clr = "navy"
        elif self.height == 1:
            clr = "blue"
        elif self.height == 2:
            clr = "PaleGreen2"
        elif self.height == 3:
            clr = "green"
        elif self.height == 4:
            clr = "orange"
        elif self.height == 5:
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
