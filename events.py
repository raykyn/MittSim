#! /usr/bin/python3

"""
This file contains various events, which are trigerred after a certain
number of ticks. Cities use a seed system for that, which means they
have a number between 0 and 9 assigned, and only trigger when the tick
shows their number.
To optimize performance, it might be better to save all cities in a 
dictionary, ordered by their seed, so the algorithm doesn't need 
to parse the whole list of cities every time.
"""

def run(tick, game, interface):
    tick = int(str(tick)[-1])
    for c in game.cities:
        if c.seed == tick:
            # Only triggers all 10 seconds
            c.detect_ressources()
            c.calculate_values()
            c.calculate_growth()
            grow(c, game.culture_models, interface)
            
            
                
def grow(c, models, interface):
    c.pop = c.pop + (c.pop*c.growth)
    if c.pop >= 500 and not c.active:
        c.make_city(models, interface)
        interface._alert_new_city(c)
