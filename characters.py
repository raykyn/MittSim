#! /usr/bin/python3

from culture import Culture
import random

class Character():
    def __init__(self, models, culture, residence, age):
        self.firstname = culture.generate_name(models, "m")
        self.culture = culture
        self.models = models
        self.place = residence
        # Fullname will later always be set to highest title
        self.fullname = "{} of {}".format(self.firstname, self.place.name)
        self.age = age
        self.state = "alive" # alive or dead
        self.titles = []
        
        
def age(self):
    self.age += 1
    if self.age > 50: # Age 100 100% dead, 50 0.1 % dead chance
        chance_to_die = (self.age - 50)*0.2
        m = random.randint(1,100)
        if m <= chance_to_die:
            self.die()
    
    
def die(self):
    # Lose title if has any and distribute them to successors
    # Standard succession type is Gavelkind => depending on Culture
    # Next line is only a placeholder until a proper system is implemented
    successor = Character(models, self.culture, self.place, random.randint(30,60))
    self.state = "dead"
