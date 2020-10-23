import PySimpleGUI as sg
import pathlib
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess as sp

#sg.ChangeLookAndFeel('BrownBlue') # change style
sg.theme('dark grey 9')
#sg.change_look_and_feel('Black')

def make_win1():
    WIN_W = 90
    WIN_H = 25
    file = None

    menu_layout = [['File', ['New (Ctrl+N)', 'Open (Ctrl+O)', 'Save (Ctrl+S)', 'Save As', '---', 'Exit']],
                  ['Tools', ['Word Count', 'Do Analysis','Plot It!']],
                  ['Help', ['About']]]

    layout = [[sg.Menu(menu_layout)],
              [sg.Text('> New file <', font=('Consolas', 10), size=(WIN_W, 1), key='_INFO_')],
              [sg.Multiline(font=('Consolas', 12), size=(WIN_W, WIN_H), key='_BODY_')]]

    window = sg.Window('Notepad', layout=layout, margins=(0, 0), resizable=True, return_keyboard_events=True, finalize=True)
    window.maximize()
    window['_BODY_'].expand(expand_x=True, expand_y=True)
    return window

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def make_win2():
    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    fig.add_subplot(111).hist(counts2,bins=bin2)

    layout = [[sg.Text('Plot test')],
          [sg.Canvas(key='-CANVAS-')]]

    # create the form and show it without the plot
    window = sg.Window('Word Freq Plot', layout, finalize=True, element_justification='center', font='Helvetica 18')
    fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    return window


window1, window2 = make_win1(), None
file = ""


def driver(file):
    dat=open(file,"r")
    txt=dat.read()
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

    data=re.sub(r'[^\w\s]', '', txt) 
    data=data.lower()
    data=data.split()
    ignore=['a','the','if','an','the','for','as','of','or','and','else','from','in','on','over','but','is','am','are','was','were','at','by','to','can','could','should','shall','will','would','be']
    data2=[]
    for i in data:
        if i not in ignore:
            data2.append(i)


    number_list = np.array(data2)

    (unique, counts) = np.unique(number_list, return_counts=True)
    frequencies = np.asarray((unique, counts)).T
    bin1=set(counts)
    bin1=len(bin1)
    frequencies=sorted(frequencies,key=lambda row: row[1])
    frequencies=np.array(frequencies)

   
    global bin2
    bin2=bin1
    global counts2
    counts2=counts
    global sentences3
    sentences3=sentences2
    return frequencies,str(len(sentences2)),str(len(nwln)),str(len(data)),frequencies[-1][0],str(frequencies[-1][-1])
'''
def find1():
    #words=text_area.get()
    words = values['_BODY_']
    if words=="":
        dat=open(fname2,"r")
        txt=dat.read()
        words=words.lower()
        words=txt.split()
    else:
        words=words.lower()
        words=words.split()
    out=""
    for i in words:
        out+="The word '"+i+"' is in the following statements:\n"
        for k in sentences3:
            mn=k.lower()
            mn=re.sub(r'[^\w\s]', '', mn) 
            if i in mn.split():
                out+= k+"\n"
        out+="\n"

    t_area = st.ScrolledText(root, 
                            width = 50,  
                            height = 8,  
                            font = ("Times New Roman", 
                                    12)) 
  
    t_area.grid(column = 1,row=6, pady = 10, padx = 10)  
    t_area.insert(INSERT,out)
    t_area.configure(state='disabled')
'''

def driver_text():
    frequencies,sent_no,nwl_nno,word_no,max_word,max_word_count = driver(file)
    text = ""
    text += ("No of sentences in file: "+str(sent_no)+"\n")
    text += ("No of newlines in file: "+str(nwl_nno)+"\n")
    text += ("No of words in file: "+word_no+"\n")
    text += ("Word with most frequency in file: '"+max_word+"'\nIts frequency: "+max_word_count+"\n")
    return text

 

def new_file():
    '''Reset body and info bar, and clear filename variable'''
    window['_BODY_'].update(value='')
    window['_INFO_'].update(value='> New File <')
    file = None
    return file

def open_file():
    '''Open file and update the infobar'''
    global file
    filename = sg.popup_get_file('Open', no_window=True)
    print(filename)
    if filename:
        file = pathlib.Path(filename)
        print(file)
        window['_BODY_'].update(value=file.read_text())
        window['_INFO_'].update(value=file.absolute())
        return file

def save_file(file):
    '''Save file instantly if already open; otherwise use `save-as` popup'''
    if file:
        file.write_text(values.get('_BODY_'))
    else:
        save_file_as()

def save_file_as():
    '''Save new file or save existing file with another name'''
    filename = sg.popup_get_file('Save As', save_as=True, no_window=True)
    if filename:
        file = pathlib.Path(filename)
        file.write_text(values.get('_BODY_'))
        window['_INFO_'].update(value=file.absolute())
        return file

def word_count():
    '''Display estimated word count'''
    words = [w for w in values['_BODY_'].split(' ') if w!='\n']
    word_count = len(words)
    sg.popup_no_wait('Word Count: {:,d}'.format(word_count))

def do_analysis():
    text = driver_text()
    sg.popup_no_wait(text)


def about_me():
    '''A short, pithy quote'''
    sg.popup_no_wait('"All great things have small beginnings" - Peter Senge')

while True:             # Event Loop
    window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED or event == 'Exit':
        window.close()
        if window == window2:       # if closing win 2, mark as closed
            window2 = None
        elif window == window1:     # if closing win 1, exit program
            break
    elif event in ('Plot It!') and not window2:
        window2 = make_win2()
    elif event == '-IN-':
        window['-OUTPUT-'].update(f'You enetered {values["-IN-"]}')
    elif event == 'Erase':
        window['-OUTPUT-'].update('')
        window['-IN-'].update('')
    elif event in ('New (Ctrl+N)', 'n:78'):
        file = new_file()
    elif event in ('Open (Ctrl+O)', 'o:79'):
        file = open_file()
    elif event in ('Save (Ctrl+S)', 's:83'):
        save_file(file)
    elif event in ('Save As',):
        file = save_file_as()   
    elif event in ('Word Count',):
        word_count()
    elif event in ('Do Analysis',) :
        do_analysis()
    elif event in ('About',):
        about_me()
window.close()