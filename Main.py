#! /usr/bin/env python3

# --- Todo ---
# TODO: add author to information
# TODO: divide search function in multiple function and move those to SCP_Machine Class
# TODO: add comments to code


# --- Imports ---
import re
import tkinter as tk
from tkinter.constants import SUNKEN, WORD

import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk

from SCP_Machine import scp as machine

# --- Variables ---
scp = ""


# --- Functions ---
def show_entry_fields():
    print("scp-%s" % (e1.get()))
    t1.delete("1.0","end")
    t1.insert(tk.END, "scp-")
    t1.insert(tk.END, e1.get())

def search():
    if (e1.get() != "" and int(e1.get()) > 99 and float (e1.get()) == int(e1.get())):
        t1.delete("1.00", "end")
        url = "http://www.scp-wiki.net/scp-{}".format(str(e1.get()))
        print (url)

        # this takes the url and recives its html file
        t1.insert("end","Url: {}".format(url))
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='main-content')

        # Find and insert the title of the scp
        Title = machine.getTitle(int(e1.get()))
        Title = "\n\nTitle: {}\n".format(Title)
        t1.insert("end", Title)

        # Find and insert an image (if any are present)
        global scpImage
        global defaultImg
        pageContent = soup.find(id='page-content')
        scpImage = machine.getImage(pageContent)
        if scpImage != None:
            c1.itemconfig("scp_image", image=scpImage)
        else:
            c1.itemconfig("scp_image", image=defaultImg)

        # Find and insert the object class
            objectClass = machine.getObjectClass(results)
            t1.insert("end", objectClass)  
        
        # Find and insert the rating
        pageContent = soup.find(id='page-content')
        rating_Temp = pageContent.find('span', class_='number prw54353')
        rating_Temp = re.search('prw54353">((.*?))</span>', str(rating_Temp))
        if (rating_Temp != None):   
            rating = str(rating_Temp.group(1))
            t1.insert("end", "\nRating: {}".format(rating))

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
    else:
        t1.delete("1.00", "end")
        t1.insert("end", "Please type a whole number above 99.")


# --- Main code ---
root = tk.Tk()

global defaultImg
defaultImg = Image.open("images/imageMissing.jpg")
defaultImg = defaultImg.resize((round(defaultImg.size[0]*0+160), round(defaultImg.size[1]*0+160)))
defaultImg = ImageTk.PhotoImage(defaultImg)

tk.Label(root, text="scp-").grid(sticky=tk.W, row=1)

l1 = tk.Label(root,text="Type the number of an scp")
e1 = tk.Entry(root)
t1 = tk.Text(root, height=10, width=52,wrap=WORD)
#img1 = tk.Label(root, image=defaultImg,borderwidth=2,relief=SUNKEN,padx=100)
c1 = tk.Canvas(root, width=160,height=160,borderwidth=2,relief=SUNKEN)
img1 = c1.create_image(85, 85, image=defaultImg, tag="scp_image")

l1.grid(row=0, sticky=tk.W)
e1.grid(row=1, columnspan=2, sticky=tk.W, padx=30)
t1.grid(row=2)
c1.grid(row=2,column=3,padx=3,pady=15)

tk.Button(root, text='Quit', command=root.quit).grid(row=3, column=0, sticky=tk.W, pady=4)
tk.Button(root, text='Show', command=search).grid(row=0, column=0, sticky=tk.W, rowspan=2, padx= 160)

print(e1.get())

tk.mainloop()
