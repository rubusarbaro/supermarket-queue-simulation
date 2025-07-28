class Label :

    """
    Initialize an object of "label" class. The text containing the label has to be provided as string.
    The available styles are "regular" and "title".
    """

    def __init__(self, text: str, style) :

        # Append the created object to the list.
        #list_labels.append(self)

        self.text = text
        self.related_screen = None
        self.style = style

        self.position_x = 0
        self.position_y = 0

    def regular(self) :
        """
        Text without format, as it was initialized.
        It returns the text in a list of two letters per item.
        """

        # Get the lenght of the text and creates a list where every pair of letter are stored.
        text_len = len(self.text)
        text_as_list = []

        # It iterates a range from 0 to the half of the text length.
        # It uses the half, because it's storing all the letter by pair, not single.
        for i in range(0, text_len//2 ) :
            a = i * 2
            b = a + 1

            string = self.text[a] + self.text[b]
            text_as_list.append(string)

        # It determines if a text lenght is pair or not. If not, it concatenates the last letter to a blank space
        # and append them to the list.
        if text_len//2 != text_len/2 :
            string = self.text[text_len-1] + " "
            text_as_list.append(string)

        return text_as_list
    
    def title(self) :
        """
        Text in title style (uppercase and double space).
        It returns the text in a list of one letter and one space per item.
        """

        # Get the lenght of the text and creates a list where every pair of letter are stored.
        text_len = len(self.text)
        text_as_list = []

        # It iterates a range from 0 to the half of the text length.
        # It uses the half, because it's storing all the letter by pair, not single.
        for i in range(0, text_len) :
           string = self.text[i] + " "
           text_as_list.append(string.upper())

        return text_as_list
    
    def spaced(self) :
        """
        Text in title style (uppercase and double space).
        It returns the text in a list of one letter and one space per item.
        """

        # Get the lenght of the text and creates a list where every pair of letter are stored.
        text_len = len(self.text)
        text_as_list = []

        # It iterates a range from 0 to the half of the text length.
        # It uses the half, because it's storing all the letter by pair, not single.
        for i in range(0, text_len) :
           string = self.text[i] + " "
           text_as_list.append(string)

        return text_as_list

    def set_in_screen(self, screen: object, position_x: int, position_y: int) :

        """
        It adds the text (label) to the assigned screen.
        The target screen, and the position (x and y) of the label has to be provided.
        "screen" is object type. "position_x" and "position_y" are integer type.
        """

        # Store the postion atributes in the object's.
        self.position_x = position_x
        self.position_y = position_y

        # Assigns the declared screen as related_screen to the object
        self.related_screen = screen
        # Defines the "text_as_list" values according to "label.regular" or "label.title"
        text_as_list = self.style(self)

        # Substitutes every item in the list in the target position.
        for i in range(0, len(text_as_list)) :
            screen.layout[self.position_y][self.position_x + i] = text_as_list[i]

        # Adds the current label to a list in the screen, to keep a track of the assigned objects.
        #screen.objects_in_screen.append(self)