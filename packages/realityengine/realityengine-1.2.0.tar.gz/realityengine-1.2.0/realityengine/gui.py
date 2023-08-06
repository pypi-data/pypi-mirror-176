from tkinter import Frame, Label
from realityengine.window import Window


class GUI:
    """
    A class to easliy create GUI elemnts using tkintyer widgets.
    A GUI can contain multiple GUI elements
    """
    def __init__(self, screen: Window, width: int, height: int, x: int = 0, y: int = 0, name: str = None, background: str = "#FFFFFF"):
        self.master = screen

        self.name = name
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.bg = background

        self.frame = Frame(self.master, background=self.bg, width=self.width, height=self.height)
        self.frame.place(x=self.x, y=self.y) 
        
    def set_bg(self, background: str):
        """
        Sets the background of the gui element.
        """
        self.frame.configure(background=background)
        self.bg = background

    def change_position(self, x: int, y: int):
        """
        Sets the position of the GUI element to the specified `x` and `y` cordinates on the screen.
        """
        self.frame.place(x=x, y=y)
        self.x = x
        self.y = y

    def change_dimensions(self, width: int, height: int):
        """
        Sets the width and height of the GUI element to the specified values.
        """
        self.frame.configure(width=width, height=height)
        self.width = width
        self.height = height


class TextLabel:
    """
    Creates a new instance of a TextLabel.\n
    Can contain text.
    """
    def __init__(self, gui: GUI, width: int, height: int, x: int = 0, y: int = 0, name: str = None, text: str = "TextLabel", colour: str = "#000000", background: str = "#FFFFFF"):
        self.master = gui.master
        
        self.name = name
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.text = text
        self.text_colour = colour
        self.bg = background

        self.label = Label(self.master, width=self.width, height=self.height, text=text, foreground=self.text_colour, background=self.bg)
        self.label.place(x=self.x, y=self.y)