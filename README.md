# MittSim

MittSim is a python script to randomly generate maps

Start program like this:

```
~$ python3 Startup.py
```

All options can now be set in the Startup window!

Loading time is pretty long atm, which is because of the generation of
city names. If you want to shorten this process, set "Min Wealth To
Activate Cities" to 40 or higher. This will prevent activation of cities
and your map will be generated almost instantly.

What do the options in the startup menu mean?

- Map Height & Map Width

The number of fields on the y and x axis. 90/180 is the standard I'm using
but you can change it lower or higher if you like. If you go lower than
90/180, there's still a bug in which there will be no ocean fields be
added at the bottom of the map which makes it just part of a bigger map.

- Region Size & Border Fracture

Region size only has little influence on the map. A lower region size will usually
produce less ocean and more land. Border fracture regulates the rate
in which one terrain type changes into an other terrain type. 
If you want smaller regions with the same terrain types and lots of islands,
set this value high. For big regions and less islands, set it low.

- Height levels

Based on a height map, terrain is generated. You can change these values
to get more/less ocean or more/less mountains. E.g. set sealevel to 1 if
you don't want any oceans. Do not change sealevel to 0, this
will not create any water fields at all which breaks river generation.
The maximum height is 200 btw, so if you don't want the highest kind of mountains,
just set it above 210.

- Min Wealth To Activate Cities

In the current state of the game, cities can be "active" or "inactive".
Active cities get a name, color and some territory. Later, those cities will
also be those which can act, e.g. go to war, trade with other cities and so on.
The inactive cities are "barbarian cities", which can be conquered or will
make problems for the active cities through events (similar to Civilization).
If a city is active at the start of the game or not depends on their wealth,
that is the quality of their territory and the resources on it. 
If you set this value low, you will get a lot of active cities and a long loading
time (I'm working on it!), if you set it high, you will get fewer or no 
active cities and a shorter loading time. 
If you are only interested in terrain generation, set this always to 50.

There will probably follow more options later, for example setting the number
of rivers or the quantity of resources.
