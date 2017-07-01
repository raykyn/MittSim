#! /usr/bin/python3

#By Ismail Prada

import random
from city import City
from culture import start_Cultures
import events
from tkinter import *


class Application():
    def __init__(self, game, fields):
        # Some attributes
        self.game = game
        self.mapmode = "p"
        self.fields = fields
        self.field_size = 12
        # Changing counters
        self._job = None
        self.counter = 0
        self.speed = 1000
        # Initialize everything
        self.root = Tk()
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
        try:
            self.inner_map.destroy()
        except:
            pass
        frame = self.game_map
        size = self.field_size
        map_height = len(fields)*size
        map_width = len(fields[0])*size
        self.inner_map = Canvas(frame, width=map_width, height=map_height)
        
        for y, row in enumerate(fields):
            for x, f in enumerate(row):
                self.inner_map.create_rectangle(x*size, y*size, (x+1)*size, (y+1)*size, fill=f.color(), outline="", tag="field")
                if self.mapmode != "t":
                    if f.city is not None:
                        if self.mapmode == "p": # political
                            citycolor = f.owner.color
                        elif self.mapmode == "c": # cultural
                            if f.owner.culture is not None:
                                citycolor = f.owner.culture.color
                            else:
                                citycolor = "white"
                        self.inner_map.create_rectangle((x*size)+(size/4), (y*size)+(size/4), ((x+1)*size)-(size/4), (y+1)*size-size/4, fill=citycolor, tag="city")
                    elif f.owner is not None:
                        if self.mapmode == "p": # political
                            bordercolor = f.owner.color
                        elif self.mapmode == "c": # cultural
                            bordercolor = f.owner.culture.color
                        self.inner_map.create_rectangle(x*size+1, y*size+1, (x+1)*size-1, (y+1)*size-1, outline=bordercolor, tag="border")
                    elif f.owner is None:
                        self.inner_map.create_rectangle(x*size+1, y*size+1, (x+1)*size-1, (y+1)*size-1, outline="", tag="border")
        self.inner_map.bind("<Button-1>", self._get_field)
        self.inner_map.pack()
        
    def _get_field(self, event):
        size = self.field_size
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        xpos = int(x/size)
        ypos = int(y/size)
        # Show all the stuff in the right hand side bar :D
        f = self.fields[ypos][xpos]
        # Set the StringVars for Field Info
        self.field_info_values["FIELD ID:"].set(str(f.fieldID))
        terrain_types = {
            0:"Ocean",
            1:"Coastal",
            2:"Grassland",
            3:"Woodland",
            4:"Hills",
            5:"Lower Mountains",
            6:"Higher Mountains"
        }
        self.field_info_values["TERRAIN TYPE:"].set(terrain_types[f.height])
        self.field_info_values["RESSOURCE:"].set(str(f.ressource))
        # Set the StringVars for City Info
        if f.owner is not None:
            self._city_name.set(f.owner.name)
            if f.owner.leader is not None:
                self.city_info_values["Leader:"].set(f.owner.leader.fullname)
            else:
                self.city_info_values["Leader:"].set(None)
            self.city_info_values["Population:"].set(round(f.owner.pop))
            if f.owner.culture is not None:
                self.city_info_values["Culture:"].set(f.owner.culture.name)
            else:
                self.city_info_values["Culture:"].set(None)
            self.city_info_values["Food:"].set(f.owner.values["f"])
            self.city_info_values["Production:"].set(f.owner.values["p"])
            self.city_info_values["Money:"].set(f.owner.values["m"])
            self.city_info_values["Ressources:"].set(', '.join(f.owner.ressources))
        else:
            self._city_name.set("")
            for l in self.city_info_values:
                self.city_info_values[l].set("")

        
    def _create_menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu)
        filemenu = Menu(menu)
        zoommenu = Menu(menu)
        mapmodes = Menu(menu)
        menu.add_cascade(label="Game", menu=filemenu)
        menu.add_cascade(label="Zoom", menu=zoommenu)
        menu.add_cascade(label="Mapmodes", menu=mapmodes)
        filemenu.add_command(label="Exit", command=self._leave)
        zoommenu.add_command(label="All", command= lambda x=8: self._zoom(x))
        zoommenu.add_command(label="Normal", command= lambda x=12: self._zoom(x))
        zoommenu.add_command(label="Close", command= lambda x=16: self._zoom(x))
        mapmodes.add_command(label="Political", command= lambda x="p": self._change_mapmode(x))
        mapmodes.add_command(label="Cultures", command= lambda x="c": self._change_mapmode(x))
        mapmodes.add_command(label="Terrain Only", command= lambda x="t": self._change_mapmode(x))
        
    def _zoom(self, size):
        self.field_size = size
        self.create_map(self.fields)
        
    def _change_mapmode(self, mode):
        self.mapmode = mode
        self.create_map(self.fields)
    
        
    def _create_game_map_frame(self):
        self.game_window = Canvas(self.root, borderwidth=0, width=1500, height=800)
        self.game_map = Frame(self.game_window)
        self.game_window.grid(row=0, column=0)
        self.game_window.create_window((8,8), window=self.game_map, anchor="nw")
        self.game_map.bind("<Configure>", lambda event, canvas=self.game_window: self._onFrameConfigure(canvas))
        
    def _onFrameConfigure(self, canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    def _create_scrollbars(self):
        self.vsb = Scrollbar(self.root, orient="vertical", command=self.game_window.yview)
        self.hsb = Scrollbar(self.root, orient="horizontal", command=self.game_window.xview)
        self.game_window.configure(yscrollcommand=self.vsb.set)
        self.game_window.configure(xscrollcommand=self.hsb.set)
        self.vsb.grid(row=0,column=1,sticky=N+E+S)
        self.hsb.grid(row=1,column=0, sticky=W+S+E)
        
    def _create_description_frame(self):
        desc = Frame(self.root, width=300, height=800)
        desc.grid(row=0, column=2)
        # 3 frames packed below that:
        # Field-Info, City-Info, Empire-Info
        self._field_info(desc)
        self._city_info(desc)
        self._emp_info(desc)
        
    def _field_info(self, desc):
        field_info = Frame(desc, width=300, height=200, relief=RIDGE)
        field_info.pack(fill="both")
        field_info_list = [
            "FIELD ID:",
            "TERRAIN TYPE:",
            "RESSOURCE:"
        ]
        self.field_info_values = {}
        for n, label in enumerate(field_info_list):
            self.field_info_values[label] = StringVar(field_info, "")
            Label(field_info, justify=LEFT, text=label).grid(row=n, column=0, sticky=N+W, padx=10)
            Label(field_info, justify=LEFT, textvariable=self.field_info_values[label]).grid(row=n, column=1, sticky=N+W)
        
    def _city_info(self, desc):
        city_info = Frame(desc, width=300, height=300, relief=RIDGE)
        city_info.pack(fill="both")
        self._city_name = StringVar(desc, "")
        city_name = Message(city_info, justify=LEFT, textvariable=self._city_name, font="Verdana 20 bold", width=300)
        city_name.grid(pady=20, columnspan=2)
        city_info_list = [
            "Leader:",
            "Population:",
            "Culture:",
            "Food:",
            "Production:",
            "Money:",
            "Ressources:"
        ]
        self.city_info_values = {}
        for n, label in enumerate(city_info_list):
            self.city_info_values[label] = StringVar(city_info, "")
            Label(city_info, justify=LEFT, text=label).grid(row=n+1, column=0, sticky=N+W, padx=10)
            Message(city_info, justify=LEFT, textvariable=self.city_info_values[label], width=200).grid(row=n+1, column=1, sticky=N+W)
        
    def _emp_info(self, desc):
        emp_info = Frame(desc, width=300, height=300)
        emp_info.pack()
        
        
    def _create_news_frame(self):
        news_frame = Frame(self.root, width=1500, height=100)
        news_frame.grid(row=2, column=0)
        self._news = StringVar(news_frame, "No news yet")
        l = Label(news_frame, textvariable=self._news)
        l.grid(row=0, column=0)
        
    def _create_date_frame(self):
        date_frame = Frame(self.root, width=300, height=100)
        date_frame.grid(row=2, column=2)
        self.date = Label(date_frame)
        self.date.grid(sticky=W+E, columnspan=4)
        speeds = [(100, "FAST"), (1000, "NORMAL"), (2000, "SLOW")]
        col = 0
        for sp, d in speeds:
            btn = Button(date_frame, text=d, command= lambda speed=sp: self._set_speed(speed), width=5)
            btn.grid(row=1, column=col)
            col += 1
        pause = Button(date_frame, text="PAUSE", command=self.cancel, width=5)
        pause.grid(row=1, column=3)
        self.counter_label()
        
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
