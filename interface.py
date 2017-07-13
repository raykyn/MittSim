#! /usr/bin/python3

#By Ismail Prada

import random
from city import City
from culture import start_Cultures
import events
from tkinter import *
from tkinter.ttk import *


class Application():
    def __init__(self, game, fields):
        # Some attributes
        self.game = game
        self.mapmode = "p"
        self.show_terrain = True
        self.fields = fields
        self.field_size = 10
        # Changing counters
        self._job = None
        self.counter = 0
        self.speed = 1000
        self.showing_city = None # The currently shown city
        # Initialize everything
        self.root = Tk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(str(self.screen_width) + "x" + str(self.screen_height))
        self.root.title("MyLittleFantasySimulator")
        self._create_menu()
        self._create_game_map_frame()
        self._create_scrollbars()
        self._create_description_frame()
        self._create_news_frame()
        self._create_date_frame()
        # create a dialogue in which the user can input his own settings? => Startup
        self.create_map(fields)
        
        mainloop()
        
    def create_map(self, fields):
        #~ try:
            #~ self.inner_map.delete("all")
        #~ except:
            #~ pass
        #~ frame = self.game_map
        size = self.field_size
        map_height = len(fields)*size
        map_width = len(fields[0])*size
        #~ self.inner_map = Canvas(frame, width=map_width, height=map_height)
        
        for y, row in enumerate(fields):
            for x, f in enumerate(row):
                # Needs to be reimplemented
                if self.mapmode == "Heightmap":
                    greytone = (230-f.height)
                    terrain_color = "#%02X%02X%02X" % (greytone, greytone, greytone)
                    river_color = "white"
                if self.show_terrain:
                    terrain_colors = {
                        "High Mountains":"gray60",
                        "Low Mountains":"brown",
                        "Grassland":"PaleGreen2",
                        "Woodland":"forest green",
                        "Desert":"khaki",
                        "Wetlands":"SeaGreen1",
                        "Swamps":"olive drab",
                        "Steppe":"yellow green",
                        "Ocean":"navy"
                    }
                    terrain_color = terrain_colors[f.terrain]
                    river_color = "blue"
                else:
                    if f.terrain != "Ocean":
                        terrain_color = "white"
                    else:
                        terrain_color = "navy"
                    river_color = "blue"
                f.graphic = self.inner_map.create_rectangle(x*size, y*size, (x+1)*size, (y+1)*size, fill=terrain_color, outline="", tag=("field", f.fieldID))
                if (self.show_terrain or self.mapmode == "terrains") and f.hill:
                    self.inner_map.create_line(x*size+1, y*size+size*(2/3), x*size+(size/2), y*size+size/3, fill="black", tag=("hill1", f.fieldID))
                    self.inner_map.create_line(x*size+size/2, y*size+size/3, x*size+size-1, y*size+size*(2/3), fill="black", tag=("hill2", f.fieldID))
                if f.river is not None:
                    for t in f.river:
                        x1, y1, x2, y2 = t
                        self.inner_map.create_line(x*size+size/2, y*size+size/2, (y1*size)+(size/2), (x1*size)+(size/2), fill=river_color, tag=("river", f.fieldID))
                        self.inner_map.create_line(x*size+(size/2), y*size+size/2, y2*size+size/2, x2*size+size/2, fill=river_color, tag=("river", f.fieldID))
                if f.lake:
                    self.inner_map.create_rectangle((x*size)+(size/4), (y*size)+(size/4), ((x+1)*size)-(size/4), (y+1)*size-size/4, fill=river_color, tag=("lake", f.fieldID), outline="")
                if self.mapmode != "t":
                    if f.city is not None:
                        if f.city.active:
                            if self.mapmode == "p": # political
                                citycolor = f.owner.color
                            elif self.mapmode == "c": # cultural
                                if f.owner.culture is not None:
                                    citycolor = f.owner.culture.color
                                else:
                                    citycolor = "white"
                            self.inner_map.create_rectangle((x*size)+(size/4), (y*size)+(size/4), ((x+1)*size)-(size/4), (y+1)*size-size/4, fill=citycolor, tag=("city", f.fieldID))
                    if f.owner is not None:
                        if f.owner.active:
                            if self.mapmode == "p": # political
                                bordercolor = f.owner.color
                            elif self.mapmode == "c": # cultural
                                bordercolor = f.owner.culture.color
                            self.inner_map.create_rectangle(x*size+1, y*size+1, (x+1)*size-1, (y+1)*size-1, outline=bordercolor, tag="border")
                        else:
                            self.inner_map.create_rectangle(x*size+1, y*size+1, (x+1)*size-1, (y+1)*size-1, outline="", tag="border")
                    else:
                        self.inner_map.create_rectangle(x*size+1, y*size+1, (x+1)*size-1, (y+1)*size-1, outline="", tag="border")

        self.inner_map.bind("<Button-3>", self._get_field)
        self.inner_map.bind("<Button-1>", self._scroll_start)
        self.inner_map.bind("<B1-Motion>", self._scroll_move)
        self.inner_map.bind("<Button-4>", self.zoomerP)
        self.inner_map.bind("<Button-5>", self.zoomerM)
        #~ self.inner_map.pack()
        
        
    def _get_field(self, event):
        size = self.field_size
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        # Show all the stuff in the right hand side bar :D
        f_graphic = self.inner_map.find_closest(x, y)
        f = self.game.fieldIDs[int(self.inner_map.gettags(f_graphic)[1])]
        #f = self.fields[int(y)][int(x)]
        # Set the StringVars for Field Info
        self.field_info_values["FIELD ID:"].set(str(f.fieldID))
        self.field_info_values["TERRAIN TYPE:"].set(f.terrain)
        self.field_info_values["RESSOURCE:"].set(str(f.resource))
        self.field_info_values["POPULATION:"].set(str(round(f.city.pop)))
        self.field_info_values["FOOD:"].set(str(f.food))
        self.field_info_values["PRODUCTION:"].set(str(f.production))
        self.field_info_values["MONEY:"].set(str(f.money))
        other = []
        if f.hill:
            other.append("Hill")
        if f.lake:
            other.append("Lake")
        elif len(f.river) > 0:
            other.append("River")
        self.field_info_values["OTHER:"].set(', '.join(other))
        # Set the StringVars for City Info
        #~ if f.owner is not None:
            #~ self._city_name.set(f.owner.name)
            #~ if f.owner.leader is not None:
                #~ self.city_info_values["Leader:"].set(f.owner.leader.firstname)
            #~ else:
                #~ self.city_info_values["Leader:"].set(None)
            #~ self.city_info_values["Population:"].set(round(f.owner.pop))
            #~ if f.owner.culture is not None:
                #~ self.city_info_values["Culture:"].set(f.owner.culture.name)
            #~ else:
                #~ self.city_info_values["Culture:"].set(None)
            #~ self.city_info_values["Food:"].set(f.owner.values["f"])
            #~ self.city_info_values["Production:"].set(f.owner.values["p"])
            #~ self.city_info_values["Money:"].set(f.owner.values["m"])
            #~ self.city_info_values["resources:"].set(', '.join(f.owner.resources))
            #~ self.char_info.pack_forget()
            #~ self.showing = f.owner
            #~ self.city_info.pack(fill="both")
            #~ self.emp_info.pack(fill="both")
        #~ else:
            #~ self._city_name.set("")
            #~ for l in self.city_info_values:
                #~ self.city_info_values[l].set("")
            #~ self.city_info.pack_forget()
            #~ self.emp_info.pack_forget()
        

        
    def _create_menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)
        filemenu = Menu(menu)
        zoommenu = Menu(menu)
        mapmodes = Menu(menu)
        menu.add_cascade(label="Game", menu=filemenu)
        menu.add_cascade(label="Mapmodes", menu=mapmodes)
        filemenu.add_command(label="Export Map", command=self._export_map)
        filemenu.add_command(label="Exit", command=self._leave)
        mapmodes.add_command(label="Political", command= lambda x="p": self._change_mapmode(x))
        mapmodes.add_command(label="Cultures", command= lambda x="c": self._change_mapmode(x))
        mapmodes.add_command(label="Terrain Only", command= lambda x="t": self._change_mapmode(x))
        mapmodes.add_command(label="Toggle Terrain", command=self._toggle_terrain)
        mapmodes.add_command(label="Terrains", command= lambda x="terrains": self._change_mapmode(x))
        
    def _export_map(self):
        self.inner_map.update()
        self.inner_map.postscript(file="exported_map.ps", colormode="color")
        
    def _change_mapmode(self, mode):
        self.mapmode = mode
        self.create_map(self.fields)
        
    def _toggle_terrain(self):
        if self.show_terrain:
            self.show_terrain = False
        else:
            self.show_terrain = True
        self.create_map(self.fields)
    
        
    def _create_game_map_frame(self):
        self.inner_map = Canvas(self.root, borderwidth=0, width=self.screen_width*0.8, height=self.screen_height*0.8)
        #~ self.game_map = Frame(self.inner_map)
        self.inner_map.grid(row=0, column=0)
        #~ self.inner_map.create_window((8,8), window=self.game_map, anchor="nw")
        self.inner_map.bind("<Configure>", lambda event, canvas=self.inner_map: self._onFrameConfigure(canvas))
        #~ self.inner_map.bind("<Button-1>", self._get_field)
        #~ self.inner_map.bind("<Button-1>", self._scroll_start)
        #~ self.inner_map.bind("<B1-Motion>", self._scroll_move)
        #~ self.inner_map.bind("<Button-4>", self.zoomerP)
        #~ self.inner_map.bind("<Button-5>", self.zoomerM)
        #~ self.inner_map.bind("<MouseWheel>",self.zoomer)
        
    #windows zoom
    def zoomer(self,event):
        if (event.delta > 0):
            self.inner_map.scale("all", 0, 0, 1.1, 1.1)
            self.field_size = self.field_size*1.1
        elif (event.delta < 0):
            self.inner_map.scale("all", 0, 0, 0.9, 0.9)
            self.field_size = self.field_size*0.9
        self.inner_map.configure(scrollregion = self.inner_map.bbox("all"))

    #linux zoom
    def zoomerP(self,event):
        self.inner_map.scale("all", 0, 0, 1.1, 1.1)
        self.field_size = self.field_size*1.1
        self.inner_map.configure(scrollregion = self.inner_map.bbox("all"))
    def zoomerM(self,event):
        self.inner_map.scale("all", 0, 0, 0.9, 0.9)
        self.field_size = self.field_size*0.9
        self.inner_map.configure(scrollregion = self.inner_map.bbox("all"))
        
    def _scroll_start(self, event):
        self.inner_map.scan_mark(event.x, event.y)

    def _scroll_move(self, event):
        self.inner_map.scan_dragto(event.x, event.y, gain=1)
        
    def _scroll_start(self, event):
        self.inner_map.scan_mark(event.x, event.y)

    def _scroll_move(self, event):
        self.inner_map.scan_dragto(event.x, event.y, gain=1)

    def _onFrameConfigure(self, canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    def _create_scrollbars(self):
        self.vsb = Scrollbar(self.root, orient="vertical", command=self.inner_map.yview)
        self.hsb = Scrollbar(self.root, orient="horizontal", command=self.inner_map.xview)
        self.inner_map.configure(yscrollcommand=self.vsb.set)
        self.inner_map.configure(xscrollcommand=self.hsb.set)
        self.vsb.grid(row=0,column=1,sticky=N+E+S)
        self.hsb.grid(row=1,column=0, sticky=W+S+E)
        
    def _create_description_frame(self):
        desc = Frame(self.root)
        desc.grid(row=0, column=2, sticky=N+W+E, ipady=10)
        # 3 frames packed below that:
        # Field-Info, City-Info, Empire-Info
        self._field_info(desc)
        self._city_info(desc)
        self._char_info(desc)
        self._emp_info(desc)
        
    def _field_info(self, desc):
        field_info = LabelFrame(desc, text="FIELD INFO")
        field_info.pack(fill="x", expand=1, padx=10, ipady=5)
        field_info_list = [
            "FIELD ID:",
            "TERRAIN TYPE:",
            "RESSOURCE:",
            "OTHER:",
            "POPULATION:",
            "FOOD:",
            "PRODUCTION:",
            "MONEY:"
        ]
        self.field_info_values = {}
        for n, label in enumerate(field_info_list):
            self.field_info_values[label] = StringVar(field_info, "")
            Label(field_info, justify=LEFT, text=label).grid(row=n, column=0,sticky=N+W, padx=10)
            Label(field_info, justify=LEFT, textvariable=self.field_info_values[label]).grid(row=n, column=1, sticky=N+W)
        
    def _city_info(self, desc):
        self.city_info = Frame(desc, relief=RIDGE)
        #self.city_info.pack(fill="both")
        self._city_name = StringVar(desc, "")
        city_name = Message(self.city_info, justify=LEFT, textvariable=self._city_name, font="Verdana 20 bold", width=300)
        city_name.grid(pady=20, columnspan=2, sticky=W+E)
        city_info_list = [
            "Leader:",
            "Population:",
            "Culture:",
            "Food:",
            "Production:",
            "Money:",
            "resources:"
        ]
        self.city_info_values = {}
        for n, label in enumerate(city_info_list):
            self.city_info_values[label] = StringVar(self.city_info, "")
            Label(self.city_info, text=label).grid(row=n+1, column=0, sticky=W+E, padx=10)
            Message(self.city_info, textvariable=self.city_info_values[label], width=200).grid(row=n+1, column=1, sticky=W+E)
        Button(self.city_info, text="More", command=self._show_char_info).grid(row=1, column=2)
        
    def _show_char_info(self):
        self.city_info.pack_forget()
        self.emp_info.pack_forget()
        try:
            self.char_name.set(self.showing.leader.fullname)
            self.char_age.set(self.showing.leader.age)
        except:
            self.char_name.set("No Leader")
            self.char_age.set("")
        self.char_info.pack(fill="both")
    
    def _char_info(self, desc):
        self.char_info = Frame(desc, relief=RIDGE)
        self.char_name = StringVar(self.char_info, "")
        Message(self.char_info, justify=LEFT, textvariable=self.char_name, width=200, font="Verdana 10 bold").grid(row=0, column=0, sticky=W+E, columnspan=2)
        self.char_age = IntVar(self.char_info, 0)
        Label(self.char_info, justify=LEFT, text="Age:").grid(row=1, column=0, sticky=W+E)
        Message(self.char_info, justify=LEFT, textvariable=self.char_age, width=200).grid(row=1, column=1, sticky=W+E)
        
        
    def _emp_info(self, desc):
        self.emp_info = Frame(desc)
        
        
    def _create_news_frame(self):
        news_frame = Frame(self.root)
        news_frame.grid(row=2, column=0)
        self._news = StringVar(news_frame, "No news yet")
        l = Label(news_frame, textvariable=self._news)
        l.grid(row=0, column=0)
        
    def _create_date_frame(self):
        date_frame = Frame(self.root)
        date_frame.grid(row=2, column=2)
        self.date = Label(date_frame)
        self.date.grid(sticky=W+E, columnspan=4)
        speeds = [(100, "FAST"), (1000, "NORMAL"), (3000, "SLOW")]
        col = 0
        for sp, d in speeds:
            btn = Button(date_frame, text=d, command= lambda speed=sp: self._set_speed(speed), width=7)
            btn.grid(row=1, column=col)
            col += 1
        pause = Button(date_frame, text="PAUSE", command=self.cancel, width=7)
        pause.grid(row=1, column=3)
        #self.counter_label()
        
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
        
    def _events(self, tick):
        events.run(tick, self.game, self)
                   
                    
    def _alert_new_city(self, city):
        self._news.set("{} just became a city!".format(city.name))

        
    def _leave(self):
        exit()
    
    
if __name__ == "__main__":
    new_app = Application()
