from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import psycopg2

from multi_poke_v1 import main, file_input, evo_pokemon_input


def db_search():
    # search for pokemon names that match search string
    # create connection to database
    db = psycopg2.connect(database = 'mydb')
    cur = db.cursor()

    search_value = search_chosen.get()
    cur.execute(
        "SELECT species FROM base_stats WHERE species ILIKE (%s)", (search_value+'%',))
    search_db = cur.fetchall()
    # returns a list of tuples: [('Lapras',), ('Lanturn',), ('Larvitar',)]
    # use this sum method to convert into list: ['Lapras', 'Lanturn', 'Larvitar']
    search_db = list(sum(search_db, ()))
    search_db.sort()
    db.close()
    # convert tuples in list into list
    try:
        #search_db = list(search_db[0])
        print('search db', search_db)
        search_results.set(search_db)
        evo_entry['values'] = search_db
    except Exception as e:
        print(e)


def open_file(*args):
    # open a file dialog to choose file
    filename = filedialog.askopenfilename()
    file_chosen.set(filename)


def analyze(*args):
    try:
        file_value = file_chosen.get()
        poke_file=file_input(file_value)
        print("file chosen", file_value)
        print("file: ", poke_file)
        evo_pokemon =  evo_pokemon_input(evo_chosen.get())
        print("evo poke: ", evo_pokemon)
        # close gui
        root.destroy()
        # run analysis program
        main()
        print('done')
    except ValueError:
        pass


# make main window, give it a title
root = Tk()
root.title("PoGo Batch Analysis")

# create a Frame widget that holds all content, place in root
mainframe = ttk.Frame(root, padding='5 5 20 12')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# if window resized, frame should expand
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# initialize vars
evo_chosen = StringVar()
file_chosen = StringVar()
search_chosen = StringVar()
search_results = StringVar()

# entry form for file
file_entry = ttk.Entry(mainframe, width = 15, textvariable=file_chosen)
file_entry.grid(column=2, row=1, sticky=(W,E))
ttk.Label(mainframe, text="File:").grid(column=1, row=1, sticky=(W,E))
# button that opens file dialog
ttk.Button(mainframe, text="...", command=open_file, width=3).grid(column=3, row=1, sticky=(W))

# entry and button to search for evo
search_entry = ttk.Entry(mainframe, textvariable=search_chosen)
search_entry.grid(column=2, row=2, sticky=(E,W))
ttk.Label(mainframe, text="Search for Evolution: ").grid(column=1, row=2)
# ideally would get text and update combobox after each keystroke
# for now, use a button to search
ttk.Button(mainframe, text="Go", width=3, command=db_search).grid(column=3, row=2, sticky=(W))
# update combobox values

ttk.Label(mainframe, text="Type in evolution if known, or choose from list").grid(column=2,row=3)
evo_entry = ttk.Combobox(mainframe, width=10, textvariable=evo_chosen)
evo_entry.grid(column=2, row=4, sticky=(W,E))
# initialize evo pokemon choices list as empty
evo_entry['values'] = []
ttk.Label(mainframe, text="Evolution:").grid(column=1, row=4, sticky=(W,E))

# button that will run main program from multi_poke_v1
ttk.Button(mainframe, text="Analyze", command=analyze).grid(column=2, row=5, sticky=(W,E))

# puts padding around all widgets
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# make cursor blink in this field first
file_entry.focus()
# makes pressing Enter key do same as press Calculate button
root.bind('<Return>', analyze)

# tells Tk to enter event loop, needed to make everything run
root.mainloop()
