import os
import glob
import tkinter
from tkinter import *
from tkinter import filedialog
from PIL import *
from PIL import Image, ImageTk
import tkinter.ttk as ttk


###############
###   GUI   ###
###############
root = Tk() # Creates the main window.
root.title = ("Python Simple Image Viewer") # Sets the window's title.

# Define the size and location of the app's window.
width = 800
height = 500
screen_width = root.winfo_screenwidth() # Gets the screen size.
screen_height = root.winfo_screenheight() # Gets the screen height.
x = (screen_width/2) - (width/2) # Centers the program's window.
y = (screen_height/2) - (height/2) - 100
root.geometry("%dx%d+%d+%d" % (width, height, x, y)) # Set the parameters defined above to the program window.

# Create the content panels.
controlPanel = LabelFrame(root, bg = "gray", fg = "white") # Holds all control buttons.
controlPanel.pack(fill = X, expand = 0)

mainPanel = PanedWindow(root, orient = HORIZONTAL) # Main panel that is split between thumbnails and image viewer.
mainPanel.pack(fill = BOTH, expand = 1)

thumbnailPanel = LabelFrame(mainPanel, text = "Thumbnails", width = 200) # Holds the thumbnails of images in the selected panel.
mainPanel.add(thumbnailPanel)

thumbContainer = LabelFrame(thumbnailPanel, width = 130)
thumbContainer.pack(side = LEFT, fill = Y, expand = 1)

thumbScroll = Scrollbar(thumbnailPanel, orient = VERTICAL, jump = 1)
thumbScroll.pack(side = RIGHT, fill = Y, expand = 0)

imagePanel = LabelFrame(mainPanel, text = "Image") # Holds the image selected amidst the thumbnails.
mainPanel.add(imagePanel)


####################
###   CONTROLS   ###
####################
currentDir = "" # Holds the currently selected directory whose tree will be shown in the explorer.

def OpenDir(): # Funciton to get a directory for the explorer.
  print("--> OpenDir")
  root.dir = filedialog.askdirectory(initialdir = "/", title = "Select Directory to Explore")
  if not root.dir == "":
    currentDir = root.dir
    print(currentDir)
    thumbnailPanel.config(text = currentDir)
    CreateThumbs(root.dir)
  return

buttonOpenDir = Button(controlPanel, text = "Open Directory", command = OpenDir) # Create the 'open directory' button.
buttonOpenDir.grid(row = 0, column = 0, columnspan = 2)


######################
###   THUMBNAILS   ###
######################
imagesFound = []
loaded_images = []
thumbnail_images = []

def CreateThumbs(indir):
  print("--> CreateThumbs")
  directory = indir + "/*.*"
  imagesFound = glob.glob(directory)
  #print(files)
  for child in thumbContainer.winfo_children():
    child.destroy()
  thumbnail_images = []
  loaded_images = []
  index = -1
  for img in imagesFound:
    #print(img)
    index += 1
    print(img)
    try:
      inputimg = Image.open(img)
      loaded_images.append(inputimg)
    except:
      print("failed to read an image: ", img)
      index -= 1
      pass
    try:
      inputimg.thumbnail((128, 128), Image.ANTIALIAS)
    except:
      print("failed to create the thumbnail: ", img)
      index -= 1
      loaded_images.remove(-1)
      pass
    try:
      phimg = ImageTk.PhotoImage(inputimg)
      thumbnail_images.append(phimg)
    except:
      print("failed to convert to PhotoImage: ", img)
      index -= 1
      loaded_images.remove(-1)
      pass
    label = img[img.find("\\")+1:] # Get the image name to be used as a label.
    label_frame = LabelFrame(thumbContainer, height = 128, width = 128, text = label) # Create the labeled frame.
    label_frame.pack()
    img_frame = Button(label_frame, image = thumbnail_images[index]) # Create the image frame within the labeled one.
    img_frame.pack()
  return


##################
###   VIEWER   ###
##################



##########################
###   INITIALIZATION   ###
##########################
if __name__ == '__main__':
  root.mainloop() # Keeps the window open by creating a program loop.
