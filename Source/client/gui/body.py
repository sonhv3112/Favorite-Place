from tkinter import *
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk, filedialog, messagebox
from PIL import ImageTk, Image

def buildBody(main):
    return Body(main)
      
class Body():
    """This class generates the body of the GUI""" 

    def __init__(self, main):
        self.width = main.width
        self.height = main.height - main.height // 10
        root = main.root
        self.client = main.client
        self.main = main

        self.bodyFrame = ttk.Frame(root, height=self.height, width=self.width)
        self.bodyFrame.grid(column=0, row=1, sticky=(N, W, E, S))
        self.bodyFrame.canvas = Canvas(
            self.bodyFrame,
            bg = "#FFFFFF",
            height = self.height,
            width = self.width,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.bodyFrame.canvas.place(x = 0, y = 0)
        
        self.generateNavigation()
        self.image_file = {}
        self.bodyFrame.button = {}
        
        self.allInfo = self.client.request_all_information()
        self.info = self.allInfo

        thumbnailSize = (self.height - self.height // 10) / 2 - 10
        x = self.width // 12 
        y = (self.height - thumbnailSize * 2) // 3
        self.frameInfo = [[thumbnailSize, x, y], [thumbnailSize, 2 * x + thumbnailSize, y], [thumbnailSize, self.width // 12, 2 * y + thumbnailSize], [thumbnailSize, 2 * x  + thumbnailSize, 2 * y + thumbnailSize]]
        
        self.numPage = len(self.info) // 4 + (len( self.info) % 4 != 0)
        self.curPage = 0
        self.generateMainPage()

    """Main Page"""
    def generateMainPage(self):
        """This function generates the main page of the GUI's body"""
        self.clearThumbnailCard()
        if (len(self.info) == 0):
            self.generateNoResult()
            return
        
        for id in range(4):
            if self.curPage * 4 + id >= len(self.info):
                break
            self.generateThumbnailCard(id)

    def generateThumbnailCard(self, id):  
        """This function generates a thumbnail card for one place

        Args:
            id (int): Position container's id
        """
        size = self.frameInfo[id][0]
        x = self.frameInfo[id][1]
        y = self.frameInfo[id][2]
        info = self.info[self.curPage * 4 + id]
        imageWidth = int(size)
        imageHeight = imageWidth // 4 * 3
        
        """Thumbnail Card Image"""
        self.image_file[id] = ImageTk.PhotoImage(self.client.request_avatar(info['id'], (imageWidth, imageHeight)))
        self.bodyFrame.button[id] = Button(
            image=self.image_file[id],
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.generateDetailsPage(self.curPage * 4 + id),
            relief="flat"
        )
        self.bodyFrame.button[id].place(
            x=x,
            y=y + self.height // 9,
            width=imageWidth,
            height=imageHeight,
            anchor='nw'
        )

        """Thumbnail Card Info"""
        infoPosition = [[x + size // 20, y + imageHeight + size // 20], [x + size - size // 20 * 6, y + imageHeight + size // 20], [x + size // 20, y + imageHeight + size // 20 * 3]]
        self.bodyFrame.canvas.create_text(
            infoPosition[0][0],
            infoPosition[0][1],
            anchor="nw",
            text=info['name'],
            fill="#2B2B43",
            font=("Arial", 14 * -1, 'bold')
        )

        self.bodyFrame.canvas.create_text(
            infoPosition[1][0],
            infoPosition[1][1],
            anchor="nw",
            text="ID: " + info['id'],
            fill="#2B2B43",
            font=("Arial", 14 * -1, 'bold')
        )

        self.bodyFrame.canvas.create_text(
            infoPosition[2][0],
            infoPosition[2][1],
            anchor="nw",
            text="Location: (" + info['longitude'] + ', ' + info['latitude'] + ")",
            fill="#2B2B43",
            font=("Arial", 14 * -1)
        )

        """Thumbnail Card Border"""
        borderPosition = [[x, y, x, y + size], [x, y, x + size, y], [x, y + size, x + size, y + size], [x + size, y, x + size, y + size]]

        for border in borderPosition:
            self.bodyFrame.canvas.create_line(
                border[0], 
                border[1], 
                border[2], 
                border[3], 
                fill = '#EDEEF2',
                width = 2
            )

    def generateNavigation(self):
        """This function generates the main page's navigation'"""
        self.main.header.headerFrame.canvas.tag_bind('homeButton', '<Button-1>',  lambda e: self.placeSearch(''))
        self.upArrowButtonImage = self.main.loadImage('button_2.png')

        self.bodyFrame.upArrowButton = Button(
            image=self.upArrowButtonImage,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.navigateMainPage(-1),
            relief="flat"
        )

        self.bodyFrame.upArrowButton.place(
            x = self.width // 12 * 10.5,
            y = self.height // 12 * 5.5,
            width=40,
            height=40
        )

        self.downArrowButtonImage = self.main.loadImage('button_3.png')

        self.bodyFrame.downArrowButton = Button(
            image=self.downArrowButtonImage,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.navigateMainPage(1),
            relief="flat"
        )

        self.bodyFrame.downArrowButton.place(
            x = self.width // 12 * 10.5,
            y = self.height // 12 * 7.5,
            width=40,
            height=40
        )

    def generateNoResult(self):
        """This function generates 'No result' text"""
        self.bodyFrame.canvas.create_text(
            (self.width - self.width // 10) // 2,
            self.height // 2,
            anchor="center",
            text='No result',
            fill="#2B2B43",
            font=("Segoe UI", 18 * -1, 'bold')
        )
    
    def clearThumbnailCard(self):
        """This function clears all the thumbnail cards in the main page"""
        self.bodyFrame.canvas.delete('all')
        for i in self.bodyFrame.button:
            self.bodyFrame.button[i].destroy()
    
    def clearNavigation(self):
        """This function clears the main page's navigation"""
        self.bodyFrame.upArrowButton.destroy()
        self.bodyFrame.downArrowButton.destroy()
        self.main.header.headerFrame.canvas.tag_unbind('homeButton', '<Button-1>')

    def navigateMainPage(self, value):
        """This function helps to navigate the main page
        
        Args:
            value (int): Navigation's value. 1 for up, -1 for down.
        """
        if self.curPage + value >= self.numPage or self.curPage + value < 0:
           return
                
        self.curPage += value
        self.generateMainPage()
    
    def placeSearch(self, value):
        """This function searchs for place, currently supports place's ID and place's name search. 
        
        Args:
            value (string): Input keyword.
        """
        if value == '':
            self.info = self.allInfo
        else:
            self.info = []
            for place in self.allInfo:
                if str.lower(place['name']) ==  str.lower(value) or  str.lower(place['id']) == str.lower(value):
                    self.info.append(place)

        self.numPage = len(self.info) // 4 + (len(self.info) % 4 != 0)
        self.curPage = 0
        self.generateMainPage()

    """Details Page"""
    def generateDetailsPage(self, id):
        """This function generates the details page for one place

        Args:
            id (int): Place's ID
        """
        self.main.header.headerFrame.searchBar.delete(0, len(self.main.header.headerFrame.searchBar.get()))
        self.main.header.headerFrame.searchBar.config(state='disabled')
        self.main.header.headerFrame.searchButton.config(state='disabled')
        self.clearThumbnailCard()
        self.clearNavigation()

        """Thumbnail Image"""
        info = self.info[id]
        self.thumbnailWidth = int(self.width // 3)
        self.thumbnailHeight = self.thumbnailWidth // 4 * 3 
        self.thumbnailImage = ImageTk.PhotoImage(self.client.request_avatar(info['id'], (self.thumbnailWidth, self.thumbnailHeight)))
        self.thumbnail = self.bodyFrame.canvas.create_image(
            self.width // 20,
            self.height // 20,
            image=self.thumbnailImage,
            anchor='nw'
        )
        self.bodyFrame.canvas.tag_bind(self.thumbnail, '<Button-1>', lambda e: self.generateZoomInPage(info['id'], -1))
        infoPosition = [[self.width // 20 * 2 + self.thumbnailWidth, self.height // 20], [self.width // 20 * 2 + self.thumbnailWidth, self.height // 20 * 2], [self.width // 20 * 2 + self.thumbnailWidth, self.height // 20 * 3], [self.width // 20 * 2 + self.thumbnailWidth, self.height // 20 * 4]]
        self.bodyFrame.canvas.create_text(
            infoPosition[0][0],
            infoPosition[0][1],
            anchor="nw",
            text='ID: ' + info['id'],
            fill="#2B2B43",
            font=("Segoe UI", 18 * -1, 'bold'),
            width=self.width // 12 * 10 - infoPosition[0][0]
        )

        """Details Info"""
        self.bodyFrame.canvas.create_text(
            infoPosition[1][0],
            infoPosition[1][1],
            anchor="nw",
            text='Name: ' + info['name'],
            fill="#2B2B43",
            font=("Segoe UI", 18 * -1, 'bold'),
            width=self.width // 12 * 10 - infoPosition[1][0]
        )
        self.bodyFrame.canvas.create_text(
            infoPosition[2][0],
            infoPosition[2][1],
            anchor="nw",
            text="Location: (" + info['longitude'] + ', ' + info['latitude'] + ")",
            fill="#2B2B43",
            font=("Segoe UI", 14 * -1),
            width=self.width // 12 * 10 - infoPosition[2][0]
        )

        self.bodyFrame.canvas.create_text(
            infoPosition[3][0],
            infoPosition[3][1],
            anchor="nw",
            text='Description: ' + info['description'],
            fill="#2B2B43",
            font=("Segoe UI", 14 * -1),
            width=self.width // 12 * 10 - infoPosition[3][0]
        )

        """Other Images"""
        self.bodyFrame.canvas.create_text(
            self.width // 20,
            self.height // 20 * 3 + self.thumbnailHeight,
            anchor="nw",
            text='More image:',
            fill="#4E60FF",
            font=("Segoe UI", 16 * -1, 'bold')
        )
        self.imageWidth = self.width // 5
        self.imageHeight = self.imageWidth // 4 * 3
        self.imgList = self.client.request_detail_image(info['id'], (self.imageWidth, self.imageHeight))
        self.imgList = [ImageTk.PhotoImage(image) for image in self.imgList]
        self.img = {}
        self.numImg = len(self.imgList) // 4 + (len(self.imgList) % 4 != 0)
        self.curImg = 0
        self.generateOtherImageList(info['id'])

        """Button"""
        self.backButtonImage = self.main.loadImage('button_4.png')

        self.bodyFrame.backButton = Button(
            image=self.backButtonImage,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.redirectMain(),
            relief="flat"
        )

        self.bodyFrame.backButton.place(
            x = self.width // 12 * 10.5,
            y = self.height // 12 * 2,
            width=40,
            height=40
        )
        
        self.leftArrowButtonImage = self.main.loadImage('button_5.png')

        self.bodyFrame.leftArrowButton = Button(
            image=self.leftArrowButtonImage,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.navigateOtherImageList(-1, info['id']),
            relief="flat"
        )

        self.bodyFrame.leftArrowButton.place(
            x = self.width // 20 * 8,
            y = self.height // 20 * 8 + self.thumbnailHeight + self.imageHeight,
            width=40,
            height=40
        )

        self.rightArrowButtonImage = self.main.loadImage('button_6.png')

        self.bodyFrame.rightArrowButton = Button(
            image=self.rightArrowButtonImage,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.navigateOtherImageList(1, info['id']),
            relief="flat"
        )

        self.bodyFrame.rightArrowButton.place(
            x = self.width // 20 * 11,
            y = self.height // 20 * 8 + self.thumbnailHeight + self.imageHeight,
            width=40,
            height=40
        )
        
        self.downloadButtonImage = self.main.loadImage('button_7.png')
        self.bodyFrame.downloadAllButton = Button(
            image=self.downloadButtonImage,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.saveAllImage(info['id']),
            relief='flat',
            bg='white'
        )
        self.bodyFrame.downloadAllButton.place(
            x = self.width // 20,
            y = self.height // 20 * 11.2,
            width=50,
            height=50
        )
        self.bodyFrame.canvas.create_text(
            self.width // 20 + 55,
            self.height // 20 * 9.3,
            anchor="nw",
            text='Download all image',
            fill="#000",
            font=("Segoe UI", 16 * -1, 'bold'),
            tags='textSaveAll'
        )
        self.bodyFrame.canvas.tag_bind('textSaveAll', '<Button-1>', lambda e: self.saveAllImage(info['id']))
    
    def generateOtherImageList(self, id_place):
        """This function generates other images of one place

        Args:
            id_place (int): Place's ID
        """
        self.bodyFrame.canvas.delete('otherImage')
        
        for id in range(4):
            if self.curImg * 4 + id >= len(self.imgList):
                break
            self.img[id] = self.bodyFrame.canvas.create_image(
                self.width // 20 + id * (self.imageWidth + self.width // 40),
                self.height // 20 * 5 + self.thumbnailHeight,
                image=self.imgList[self.curImg * 4 + id],
                anchor='nw',
                tags='otherImage'
            )

        if (self.curImg * 4 < len(self.imgList)): 
            self.bodyFrame.canvas.tag_bind(self.img[0], '<Button-1>', lambda e: self.generateZoomInPage(id_place, self.curImg * 4))

        if (self.curImg * 4 + 1 < len(self.imgList)): 
            self.bodyFrame.canvas.tag_bind(self.img[1], '<Button-1>', lambda e: self.generateZoomInPage(id_place, self.curImg * 4 + 1))

        if (self.curImg * 4 + 2 < len(self.imgList)): 
            self.bodyFrame.canvas.tag_bind(self.img[2], '<Button-1>', lambda e: self.generateZoomInPage(id_place, self.curImg * 4 + 2))

        if (self.curImg * 4 + 3 < len(self.imgList)): 
            self.bodyFrame.canvas.tag_bind(self.img[3], '<Button-1>', lambda e: self.generateZoomInPage(id_place, self.curImg * 4 + 3))

    def clearDetailsPage(self):
        """This function clears the details page"""
        self.bodyFrame.backButton.destroy()
        self.bodyFrame.leftArrowButton.destroy()
        self.bodyFrame.downloadAllButton.destroy()
        self.bodyFrame.rightArrowButton.destroy()

    def navigateOtherImageList(self, value, id_place):
        """This function helps to navigate list of other images

        Args:
            value (int): Navigation's value. 1 for right, -1 for left.
            id_place (int): Place's ID
        """
        if self.curImg + value >= self.numImg or self.curImg + value < 0:
           return

        self.curImg += value
        self.generateOtherImageList(id_place)

    def saveAllImage(self, id_place): 
        """This function saves all images from a place

        Args:
            id_place (int): Place's ID
        """
        directory = filedialog.askdirectory(title='Select the directory')
        if (len(directory) == 0): 
            return 
        avatar = self.client.request_avatar(id_place) 
        avatar.save(f'{directory}/{id_place}_avatar.jpg')
        list_img = self.client.request_detail_image(id_place)
        for i in range(len(list_img)): 
            list_img[i].save(f'{directory}/{id_place}_{i}.jpg')
        messagebox.showinfo("Save All Image","Saved successfully")
        
    def redirectMain(self):
        """This function redirects from details page to main page"""
        self.clearDetailsPage()
        self.main.header.headerFrame.searchBar.config(state='normal')
        self.main.header.headerFrame.searchButton.config(state='normal')
        self.generateNavigation()
        self.generateMainPage()

    """Zoom In Page"""
    def generateZoomInPage(self, id_place, id_img):    
        """This function generates zoom in page for one image

        Args:
            id_place (int): Place's ID
            id_img (int): Image's ID
        """
        if (id_img == -1): 
            PILImage = self.client.request_avatar(id_place, (int(self.width / 1.2), int(self.width / 1.2 / 4 * 3)))
        else: 
            PILImage = self.client.request_one_detail_image(id_place, id_img, (int(self.width / 1.2), int(self.width / 1.2 / 4 * 3)))

        self.bodyFrame.leftArrowButton.place_forget()
        self.bodyFrame.rightArrowButton.place_forget()
        self.bodyFrame.backButton.place_forget()
        self.bodyFrame.downloadAllButton.place_forget()
        self.bodyFrame.generateZoomInPageCanvas = Canvas( 
            self.bodyFrame,
            bg = 'white',
            height = self.height,
            width = self.width,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.bodyFrame.generateZoomInPageCanvas.place(x = 0, y = 0)

        self.bodyFrame.backButtonZoom = Button(
            image=self.backButtonImage,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.redirectDetailsPage(),
            relief='flat'
        )
        self.bodyFrame.backButtonZoom.place(
            x = self.width // 20 - 30,
            y = self.height // 12 * 1.5, 
            width = 40, 
            height = 40
        )

        self.bodyFrame.downloadButton = Button(
            image=self.downloadButtonImage,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.saveImage(id_place, id_img),
            relief='flat',
            bg='white'
        )
        self.bodyFrame.downloadButton.place(
            x = self.width - self.width // 20 - 10,
            y = self.height // 12 * 1.5, 
            width = 40, 
            height = 40
        )

        self.downloadImage = ImageTk.PhotoImage(PILImage)
        self.bodyFrame.generateZoomInPageCanvas.create_image(
            self.width/2, 
            self.height/2,
            anchor='center', 
            image=self.downloadImage
        )

    def saveImage(self, id_place, id_img): 
        """This function saves image from a place

        Args:
            id_place (int): Place's ID
            id_img (int): Image's ID. -1 for thumbail image.
        """
        if (id_img == -1): 
            PILImage = self.client.request_avatar(id_place)
        else: 
            PILImage = self.client.request_one_detail_image(id_place, id_img)
        filename = filedialog.asksaveasfilename(
            defaultextension='.jpg', 
            initialdir = "/",
            title = "Select file",
            filetypes = (("jpeg files","*.jpg"),("all files","*.*"))
        )
        if (filename != ''):
            PILImage.save(filename)
            messagebox.showinfo("Save Image","Saved successfully")

    def redirectDetailsPage(self): 
        """This function redirects from zoom in page to details page"""
        self.bodyFrame.backButtonZoom.destroy()
        self.bodyFrame.downloadButton.destroy()
        self.bodyFrame.generateZoomInPageCanvas.destroy()
        self.bodyFrame.leftArrowButton.place(
            x = self.width // 20 * 8,
            y = self.height // 20 * 8 + self.thumbnailHeight + self.imageHeight,
            width=40,
            height=40
        )
        self.bodyFrame.rightArrowButton.place(
            x = self.width // 20 * 11,
            y = self.height // 20 * 8 + self.thumbnailHeight + self.imageHeight,
            width=40,
            height=40
        )
        self.bodyFrame.backButton.place(
            x = self.width // 12 * 10.5,
            y = self.height // 12 * 2,
            width=40,
            height=40
        )
        self.bodyFrame.downloadAllButton.place(
            x = self.width // 20,
            y = self.height // 20 * 11.2,
            width=50,
            height=50
        )