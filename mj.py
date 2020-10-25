# Importing all the necessary libraries
from tkinter import *
from tkinter import filedialog 
import re
import numpy as np
import matplotlib.pyplot as plt
from tkinter import scrolledtext as st
from nltk.corpus import stopwords 
import subprocess as sp

# Declared global variable fname to store the current file of execution
global fname
fname=""
global fname2
fname2=""

# Reads the iven input file using pythons open function
def read_file_text(file):
    try:
	    dat=open(file,"r") # opens the file 
	    txt=dat.read()
	    return txt
    except FileNotFoundError:
    	print("No File Chosen!!!!")  

# Returns the bin length, frequencies and counts of the unique words in the given input list
def get_frequency(word_list):
    (unique, counts) = np.unique(word_list, return_counts=True)
    frequencies = np.asarray((unique, counts)).T
    bins =set(counts)
    len_bin=len(bins)
    frequencies=sorted(frequencies,key=lambda row: row[1]) # Sorting the frequencies
    frequencies=np.array(frequencies)
    return (len_bin,frequencies,counts)

# Performing splitting into words and removing '.',' ','\n' characters 
def preprocess_text(txt):
    nwln=txt.split("\n")
    split_sent=txt.split(".")
    split_sent=split_sent[:-1]
    sentences=[]
    for i in split_sent:
        k=0
        if i[k]==" ":
            k+=1
        if i[k]=="\n":
            k+=1
        sentences.append(i[k:])
    return (nwln,sentences)

# Lowercasing and Removing the stopwords i.e. the commonly occuring articles preposiitons from the words list
def remove_common_words(txt):
    data=re.sub(r'[^\w\s]', '', txt) 
    data=data.lower()
    data=data.split()
    # Commonly occuring words stored in a dictionary
    ignore=['a','the','if','an','the','for','as','of','or','and','else','from','in','on','over','but','is','am','are','was','were','at','by','to','can','could','should','shall','will','would','be']
    
    mod_data=[]
    for i in data:
        if i not in ignore:
            mod_data.append(i)
    return (mod_data,data)

# Defined driver code for opening the file and do the file processing
def driver(file1):
    txt = read_file_text(file1)  
    print(type(txt))

    # Performing splitting into words and removing '.',' ','\n' characters  
    new_ln,sent = preprocess_text(txt)

    # Lowercasing and Removing the stopwords i.e. the commonly occuring articles preposiitons from the words list
    mod_data,data = remove_common_words(txt)
    word_list = np.array(mod_data)

    # Finding the (word -> frequency) values using the numpy's unique function
    bin1,frequencies,counts = get_frequency(word_list)

   # Storing the values in globalvars so as to be used later for plotting 
    global bin2
    bin2=bin1

    global counts2
    counts2=counts
    
    global sentences3
    sentences3=sent

    return frequencies,str(len(sent)),str(len(new_ln)),str(len(data)),frequencies[-1][0],str(frequencies[-1][-1])

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
        if fname2=="":
            lbl_upload_2.configure(text="No file selected, enter valid text file or enter keywords in textbox.")
            return
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
                                    12),bg='#f2e9e4') 
    t_area.grid(column = 3,row=7, pady = 10, padx = 10,columnspan=5,sticky='w')  
    t_area.insert(INSERT,out)
    t_area.configure(state='disabled')
   
# The Driver code for adding the info onto the widgets
def driver_widget():
    # Gets the corresponding stats from the driver function
    if fname == "":
        lbl.configure(text = "No file selected, please select a valid text file.")
        return

    frequencies,sent_no,nwl_nno,word_no,max_word,max_word_count = driver(fname)
    # Doing the necessary configuration to display
    lbl_sentences.configure(text="No of sentences in file: "+sent_no)
    lbl_newlines.configure(text="No of newlines in file: "+nwl_nno)
    lbl_wcount.configure(text="No of words in file: "+word_no)
    lbl_frequency.configure(text="Word with most frequency in file: '"+max_word)
    lbl_frequency2.configure(text="Its frequency: "+max_word_count)

    # Adding labels to the frame
    lbl_search_label = Label(root,text="Enter the words to search separated by space or",width=50,anchor=W,bg="#c9ada7")
    lbl_search_label.grid(column=4,row=2,columnspan=4)  
    
    # Button to plot the histogram
    hist_plot_btn= Button(root, text = "Plot Histogram" , 
            command=hist_p,width =20,bg="#9a8c98",highlightthickness=2,highlightbackground="white") 
    hist_plot_btn.grid(column=0,row=1,columnspan=2,sticky='w',padx=5)
    edit_btn = Button(root, text = "Edit" ,command=edit_1,width=12,bg="#9a8c98",highlightthickness=2,highlightbackground="white") 
    edit_btn.grid(column=4,row=1,sticky='e')

    # Showing the results of the search onto the Text area
    global text_area
    text_area = Entry(root, width=35,bg='#f2e9e4') 
    text_area.grid(column = 4, row=3,pady = 1, padx = 5,columnspan=3,sticky='w') 
   
    global lbl_upload_2
    # Labels and buttons for uploading and executing the files
    lbl_upload_2 = Label(root, text = "Upload file of keywords separated by space \n(keep input text blank)",width=50,anchor=W,bg="#c9ada7") 
    lbl_upload_2.grid(column=4, row=4,columnspan=5,rowspan=2) 
    up_btn = Button(root, text = "Upload file" , 

            command=browseFiles_search,width=12,bg="#9a8c98",highlightthickness=2,highlightbackground="white") 
    up_btn.grid(column=4,row=6,sticky="e")


    # Placing these onto the screen
    exe_btn =Button(root, text = "Execute" ,command=find1,width=12,bg="#9a8c98",highlightthickness=2,highlightbackground="white") 
    exe_btn.grid(column=5,row=6,sticky="w")
    

   
# Funtion implemented to browse the files using tkinter's filedialog system
def browseFiles_search(): 
    filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("Text files", 
                                                        "*.txt*"), 
                                                       ("all files", 
                                                        "*.*"))) 
    lbl_upload_2.configure(text="File Opened: "+filename+"\n(Keep above input blank)") 
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
root.geometry('750x450')
root['bg']="#c9ada7"
  
# Adding a label to the root window 
lbl = Label(root, text = "Choose a file to run",width=40,anchor=W,borderwidth=1,relief="raised",bg='#f2e9e4') 
lbl.grid(column=0, row=0,columnspan=4,sticky='w',padx=5) 

# Setting up the window for the gui
lbl_sentences = Label(root,width=40,anchor=W,bg="#c9ada7")
lbl_sentences.grid(column=0,row=3,columnspan=4)
lbl_newlines =Label(root,width=40,anchor=W,bg="#c9ada7")
lbl_newlines.grid(column=0,row=6,columnspan=4)
lbl_frequency =Label(root,width=40,anchor=W,bg="#c9ada7")
lbl_frequency.grid(column=0,row=4,columnspan=4)
lbl_frequency2 =Label(root,width=40,anchor=W,bg="#c9ada7")
lbl_frequency2.grid(column=0,row=5,columnspan=4)
lbl_wcount =Label(root,width=40,anchor=W,bg="#c9ada7")
lbl_wcount.grid(column=0,row=2,columnspan=4)



# getting the buttons from tkinter
btn = Button(root, text = "Browse files" , 
            command=browseFiles,width=12,bg="#9a8c98",highlightthickness=2,highlightbackground="white") 
btn2= Button(root, text = "Run" , 

            command=driver_widget,width=12,bg="#9a8c98",highlightthickness=2,highlightbackground="white") 


# Adding them to the grid
btn.columnconfigure(0,weight=1) 
btn.grid(column=4, row=0,padx=2,pady=10,sticky=E)

btn2.grid(column=5,row=0,sticky=W)
# Running the root window 
root.mainloop()
