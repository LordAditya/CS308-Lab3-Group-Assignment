# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter
from tkinter import *
from tkinter import filedialog

def browseFunc():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path
    
def writeFile():
    filepath=browseFunc()
    #file = open('sh3rly.txt','a+')
    file=open(filepath,'a+')
    file.write(metinF.get() + '\n')
    file.close()


#create a window
window = Tk()

#set a title
window.title("Lab-3")

#give a heading
label1 = Label(window,text="lab-3 group assignment\n\n")
label1.grid(row=7,column=1)

#instructions for the entry field
label2 = Label(window,text="enter some sentence to be written to the file\n")
label2.grid(row=8,column=1)

#some input text is taken here, which will be written to a file
metinF = Entry(window)
metinF.grid(row=9, column=1)

#clicking this button gives a prompt to choose a file,where the previous text will be written
butonWrite = Button(window)
butonWrite.config(text = 'Choose & Write To File', command = writeFile)
butonWrite.grid(row=10, column=1)

#size of the window
window.geometry("500x200")

#run the loop until stopped externally
window.mainloop()


