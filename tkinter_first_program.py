from tkinter import *
from tkinter import ttk

# this program converts meters to feet, or something

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set((0.3048*value*10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

# make main window, give it a title
root = Tk()
root.title("Feet to Meters")

# create a Frame widget that holds all content, place in root
mainframe = ttk.Frame(root, padding='3 3 12 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# if window resized, frame should expand
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()

# make Entry widget, place in grid, place in cell w/ N,S,E,W
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

# condensed versions of doing same thing as above
# make Label widget, place in grid, place in cell
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
# make Button widget, define text to show, what it should do
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

# create Label widgets, define text to show, where it's placed
ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

# puts padding around all widgets
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# make cursor blink in this field first
feet_entry.focus()
# makes pressing Enter key do same as press Calculate button
root.bind('<Return>', calculate)

# tells Tk to enter event loop, needed to make everything run
root.mainloop()
