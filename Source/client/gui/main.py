from pathlib import Path
from tkinter import Tk
from PIL import ImageTk, Image
from .header import buildHeader
from .body import buildBody

ASSETS_PATH = 'assets/'

import sys
sys.path.insert(1, '/path/to/client/function/')
from function.function import makeClient

def mainWindow(address, port):
    MainWindow(address, port)

class MainWindow():
    """This class generates the GUI""" 

    def __init__(self, address, port):
        self.client = makeClient((address, port))

        self.root = Tk()
        self.width, self.height = self.findDimension()
        self.root.geometry(str(self.width) + 'x' + str(self.height))
        self.root.configure(bg = "#FFFFFF")
        self.root.title('Favorite Place')

        self.header = buildHeader(self)
        self.body = buildBody(self)

        self.root.resizable(False, False)
        self.root.mainloop()

    def findDimension(self):
        """This function finds the dimension for the GUI

        Returns:
            tuple (int, int): Width and height of GUI
        """
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()  
        dimensionList = [[640, 480], [800, 600], [960, 720], [1024, 768], [1280, 960], [1400, 1050], [1440, 1080], [1600, 1200], [1856, 1392], [1920, 1440], [2048, 1536]]
        
        for dimension in reversed(dimensionList):
            if screenWidth > dimension[0] and screenHeight > dimension[1] * 1.1:
                return dimension[0], dimension[1]
        return 0, 0

    def loadImage(self, name):
        """This function loads the assets

        Args:
            name (string): Asset's filename

        Returns:
            PhotoImage: tkinter's image format
        """
        return ImageTk.PhotoImage(Image.open(Path(ASSETS_PATH + name)))
        
