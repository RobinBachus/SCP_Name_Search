# TODO: fix SCP_Machine class
# TODO: add title to information
# TODO: add author to information

# --- Imports ---
import re
import tkinter as tk
from bs4 import BeautifulSoup
import requests
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
    #try:
    if (e1.get() != "" and int(e1.get()) > 99 and float (e1.get()) == int(e1.get())):
        t1.delete("1.00", "end")
        url = "http://www.scp-wiki.net/scp-{}".format(str(e1.get()))
        print (url)
        # print(url)

        # this takes the url and recives its html file
        t1.insert("end",url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='main-content')
        pageElements = results.find_all('p')
        #machine.getTitle(int(e1.get()))

        for i in pageElements:
            objectClass = re.search("Object Class:</strong> ((.*?))</p>", str(i))
            if objectClass == None:
                continue
            objectClass = str (objectClass.group(1))
            if (re.search("<span style=((.*?));",objectClass)== None):
                print (objectClass)
                objectClass = "\nObject class: {}".format(str(objectClass))
            else:
                objectClass = re.search("</span> ((.*?))</p>", str(i))
                objectClass = str(objectClass.group(1))
                objectClass = "\nObject class: {}".format(str(objectClass))
            t1.insert("end", objectClass)  
        
        pageContent = soup.find(id='page-content')
        rating_Temp = pageContent.find('span', class_='number prw54353')
        rating_Temp = re.search('prw54353">((.*?))</span>', str(rating_Temp))
        if (rating_Temp != None):   
            rating = str(rating_Temp.group(1))
            t1.insert("end", "      Rating: {}".format(rating))
    else:
        t1.delete("1.00", "end")
        t1.insert("end", "Please type a whole number above 99.")
    """ except:
        t1.delete("1.00", "end")
        t1.insert("end", "Please type a whole number above 99.")"""

# --- Main code ---
root = tk.Tk()
tk.Label(root, text="scp-").grid(sticky=tk.W, row=1)

l1 = tk.Label(root,text="Type the number of an scp")
e1 = tk.Entry(root)
t1 = tk.Text(root, height=5, width=52)

l1.grid(row=0, sticky=tk.W)
e1.grid(row=1, columnspan=2, sticky=tk.W, padx=30)
t1.grid(row=2)

tk.Button(root, 
          text='Quit', 
          command=root.quit).grid(row=3, 
                                    column=0, 
                                    sticky=tk.W, 
                                    pady=4)

tk.Button(root, text='Show', command=search).grid(row=0, column=0, sticky=tk.W, rowspan=2, padx= 160)

print(e1.get())

tk.mainloop()