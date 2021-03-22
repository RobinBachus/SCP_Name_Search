#! /usr/bin/env python3

# --- Todo ---
# TODO: add author to information
# TODO: divide search function in multiple function and move those to SCP_Machine Class
# TODO: add comments to code


# --- Imports ---
import re
import tkinter as tk
from tkinter.constants import END, SUNKEN, WORD
import time

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk

from SCP_Machine import scp as machine

# --- Variables ---
scp = ""
imageIndex = 1
imageAmount = 1

# --- Functions ---
def show_entry_fields():
    print("scp-%s" % (e1.get()))
    t1.delete("1.0","end")
    t1.insert(tk.END, "scp-")
    t1.insert(tk.END, e1.get())

def imageButtonPrevious(event=None):
    global imageIndex
    global scpImage
    global defaultImg
    if (imageIndex > 1):
        imageIndex = imageIndex - 1
        scpImage = machine.getImage(imageIndex)
        if scpImage != None:
            c1.itemconfig("scp_image", image=scpImage)
        else:
            c1.itemconfig("scp_image", image=defaultImg)

        l2_Text.set("{}/{}".format(imageIndex,imageAmount))
        
def imageButtonNext(event=None):
    global imageIndex
    global scpImage
    global defaultImg
    if (imageIndex < imageAmount):
        imageIndex = imageIndex + 1
        scpImage = machine.getImage(imageIndex)
        if scpImage != None:
            c1.itemconfig("scp_image", image=scpImage)
        else:
            c1.itemconfig("scp_image", image=defaultImg)

        l2_Text.set("{}/{}".format(imageIndex,imageAmount))
        

def search(event=None):
    if (e1.get() != "" and int(e1.get()) > 99 and float (e1.get()) == int(e1.get())):
        startTime = time.time()
        t1.delete("1.00", "end")
        url = "http://www.scp-wiki.net/scp-{}".format(str(e1.get()))
        
        print("\n------------- scp-{} -------------".format(e1.get()))
        print (url)

        # this takes the url and recives its html file
        try:
            page = requests.get(url)
        except requests.exceptions.ConnectionError:
            t1.insert(END,"Connection error: \nplease check your internet connection and try again")
            return
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='main-content')
        t1.insert("end","Url: {}".format(url))

        pageContent = soup.find(id='page-content')
        pageElements = results.find_all('p')

        # Find and insert the title of the scp
        Title = machine.getTitle(int(e1.get()))
        Title = "\n\nTitle: {}\n".format(Title)
        t1.insert("end", Title)

        # Find and insert images (if any are present)
        global scpImage
        global defaultImg
        global imageIndex
        global imageAmount
        imageIndex = 1
        imageAmount = machine.DownloadImages(pageContent)
        l2_Text.set("{}/{}".format(imageIndex,imageAmount))
        scpImage = machine.getImage(imageIndex)
        if scpImage != None:
            c1.itemconfig("scp_image", image=scpImage)
        else:
            c1.itemconfig("scp_image", image=defaultImg)

        # Find and insert the object class
        objectClass = machine.getObjectClass(pageElements)
        t1.insert(END, str(objectClass))  

        # Find and insert the rating
        ratingTemp = machine.getRating(pageContent) 
        if (ratingTemp != None):  
            rating = str(ratingTemp.group(1))
            print("Rating: {}".format(rating)) 
            t1.insert("end", "\nRating: {}".format(rating))
        else:
            print("Rating not found")

        # Find and insert the tags
        page_tags = results.find_all('div', class_='page-tags')
        for page_tags in page_tags:
                    Tags = page_tags.find_all('a')
                    if None in Tags:
                        continue
                    list(Tags)

                    # getting the tag name from the element
                    t1.insert("end", "\n\ntags: ")
                    for i in Tags:
                        var = str(i)
                        pattern = ">((.*?))<"
                        var = re.search(pattern, var)

                        var_tag = str(var.group(1))
                        # print(var_tag)
                        
                        t1.insert("end", "{}, ".format(var_tag))
                    t1.delete("end-3c","end")
        t1.insert("end", "\n\nsearch time: {}".format(round(time.time()-startTime, 2)))
        print("------------- /scp-{} -------------\n".format(e1.get()))
    else:
        t1.delete("1.00", "end")
        t1.insert("end", "Please type a whole number above 99.")


# --- Main code ---
root = tk.Tk()

root.bind('<Return>', search)

# the commented code binds the left and right arrow key to the image controll buttons.
# This works but it also means the image changes if you move the cursor with the arrow keys.

# root.bind('<Left>', imageButtonPrevious) 
# root.bind('<Right>', imageButtonNext)    


global defaultImg
defaultImg = Image.open("images/imageMissing.jpg")
defaultImg = defaultImg.resize((round(defaultImg.size[0]*0+160), round(defaultImg.size[1]*0+160)))
defaultImg = ImageTk.PhotoImage(defaultImg)

l2_Text = tk.StringVar()

tk.Label(root, text="scp-").grid(sticky=tk.W, row=1)

l1 = tk.Label(root,text="Type the number of an scp")
l2 = tk.Label(root, textvariable=l2_Text)
e1 = tk.Entry(root)
t1 = tk.Text(root, height=10, width=52,wrap=WORD)
c1 = tk.Canvas(root, width=160,height=160,borderwidth=2,relief=SUNKEN)
img1 = c1.create_image(85, 85, image=defaultImg, tag="scp_image")

l1.grid(row=0, sticky=tk.W)
l2.grid(row=3, column=3)
e1.grid(row=1, columnspan=2, sticky=tk.W, padx=30)
t1.grid(row=2)
c1.grid(row=2,column=3)

tk.Button(root, text='Quit', command=root.quit).grid(row=3, column=0, sticky=tk.W, pady=4)
tk.Button(root, text='Show', command=search).grid(row=0, column=0, sticky=tk.W, rowspan=2, padx= 160)
tk.Button(root, text='Next', command=imageButtonNext).grid(row=3, column=3, sticky=tk.E, padx=(0,10))
tk.Button(root, text='Previous', command=imageButtonPrevious).grid(row=3, column=3, sticky=tk.W, padx=5)

tk.mainloop()
