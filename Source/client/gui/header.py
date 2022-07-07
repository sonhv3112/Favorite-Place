from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk, Label

def buildHeader(main):
    return Header(main)

class Header():
    """This class generates the header of the GUI""" 

    def __init__(self, main):
        self.width = main.width
        self.height = main.height // 10
        root = main.root
        self.main = main

        self.headerFrame = ttk.Frame(root, height=self.height, width=self.width)
        self.headerFrame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.headerFrame.canvas = Canvas(
            self.headerFrame,
            bg = "#FFFFFF",
            height = self.height,
            width = self.width,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.headerFrame.canvas.place(x = 0, y = 0)
        
        """Border"""
        self.headerFrame.canvas.create_line(0, 0, self.width, 0, fill='#EDEEF2', width=2)
        self.headerFrame.canvas.create_line(0, self.height, self.width, self.height, fill='#EDEEF2', width=2)
        
        """Logo"""
        self.headerFrame.canvas.create_text(
            self.width // 20,
            (self.height - self.height / 1.5) / 2,
            anchor="nw",
            text="Favorite",
            fill="#2B2B43",
            font=("Segoe UI Black", 21 * -1),
            tags='homeButton'
        )

        self.headerFrame.canvas.create_text(
            self.width // 20,
            (self.height - self.height / 1.5) / 2 + 21.0,
            anchor="nw",
            text="Place",
            fill="#4E60FF",
            font=("Segoe UI Black", 21 * -1, 'bold'),
            tags='homeButton'
        )

        """Search Bar"""
        self.roundRectangle(
            self.width / 20 * 15, 
            (self.height - self.height / 2) // 2, 
            self.width / 20 * 19.5, 
            self.height - ( self.height - self.height / 2) // 2, 
            r=18, 
            fill="#EDEEF2"
        )

        self.headerFrame.searchBar = Entry(
            bd=0,
            bg="#EDEEF2",
            highlightthickness=0
        )

        self.headerFrame.searchBar.place(
            x=self.width / 20 * 15.2,
            y=(self.height - self.height / 2) // 2 + self.height // 10,
            width=self.width / 20 * 3.5,
            height=26
        )
        
        self.searchButtonImage = self.main.loadImage('button_1.png')

        self.headerFrame.searchButton = Button(
            image=self.searchButtonImage,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: main.body.placeSearch(self.headerFrame.searchBar.get()),
            relief="flat"
        )

        self.headerFrame.searchButton.place(
            x=self.width / 20 * 19.5 - self.width // 30,
            y=(self.height - self.height // 6) // 2,
            width=14,
            height=14
        )

    def roundRectangle(self, x1, y1, x2, y2, r=25, **kwargs): 
        """This function generates a rectangle with rounded corners

        Args:
            x1 (float): Top left x coordinate
            y1 (float): Top left y coordinate
            x2 (float): Bottom right x coordinate
            y2 (float): Bottom right y coordinate
            r (int): Roundness of the rectangle. Defaults to 25.
            **kwargs: tkinter options
        """
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        self.headerFrame.canvas.create_polygon(points, **kwargs, smooth=True)
        
        

