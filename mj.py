# Importing all the necessary libraries
from tkinter import *
from tkinter import filedialog 
import re
import numpy as np
import matplotlib.pyplot as plt
from tkinter import scrolledtext as st
import subprocess as sp
from nltk.corpus import stopwords 

# Declared global variable fname to store the current file of execution
global fname
fname=""

# Defined driver code for opening the file and do the file processing
def driver(file1):
    dat=open(file1,"r") # opens the file 
    txt=dat.read()   

    # Performing splitting into words and removing '.',' ','\n' characters   
    nwln=txt.split("\n")
    sentences=txt.split(".")
    sentences=sentences[:-1]
    sentences2=[]
    for i in sentences:
        k=0
        if i[k]==" ":
            k+=1
        if i[k]=="\n":
            k+=1
        sentences2.append(i[k:])

    # Lowercasing and Removing the stopwords i.e. the commonly occuring articles preposiitons from the words list
    data=re.sub(r'[^\w\s]', '', txt) 
    data=data.lower()
    data=data.split()
    #ignore=['a','the','if','an','the','for','as','of','or','and','else','from','in','on','over','but','is','am','are','was','were','at','by','to','can','could','should','shall','will','would','be']
    #using set of stop words provided by nltk
    ignore=set(stopwords.words('english'))
    data2=[]
    for i in data:
        if i not in ignore:
            data2.append(i)


    number_list = np.array(data2)

    # Finding the (word -> frequency) values using the numpy's unique function
    (unique, counts) = np.unique(number_list, return_counts=True)
    frequencies = np.asarray((unique, counts)).T
    bin1=set(counts)
    bin1=len(bin1)
    frequencies=sorted(frequencies,key=lambda row: row[1]) # Sorting the frequencies
    frequencies=np.array(frequencies)

   # Storing the values in globalvars so as to be used later for plotting 
    global bin2
    bin2=bin1
    global counts2
    counts2=counts
    global sentences3
    sentences3=sentences2
    return frequencies,str(len(sentences2)),str(len(nwln)),str(len(data)),frequencies[-1][0],str(frequencies[-1][-1])

# Function used for plotting the frequency values of words in a histogram
def hist_p():
    plt.hist(counts2,bins=bin2)
    plt.title("Histogram of frequency of words")
    plt.xlabel("no of times word occoured")
    plt.ylabel("frequency")
    plt.show()

# Opens the notepad for editing
def edit_1():
    programName = "notepad.exe"
    sp.Popen([programName, fname])

# Functionality used for finding a particular words occurence in the file
def find1():
    words=text_area.get()
    if words=="":
        dat=open(fname2,"r")
        txt=dat.read()
        words=words.lower()
        words=txt.split()
    else:
        words=words.lower()
        words=words.split()
    out=""
    # Prints the the setences where word is found onto the text box
    for i in words:
        out+="The word '"+i+"' is in the following statements:\n"
        for k in sentences3:
            mn=k.lower()
            mn=re.sub(r'[^\w\s]', '', mn) 
            if i in mn.split():
                out+= k+"\n"
        out+="\n"

    # Adding the necessary widgets
    t_area = st.ScrolledText(root, 
                            width = 50,  
                            height = 8,  
                            font = ("Times New Roman", 
                                    12)) 
    t_area.grid(column = 1,row=6, pady = 10, padx = 10)  
    t_area.insert(INSERT,out)
    t_area.configure(state='disabled')
   
# The Driver code for adding the info onto the widgets
def driver2():
    # Gets the corresponding stats from the driver function
    frequencies,sent_no,nwl_nno,word_no,max_word,max_word_count = driver(fname)
    # Doing the necessary configuration to display
    lbl_sentences.configure(text="No of sentences in file: "+sent_no)
    lbl_newlines.configure(text="No of newlines in file: "+nwl_nno)
    lbl_wcount.configure(text="No of words in file: "+word_no)
    lbl_frequency.configure(text="word with most frequency in file: '"+max_word+"'\nIts frequency: "+max_word_count)
    
    # Adding labels to the frame
    lbl_search_label = Label(root,text="Enter the words to search separated by space or")
    lbl_search_label.grid(column=1,row=2)  
    
    # Button to plot the histogram
    hist_plot_btn= Button(root, text = "Plot Histogram" , 
            command=hist_p) 
    hist_plot_btn.grid(column=0,row=1)
    edit_btn = Button(root, text = "Edit" ,command=edit_1) 
    edit_btn.grid(column=2,row=1)

    # Showing the results of the search onto the Text area
    global text_area
    text_area = Entry(root, width=10) 
    text_area.grid(column = 1, row=3,pady = 1, padx = 5) 
   
    global lbl_upload_2
    # Labels and buttons for uploading and executing the files
    lbl_upload_2 = Label(root, text = "Upload file of keywords separated by space (keep input text blank)") 
    lbl_upload_2.grid(column=1, row=4) 
    up_btn = Button(root, text = "Upload file" , 
            command=browseFiles2) 
    up_btn.grid(column=1,row=5)

    # Placing these onto the screen
    exe_btn =Button(root, text = "Execute" ,command=find1) 
    exe_btn.grid(column=2,row=5)
    

   
# Funtion implemented to browse the files using tkinter's filedialog system
def browseFiles2(): 
    filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("Text files", 
                                                        "*.txt*"), 
                                                       ("all files", 
                                                        "*.*"))) 
    lbl_upload_2.configure(text="(Keep above input blank) File Opened: "+filename) 
    global fname2
    fname2=filename
    
# Funtion implemented to browse the files using tkinter's filedialog system
def browseFiles(): 
    filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("Text files", 
                                                        "*.txt*"), 
                                                       ("all files", 
                                                        "*.*"))) 
    lbl.configure(text="File Opened: "+filename) 
    global fname
    fname=filename
       
root = Tk() 
  
# Root window title and dimension 
root.title("Lap_LAB_3") 
root.geometry('900x700') 
  
# Adding a label to the root window 
lbl = Label(root, text = "Choose a file to run") 
lbl.grid(column=0, row=0) 

# Setting up the window for the gui
lbl_sentences = Label(root)
lbl_sentences.grid(column=0,row=3)
lbl_newlines =Label(root)
lbl_newlines.grid(column=0,row=5)
lbl_frequency =Label(root)
lbl_frequency.grid(column=0,row=4)
lbl_wcount =Label(root)
lbl_wcount.grid(column=0,row=2)



# getting the buttons from tkinter
btn = Button(root, text = "Browse files" , 
            command=browseFiles) 
btn2= Button(root, text = "Run" , 
            command=driver2) 

# Adding them to the grid
btn.grid(column=1, row=0,padx=10,pady=10) 
btn2.grid(column=1,row=1)
# Running the root window 
root.mainloop()
