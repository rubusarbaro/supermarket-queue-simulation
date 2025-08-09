## Modules to use in this file:
#from math import inf as infinite
from parameters import simulation_parameters
import elements     # Custom module: Provides graphical objects the agents can interact with.
import environment  # Custom module: Simulation manager.  

## Simulation initialization
simulation = environment.Environment()   # Controls the simulation with an internal clock.
screen = environment.Screen(simulation,30,30,elements.Border.none)  # Creates the simulation graphical layout.

## Layout customization.
outer_wall = elements.Wall(None)
for x in range(0, 30):
    outer_wall.set_in_screen(screen, x, 29)   # Crea el borde inferior
for y in range(1, 29):
    outer_wall.set_in_screen(screen, 29, y)   # Crea el borde derecho
for y in range(1, 28):
    outer_wall.set_in_screen(screen, 0, y)    # Crea el borde izquierdo
for x in range(0, 29):
    elements.Queue().set_in_screen(screen, x, 28) # Crea la fila principal

## Simulation
simulation.define_parameters(simulation_parameters)
simulation.start()