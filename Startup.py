#! /usr/bin/python3
# This app is not only for setting terrain generation values, 
# but will also later provide a button to load existing savegames

from tkinter import *
from map import SimMap

class StartUp():
    def __init__(self):
        self.root = Tk()
        self.root.title("Game Setup")
        # map height
        Label(self.root, text="Map Height", justify=LEFT).grid(sticky=W+E)
        self.map_height = IntVar(self.root, 90)
        Entry(self.root, textvariable=self.map_height, justify=LEFT).grid(row=0, column=1, sticky=W+E)
        # map width
        Label(self.root, text="Map Width", justify=LEFT).grid(row=1, column=0, sticky=W+E)
        self.map_width = IntVar(self.root, 180)
        Entry(self.root, textvariable=self.map_width, justify=LEFT).grid(row=1, column=1, sticky=W+E)
        # separator
        Frame(self.root, height=2, bd=1, relief=SUNKEN).grid(columnspan=2, sticky=W+E)
        # region size (low value more fractured, high value less)
        Label(self.root, text="Region Size", justify=LEFT).grid(row=3, column=0, sticky=W+E)
        self.reach = IntVar(self.root, 8)
        Entry(self.root, textvariable=self.reach, justify=LEFT).grid(row=3, column=1, sticky=W+E)
        # border fracture (low value low fracture, high value more)
        Label(self.root, text="Border Fracture", justify=LEFT).grid(row=4, column=0, sticky=W+E)
        self.terrain_change = DoubleVar(self.root, 0.2)
        Entry(self.root, textvariable=self.terrain_change, justify=LEFT).grid(row=4, column=1, sticky=W+E)
        # separator
        Frame(self.root, height=2, bd=1, relief=SUNKEN).grid(columnspan=2, sticky=W+E)
        # Terrain chances
        self.terrain_types = [
            ("Ocean", IntVar(self.root,1)),
            ("Coastal", IntVar(self.root,3)),
            ("Lowlands", IntVar(self.root,4)),
            ("Woodlands", IntVar(self.root,4)),
            ("Highlands", IntVar(self.root,3)),
            ("Lower Mountains", IntVar(self.root,2)),
            ("High Mountains", IntVar(self.root,1))
        ]
        Label(self.root, text="Terrain Generation Chances:").grid(columnspan=2, sticky=W+E)
        for n, t in enumerate(self.terrain_types):
            Label(self.root, text=t[0], justify=LEFT).grid(row=n+7, column=0, sticky=W+E)
            Entry(self.root, textvariable=t[1], justify=LEFT).grid(row=n+7, column=1, sticky=W+E)
        # separator
        Frame(self.root, height=2, bd=1, relief=SUNKEN).grid(columnspan=2, sticky=W+E)
        # city generation chance
        self.city_gen = DoubleVar(self.root, 0.15)
        Label(self.root, text="CityGen rate", justify=LEFT).grid(column=0, sticky=W+E)
        Entry(self.root, textvariable=self.city_gen, justify=LEFT).grid(row=15, column=1, sticky=W+E)
        # separator
        Frame(self.root, height=2, bd=1, relief=SUNKEN).grid(columnspan=2, sticky=W+E)
        # Button: Start Game
        Button(self.root, text="Start Game", command=self._start).grid(columnspan=2, sticky=W+E)
        
        mainloop()
        
    def _start(self):
        newmap = SimMap(self.map_width.get(), self.map_height.get())
        newmap.reach_limit = self.reach.get()
        newmap.terrain_change_rate = self.terrain_change.get()
        newmap.ocean_chance = self.terrain_types[0][1].get()
        newmap.coastal_chance = self.terrain_types[1][1].get()
        newmap.lowlands_chance = self.terrain_types[2][1].get()
        newmap.woodlands_chance = self.terrain_types[3][1].get()
        newmap.highlands_chance = self.terrain_types[4][1].get()
        newmap.lower_m_chance = self.terrain_types[5][1].get()
        newmap.higher_m_chance = self.terrain_types[6][1].get()
        newmap.city_generation_chance = self.city_gen.get()
        newmap.fillfield()
        self.root.destroy()
        newmap.create_tkinter()
        


def main():
    new_game = StartUp()


if __name__ == "__main__":
    main()
