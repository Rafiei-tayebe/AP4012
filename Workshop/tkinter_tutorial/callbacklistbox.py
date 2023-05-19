import tkinter as tk

root = tk.Tk()
label = tk.Label(root)
listbox = tk.Listbox(root)
label.pack(side="bottom", fill="x")
listbox.pack(side="top", fill="both", expand=True)

listbox.insert("end", "one", "two", "three", "four", "five", "5", "5", "5", "5", "5", "5", "5", "5", "5", "5", "5", "5")

def callback(event):
    selection = event.widget.curselection()
   
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        label.configure(text=data)
        print("eeeeeeeeeeahmad",data)
    else:
        label.configure(text="")

listbox.bind("<<ListboxSelect>>", callback)

root.mainloop()

