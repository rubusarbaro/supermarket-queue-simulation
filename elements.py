###########################################
##  Saúl R. Morales © 2025 MIT License   ##
###########################################
## This module contains simulation objects that agents can interact with.


# Modules to use in this file:
import colors   # Custom module: Allows to modify printed text.

class Border :
    """
    This class provides two styles for app border: "none" (two blank spaces) and "ascii" (two vertical rectangles, "██")
    """
    none = "  "
    ascii = "██"

class Element () :
    """
    Parent class. Represents a physical element in the simulation.

    Attributes:
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

    Args:
        color (object | None): The color can be set using the custom module "colors". If no color is desired, None can be used.
    
    Attributes:
        x_location (int): Object location in the x axis of screen layout.
        y_location (int): Object location in the y axis of screen layout.
        icon (str): Printed icon. This is set by default as "██" and cannot be changed.
        sprite (str): Icon that will be printed. String containing the ANSI scape codes and the object's icon.
    """
    def __init__(self, color) :
        super().__init__()
        self.icon = "██"
        self.color = color
        self.sprite = self.gen_sprite()

    def gen_sprite(self) :
        """
        Generate sprite to use, concatenating ANSI codes to current logo.
        
        Returns:
            sprite (str)
        """

        if self.color == None :
            return self.icon
        else :
            return f"{self.color}{self.icon}{colors.Text.end}"
        
    def set_in_screen(self, screen: object, x_location: int, y_location: int) :
        """
        Add current object to the screen layout. Necessary to import execute this method before printing the screen layout.

        Args:
            screen (object): Screen where this object will be displayed.
            x_location (int): Object location in the x axis of screen layout.
            y_location (int): Object location in the y axis of screen layout.
        """

        self.y_location = y_location    # Primero se escoge el eje y,
        self.x_location = x_location    # Luego se escoge el eje x.

        screen.layout[y_location][x_location] = self.sprite

class Queue(Element) :
    """
    Inherited class from Element.
    Represents a gray tile representing the queue.

    Attributes:
        x_location (int): Object location in the x axis of screen layout.
        y_location (int): Object location in the y axis of screen layout.
        icon (str): Printed icon. This is set by default as "██" and cannot be changed.
        color (object): Default color is dark gray and it cannot be changed.
        sprite (str): Icon that will be printed. String containing the ANSI scape codes and the object's icon.
    """

    def __init__(self) :
        super().__init__()
        self.icon = "██"
        self.color = colors.Regular.dark_gray
        self.sprite = self.gen_sprite()

    def gen_sprite(self) :
        """
        Generate sprite to use, concatenating ANSI codes to current logo.
        
        Returns:
            sprite (str)
        """

        if self.color == None :
            return self.icon
        else :
            return f"{self.color}{self.icon}{colors.Text.end}"
        
    def set_in_screen(self, screen: object, x_location: int, y_location: int) :
        """
        Add current object to the screen layout. Necessary to import execute this method before printing the screen layout.

        Args:
            screen (object): Screen where this object will be displayed.
            x_location (int): Object location in the x axis of screen layout.
            y_location (int): Object location in the y axis of screen layout.
        """

        self.y_location = y_location    # Primero se escoge el eje y,
        self.x_location = x_location    # Luego se escoge el eje x.

        screen.layout[y_location][x_location] = self.sprite

class Void(Element) :
    """
    Inherited class from Element.
    Represents void, the abscence of an element in the screen.

    Attributes:
        x_location (int): Object location in the x axis of screen layout.
        y_location (int): Object location in the y axis of screen layout.
        sprite (str): Two blank spaces "  ". It cannot be changed.
    """

    def __init__(self) :
        super().__init__()
        self.sprite = "  "
    
    def set_in_screen(self, screen: object, x_location: int, y_location: int) :
        """
        Add current object to the screen layout. Necessary to import execute this method before printing the screen layout.

        Args:
            screen (object): Screen where this object will be displayed.
            x_location (int): Object location in the x axis of screen layout.
            y_location (int): Object location in the y axis of screen layout.
        """

        self.y_location = y_location    # Primero se escoge el eje y,
        self.x_location = x_location    # Luego se escoge el eje x.

        screen.layout[y_location][x_location] = self.sprite