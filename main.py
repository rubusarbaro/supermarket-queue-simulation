import colors
import elements
import environment
import functions

simulation = environment.Environment(0)
simulation.time_scale = 1
screen = environment.Screen(simulation,30,33,environment.Border.none)


## This part of the code build the layout.
outer_wall = elements.Wall(None)
for x in range(0,30) :
    outer_wall.set_in_screen(screen,x,29)   # Crea el borde inferior
for y in range(1,29) :
    outer_wall.set_in_screen(screen,29,y)   # Crea el borde derecho
for y in range(1,28) :
    outer_wall.set_in_screen(screen,0,y)    # Crea el borde izquierdo
for x in range(0,29) :
    elements.Queue().set_in_screen(screen,x,28) # Crea la fila principal

functions.generate_cashiers(simulation,3,15)

simulation.start()