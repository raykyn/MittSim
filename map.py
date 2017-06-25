#! /usr/bin/python3

#By Ismail Prada

import random
from tkinter import *

class SimMap(object):
    
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.fields = [["O" for x in range(self.width)] for y in range(self.height)] 

    def printfield(self):
        for x in range(len(self.fields)):
            for y in range(len(self.fields[x])):
                print(self.fields[x][y], end=' ')
            print()
            
    def fillfield(self):
        self.fieldIDcounter = 1
        for y in range(self.height):
            for x in range(self.width):
                newField = Field(self.fieldIDcounter, x, y)
                self.fieldIDcounter += 1
                self.setlevel(newField)
                self.fields[y][x] = newField
                
                
    #def setlevel(self, field):
        #if field.fieldID == 0:
            #field.height = 3
        #else:
            #neighbours = [field.upleftN, field.upN, field.leftN]
            #validNs = []
            #for neighbour in neighbours:
                #if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= self.height or neighbour[1] >= self.width:
                    #pass
                #elif type(self.fields[neighbour[0]][neighbour[1]]) == Field:
                    #validNs.append(self.fields[neighbour[0]][neighbour[1]].height)
            #print(validNs)
        
    def setlevel(self, field):
        if field.fieldID == 1:
            field.height = 3
        else:
            neighborheights = []
            for element in field.neighbors():
                if element[0] < 0 or element[1] < 0 or element[0] >= self.height or element[1] >= self.width:
                    pass
                elif type(self.fields[element[0]][element[1]]) == Field:
                    neighborheights.append(self.fields[element[0]][element[1]].height)
            if len(neighborheights) == 1:
                randomnum = random.randint(1,10)
                if neighborheights[0] == 0:
                    if randomnum <= 2:
                        field.height = 1
                    else:
                        field.height = 0
                elif neighborheights[0] == 1:
                    if randomnum <= 4:
                        field.height = 0
                    elif randomnum > 6:
                        field.height = 2
                    else:
                        field.height = 1
                elif neighborheights[0] == 2:
                    if randomnum <= 4:
                        field.height = 1
                    elif randomnum > 6:
                        field.height = 3
                    else:
                        field.height = 2
                elif neighborheights[0] == 3:
                    if randomnum <= 6:
                        field.height = 3
                    elif randomnum > 8:
                        field.height = 2
                    else:
                        field.height = 4
                elif neighborheights[0] == 4:
                    if randomnum <= 3:
                        field.height = 5
                    elif randomnum > 7:
                        field.height = 3
                    else:
                        field.height = 4
                elif neighborheights[0] == 5:
                    if randomnum <= 4:
                        field.height = 4
                    elif randomnum > 8:
                        field.height = 6
                    else:
                        field.height = 5
                elif neighborheights[0] == 6:
                    if randomnum <= 3:
                        field.height = 6
                    else:
                        field.height = 5
            else:
                randomnum = random.randint(1,10)
                if neighborheights[0] == 0 and neighborheights[1] == 0:
                    if randomnum <= 2:
                        field.height = 1
                    else:
                        field.height = 0
                elif neighborheights[0] == 0 and neighborheights[1] == 1:
                    if randomnum <= 4:
                        field.height = 1
                    else:
                        field.height = 0
                elif neighborheights[0] == 1 and neighborheights[1] == 0:
                    if randomnum <= 4:
                        field.height = 1
                    else:
                        field.height = 0
                elif neighborheights[0] == 1 and neighborheights[1] == 1:
                    if randomnum <= 4:
                        field.height = 0
                    elif randomnum > 6:
                        field.height = 2
                    else:
                        field.height = 1
                elif neighborheights[0] == 2 and neighborheights[1] == 1:
                    if randomnum <= 5:
                        field.height = 1
                    else:
                        field.height = 2
                elif neighborheights[0] == 1 and neighborheights[1] == 2:
                    if randomnum <= 5:
                        field.height = 1
                    else:
                        field.height = 2
                elif neighborheights[0] == 2 and neighborheights[1] == 2:
                    if randomnum <= 4:
                        field.height = 1
                    elif randomnum > 6:
                        field.height = 3
                    else:
                        field.height = 2
                elif neighborheights[0] == 3 and neighborheights[1] == 2:
                    if randomnum <= 7:
                        field.height = 3
                    else:
                        field.height = 2
                elif neighborheights[0] == 2 and neighborheights[1] == 3:
                    if randomnum <= 7:
                        field.height = 3
                    else:
                        field.height = 2
                elif neighborheights[0] == 3 and neighborheights[1] == 3:
                    if randomnum <= 6:
                        field.height = 3
                    elif randomnum > 8:
                        field.height = 2
                    else:
                        field.height = 4
                elif neighborheights[0] == 4 and neighborheights[1] == 3:
                    if randomnum <= 7:
                        field.height = 3
                    else:
                        field.height = 4
                elif neighborheights[0] == 3 and neighborheights[1] == 4:
                    if randomnum <= 7:
                        field.height = 3
                    else:
                        field.height = 4
                elif neighborheights[0] == 4 and neighborheights[1] == 4:
                    if randomnum <= 3:
                        field.height = 5
                    elif randomnum > 7:
                        field.height = 3
                    else:
                        field.height = 4
                elif neighborheights[0] == 5 and neighborheights[1] == 4:
                    if randomnum <= 7:
                        field.height = 4
                    else:
                        field.height = 5
                elif neighborheights[0] == 4 and neighborheights[1] == 5:
                    if randomnum <= 7:
                        field.height = 4
                    else:
                        field.height = 5
                elif neighborheights[0] == 5 and neighborheights[1] == 5:
                    if randomnum <= 4:
                        field.height = 4
                    elif randomnum > 8:
                        field.height = 6
                    else:
                        field.height = 5
                elif neighborheights[0] == 6 and neighborheights[1] == 5:
                    if randomnum <= 7:
                        field.height = 5
                    else:
                        field.height = 6
                elif neighborheights[0] == 5 and neighborheights[1] == 6:
                    if randomnum <= 7:
                        field.height = 5
                    else:
                        field.height = 6
                elif neighborheights[0] == 6 and neighborheights[1] == 6:
                    if randomnum <= 3:
                        field.height = 6
                    else:
                        field.height = 5
                elif neighborheights[0]-neighborheights[1] == 2:
                    field.height = neighborheights[0]-1
                elif neighborheights[1]-neighborheights[0] == 2:
                    field.height = neighborheights[1]-1
                
    def create_tkinter(self):
        root = Tk()
        menu = Menu(root)
        root.config(menu=menu)
        filemenu = Menu(menu)
        menu.add_cascade(label="Game", menu=filemenu)
        filemenu.add_command(label="Exit", command=self._leave)
        canvas = Canvas(root, borderwidth=0, width=1500, height=800)
        frame = Frame(canvas)
        vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
        hsb = Scrollbar(root, orient="horizontal", command=canvas.xview)
        canvas.configure(yscrollcommand=vsb.set)
        canvas.configure(xscrollcommand=hsb.set)
        vsb.grid(sticky=N+E+S)
        hsb.grid(sticky=W+S+E)
        canvas.grid(row=0, column=0)
        canvas.create_window((8,8), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda event, canvas=canvas: self._onFrameConfigure(canvas))
        #canvas.bind_all("<MouseWheel>", lambda event, canvas=canvas: self._on_mousewheel(canvas))
        canvas_width = 15
        canvas_height = 15
        self.canvas_fields = {}
        for x in range(len(self.fields)):
            for y in range(len(self.fields[x])):
                #f = Button(root, text=str(x)+str(y), command=self.show_field).grid(row=x, column=y)
                f = Canvas(frame, width=canvas_width, height=canvas_height)
                f.grid(row=x, column=y, padx=0, pady=0, ipadx=0, ipady=0)
                #enter color
                color = self.fields[x][y].color()
                f.configure(background=color, highlightthickness=0)
                #f.create_text(canvas_width/2, canvas_height/2, text=str(x)+str(y))
                self.canvas_fields[self.fields[x][y].fieldID] = f
        infos = Message(root, text="PLACEHOLDER").grid(row=0, column=1)
        print(self.canvas_fields)
        mainloop()
        
    def _onFrameConfigure(self, canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    #~ def _on_mousewheel(self, canvas):
        #~ canvas.yview_scroll(-1*(event.delta/120), "units")
        
    #~ def show_field(self):
        #~ pass
        
    def _leave(self):
        exit()
                        
class Field(object):
    
    def __init__(self, id, x, y):
        self.fieldID = id
        self.x = x
        self.y = y
        #Höhe: 0: Sealevel 1: Coastal 2: Lowlands 3: Flatlands 4: Highlands 
        #5: Low mountains 6: High Mountains
        self.height = 7
        
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
        
    def neighbors(self):
        self.neighbors = []
        self.upN = (self.y-1,self.x)
        self.neighbors.append(self.upN)
        self.rightN = (self.y, self.x+1)
        self.neighbors.append(self.rightN)
        self.downN = (self.y+1, self.x)
        self.neighbors.append(self.downN)
        self.leftN = (self.y, self.x-1)
        self.neighbors.append(self.leftN)
        return self.neighbors
        
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

        
def main():
    newmap = SimMap(180,90)
    newmap.fillfield()
    newmap.create_tkinter()

if __name__ == "__main__":
    main()
