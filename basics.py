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
    #file_path = askopenfilename()
    return file_path
    
def writeFile():
    filepath=browseFunc()
    #file = open('sh3rly.txt','a+')
    file=open(filepath,'a+')
    file.write(metinF.get() + '\n')
    file.close()






window = Tk()
window.title("Lab-3")
#txt = browseFunc()
metinF = Entry(window)
metinF.grid(row=9, column=1)

butonWrite = Button(window)
butonWrite.config(text = 'Write To File', command = writeFile)
butonWrite.grid(row=8, column=1)

#label = Label(window,text="lab-3 group assignment").pack()
#label = tkinter.Label(window,text=txt).pack()
#bt = Button(window,text="Browse",command=browseFunc).pack()

window.mainloop()


