###########################################
##  Saúl R. Morales © 2025 MIT License   ##
###########################################
## This module contains simulation objects that agents can interact with.


# Modules to use in this file:
import colors   # Allows to modify printed text.

class Element () :
    """
    Parent class.

    Attr:
        x_location (int): Object location in the x axis of screen layout.
        y_location (int): Object location in the y axis of screen layout.
    """
    def __init__(self):
        self.x_location = 0
        self.y_location = 0
    
class Wall(Element) :
    """
    Inherited class from Element.
    Represents a wall that agent cannot pass.

    Attr:
        x_location (int): Object location in the x axis of screen layout.
        y_location (int): Object location in the y axis of screen layout.
        icon (str): Printed icon. This is set by default as "██" and cannot be changed.
        color (object | None): The color can be set using the custom module "colors". If no color is desired, None can be used.
        sprite (str): Icon that will be printed. String containing the ANSI scape codes  and the object icon.
    """
    def __init__(self, color) :
        super().__init__()
        self.icon = "██"
        self.color = color
        self.sprite = self.gen_sprite()

    def gen_sprite(self) :
        if self.color == None :
            return self.icon
        else :
            return f"{self.color}{self.icon}{colors.Text.end}"
        
    def set_in_screen(self, screen: object, x_location: int, y_location: int) :
        self.y_location = y_location    # Primero se escoge el eje y,
        self.x_location = x_location    # Luego se escoge el eje x.

        screen.layout[y_location][x_location] = self.sprite

class Queue(Element) :
    def __init__(self) :
        super().__init__()
        self.icon = "██"
        self.color = colors.Regular.dark_gray
        self.sprite = self.gen_sprite()

    def gen_sprite(self) :
        if self.color == None :
            return self.icon
        else :
            return f"{self.color}{self.icon}{colors.Text.end}"
        
    def set_in_screen(self, screen: object, x_location: int, y_location: int) :
        self.y_location = y_location    # Primero se escoge el eje y,
        self.x_location = x_location    # Luego se escoge el eje x.

        screen.layout[y_location][x_location] = self.sprite

class Void(Element) :
    def __init__(self) :
        super().__init__()
        self.sprite = "  "
    
    def set_in_screen(self, screen: object, x_location: int, y_location: int) :
        self.y_location = y_location    # Primero se escoge el eje y,
        self.x_location = x_location    # Luego se escoge el eje x.

        screen.layout[y_location][x_location] = self.sprite