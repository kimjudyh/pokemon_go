from tkinter import *
from tkinter import ttk

from multi_poke_v1 import main, file_input, evo_pokemon_input

# this program converts meters to feet, or something

def analyze(*args):
    try:
        file_value = file_chosen.get()
        poke_file=file_input(file_value)
        print("file chosen", file_value)
        print("file: ", poke_file)
        evo_pokemon =  evo_pokemon_input(evo_chosen.get())
        print("evo poke: ", evo_pokemon)
        root.destroy()
        main()
        print('done')
    except ValueError:
        pass

# make main window, give it a title
root = Tk()
root.title("PoGo Batch Analysis")

# create a Frame widget that holds all content, place in root
mainframe = ttk.Frame(root, padding='4 4 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# if window resized, frame should expand
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

evo_chosen = StringVar()
file_chosen = StringVar()

file_entry = ttk.Entry(mainframe, width = 10, textvariable=file_chosen)
file_entry.grid(column=2, row=1, sticky=(W,E))
ttk.Label(mainframe, text="File:").grid(column=1, row=1, sticky=(W,E))

evo_entry = ttk.Combobox(mainframe, width=7, textvariable=evo_chosen)
evo_entry.grid(column=2, row=2, sticky=(W,E))
evo_entry['values'] =('Lanturn', 'Gallade')
ttk.Label(mainframe, text="Evolution:").grid(column=1, row=2, sticky=(W,E))

ttk.Button(mainframe, text="Analyze", command=analyze).grid(column=2, row=3, sticky=(W,E))

# puts padding around all widgets
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# make cursor blink in this field first
file_entry.focus()
# makes pressing Enter key do same as press Calculate button
root.bind('<Return>', analyze)

# tells Tk to enter event loop, needed to make everything run
root.mainloop()
