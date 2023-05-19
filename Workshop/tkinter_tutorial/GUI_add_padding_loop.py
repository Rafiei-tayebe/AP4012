import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import *

win = tk.Tk()

win.title('First GUI')


def click_me():
    h = name.get()
    action.config(text='Hello' + ' ' + h + ' ' + number_chosen.get())
    

ttk.Label(win, text='Enter a name:').grid(row=0, column=0,pady= 20)

name = tk.StringVar()
name_entered = ttk.Entry(win, width=12, textvariable=name)
name_entered.grid(column=0, row=1)

action = ttk.Button(win, text="Click Me", command=click_me)
action.grid(column=2, row=1)



ttk.Label(win, text='Choose a number: ').grid(column=1, row=0)
number = tk.StringVar()
number_chosen = ttk.Combobox(win, width=12, textvariable=number, state='readonly')
number_chosen['values'] = (1, 2, 4, 42, 100)
number_chosen.grid(column=1, row=1)
number_chosen.current(0)  #defult miad ro yeki az 5ta maghadire ma bastegi dare az 0 ta 4 kodomo bedim

chVarDis = tk.IntVar()
check1 = tk.Checkbutton(win, text = 'Disabled', variable=chVarDis, state='disabled')  #checkbutton hamoon ja baraye tik zadano inas ke bayad intvaro import konim az tk
check1.select()
check1.grid(column=0, row=4, sticky=tk.W)

chVarUn = tk.IntVar()
check2 = tk.Checkbutton(win, text='Unchecked', variable=chVarUn)
check2.deselect()
check2.grid(column=1, row=4, sticky=tk.W)  #sticky baraye ine ke kojaye safe gharar begire in checkbutton

chVarEn = tk.IntVar()
check3 = tk.Checkbutton(win, text='Enabled', variable=chVarEn)
check3.select()
check3.grid(column=2, row=4, sticky=tk.W)

color = ['Blue','Gold','Red']

def radCall():
    radSel = radVar.get()
    if radSel == 0:
        win.config(bg=color[0])
    elif radSel == 1:
        win.config(bg=color[1])
    elif radSel == 2:
        win.config(bg=color[2])

radVar = tk.IntVar()
radVar.set(51)

for col in range(3):
    curRad = tk.Radiobutton(win, text=color[col], variable=radVar, value=col, command=radCall)  
    curRad.grid(column=col, row=5, sticky=tk.W)
    #radiobutton baraye in daierehas ke toosh mishe tik zad
    


scrol_w = 30
scrol_h = 3
scr = scrolledtext.ScrolledText(win, width=scrol_w, height=scrol_h, wrap=tk.WORD)
scr.grid(column=0,columnspan=3)

# 
button_frame_p = ttk.LabelFrame(win, text='Labels in a Frame')
button_frame_p.grid(row=8, column=0, padx=20, pady=40)

tk.Label(button_frame_p, text='Label1').grid(row=0, column=0)
tk.Label(button_frame_p, text='Label2').grid(row=1, column=0)
tk.Label(button_frame_p, text='Label3').grid(row=2, column=0)
# .winfo_children()
for child in button_frame_p.winfo_children():
    child.grid_configure(padx=8, pady=4)

name_entered.focus() #we can type into this textbox without having to click it first


win.mainloop()
