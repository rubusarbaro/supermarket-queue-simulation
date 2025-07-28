import colors

class Element () :
    def __init__(self):
        self.x_location = 0
        self.y_location = 0
    
class Wall(Element) :
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