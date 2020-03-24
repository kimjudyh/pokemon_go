from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import psycopg2

from multi_poke_v1 import *

def db_search(search_value):
    # search for pokemon names that match search string

    # create connection to database
    db = psycopg2.connect(database = 'mydb')
    cur = db.cursor()
    cur.execute(
        "SELECT species FROM base_stats WHERE species ILIKE (%s)", (search_value+'%',))
    search_db = cur.fetchall()
    # returns a list of tuples: [('Lapras',), ('Lanturn',), ('Larvitar',)]
    # use this sum method to convert into list: ['Lapras', 'Lanturn', 'Larvitar']
    search_db = list(sum(search_db, ()))
    search_db.sort()
    db.close()

    return search_db

def set_single_search_results(search_db):
    # display database search results in listbox for single pokemon
    try:
        single_list_results.set(search_db) 
    except Exception as e:
        print(e)

def set_evo_search_results(search_db):
    # display database search results in listbox for evolution pokemon
    try:
        # set listbox 
        search_results.set(search_db)
        list_results.set(search_db)
    except Exception as e:
        print(e)

def onKeyReleaseSingle(event):
    # on key press, performs search of normal pokemon string in database
    global db_search_results_single

    search_value = pokemon_name.get()
    db_search_results_single = db_search(search_value)
    # show results in listbox
    set_single_search_results(db_search_results_single)

def onKeyRelease(event):
    # on key press, performs search of evolution pokemon string in database
    global db_search_results

    search_value = search_chosen.get()
    db_search_results = db_search(search_value)
    # show results in listbox
    set_evo_search_results(db_search_results)

def onLeftClick(event):
    # on left click, make list selection evolution pokemon

    # curselection returns tuple of index of item chosen: (2,) or second list item
    selection_tuple = result_list.curselection()

    try:
        # cast index as int after extracting from tuple
        selection_idx = int(selection_tuple[0])

        # get list of search results from combobox values 
        select_from = db_search_results
        selection = select_from[selection_idx]

        # set search box to list selection
        search_chosen.set(selection)

    except:
        # nothing is selected, empty tuple
        pass


def onLeftClickSingle(event):
    # on left click, make list selection single pokemon
    selection_tuple = single_list.curselection()
    try:
        selection_idx = int(selection_tuple[0])
        #select_from = search_db
        select_from = db_search_results_single
        selection = select_from[selection_idx]
        pokemon_name.set(selection)
        single_poke_cp.focus()
    except Exception as e:
        pass

def open_file(*args):
    # open a file dialog to choose file
    filename = filedialog.askopenfilename()
    file_chosen.set(filename)


def set_single_pokemon():
    # create list of single pokemon's data
    try:
        single_entry = []
        single_entry.append(1)
        single_entry.append(pokemon_name.get())
        single_entry.append(int(CP.get()))
        single_entry.append(int(attack.get()))
        single_entry.append(int(defense.get()))
        single_entry.append(int(stamina.get()))

        return single_entry
    except ValueError:
        pass

def single_poke_analysis(single_entry):
    from stat_product import get_stat_product, create_table, calc_stat_product
    
    stats = read_stats(filename=None, single_entry=single_entry)
    evo_pokemon = search_chosen.get()
    # read cp multiplier and level data from text file
    dic_cp_mult = read_cp_mult()
    # read stardust and level data from csv file
    dic_stardust = read_stardust()
    dic_power_up = read_power_up_costs()

    for entry in stats:
        pokemon = entry[1]
        t_IV = entry[3:]    # order: atk, def, stam
        # choose correct base stat for pokemon being analyzed
        t_base_stats = read_base_stats(pokemon)
        # guess by inputing IVs and possible cp_mult into cp equation
        # narrow down levels & cp multipliers based on stardust
        t_cp_mult, t_level = narrow_cp_mult(dic_cp_mult, dic_stardust, entry,
                t_base_stats)
        # calc evolution stats
        evolve_stats = calc_evolve_cp(evo_pokemon, t_IV, t_level, t_cp_mult, 
                dic_cp_mult, dic_power_up)
        # get PVP stat product
        try:
            create_table(evo_pokemon)
            calc_stat_product(evo_pokemon)
        except Exception as e:
            pass #print(e)

        PVP_stats = get_stat_product(evo_pokemon, t_IV)
        # display tables for great league and perhaps ultra league
        display_great_league(PVP_stats, entry, t_level, t_IV, evolve_stats, evo_pokemon)
        if show_ultra_league.get() is True:
            display_ultra_league(PVP_stats, entry, t_level, t_IV, evolve_stats)
        if show_master_league.get() is True:
            display_master_league(PVP_stats, entry, t_level, t_IV, evolve_stats)
        

def analyze(*args):
    # what pressing the Analyze button does
    try:
        # see if there is a single pokemon's data
        single_entry = set_single_pokemon()
        # see if there is a csv file entered
        file_value = file_chosen.get()

        # either analyze file, or analyze single pokemon
        if len(file_value) > 0:
            # file was chosen, get its value from entry form
            poke_file = file_input(file_value)
            print("file: ", poke_file)
            # get evolution pokemon from entry form
            evo_pokemon =  evo_pokemon_input(search_chosen.get())
            print("evo poke: ", evo_pokemon)
            # get ultra and master league analysis display option state, used in main
            get_display_option(show_ultra_league.get(), show_master_league.get())
            # run main function from multi_poke_v1
            main()
            print('done')

        elif single_entry is not None:
            # single pokemon data was entered
            single_poke_analysis(single_entry)
            print('done')
        # close gui
    except ValueError:
        pass


# make main window, give it a title
root = Tk()
root.title("PoGo Batch Analysis")

# create a Frame widget that holds all content, place in root
mainframe = ttk.Frame(root, padding='5 5 5 5')
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

# create smaller Frame widget for single pokemon data entry
singleframe = ttk.Frame(mainframe)#, padding='10 5 20 12')
singleframe.grid(column=2, row=0, sticky=(N,W,E,S))

# if window resized, frame should expand
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# initialize vars
pokemon_name = StringVar()
CP = StringVar()
attack = StringVar()
defense = StringVar()
stamina = StringVar()
file_chosen = StringVar()
search_chosen = StringVar()
search_results = StringVar()
single_list_results = StringVar()
list_results = StringVar()
show_ultra_league = BooleanVar()
show_master_league = BooleanVar()

# entry forms for single Pokemon stats
single_row = 0
ttk.Label(singleframe, text="Pokemon:").grid(column=1, row=single_row, sticky=(W,E))
single_poke_name = ttk.Entry(singleframe, width=15, textvariable=pokemon_name)
single_poke_name.grid(column=1, row=single_row+1, sticky=(W,E))
single_poke_name.bind("<KeyRelease>", onKeyReleaseSingle)

ttk.Label(singleframe, text="CP").grid(column=2, row=single_row)
single_poke_cp = ttk.Entry(singleframe, width = 5, textvariable=CP)
single_poke_cp.grid(column=2, row=single_row+1, sticky=(W,))

ttk.Label(singleframe, text="ATK IV").grid(column=3, row=single_row, sticky=(W,E))
single_poke_atk = ttk.Entry(singleframe, width = 5, textvariable=attack)
single_poke_atk.grid(column=3, row=single_row+1, sticky=(W,E))

ttk.Label(singleframe, text="DEF IV").grid(column=4, row=single_row, sticky=(W,E))
single_poke_def = ttk.Entry(singleframe, width = 5, textvariable=defense)
single_poke_def.grid(column=4, row=single_row+1, sticky=(W,E))

ttk.Label(singleframe, text="STM IV").grid(column=5, row=single_row, sticky=(W,E))
single_poke_stm = ttk.Entry(singleframe, width = 5, textvariable=stamina)
single_poke_stm.grid(column=5, row=single_row+1, sticky=(W,E))

# Pokemon search list box
single_list = Listbox(mainframe, listvariable=single_list_results, height=10, 
        takefocus=False)
single_list.grid(row=single_row+1, column=2, sticky=(W,E))
# bind for cursor selection
single_list.bind("<<ListboxSelect>>", onLeftClickSingle)

# instructions
instructions = Text(mainframe, state='disabled', wrap=WORD, width=30, height=14)
instructions.grid(row=0, rowspan=3, column=1, sticky=(W,E))
instructions['state'] = 'normal'
instructions.insert('1.0', 
        '''Input data for a single pokemon, or select a file to analyze. \n
Search for the evolution pokemon and select from the list of results. \n
Click Analyze to see results.\n
This window can remain open to switch to a \
different single pokemon, file, or evolution.''')
instructions['state'] = 'disabled'

# entry form for file
file_row = 8
file_entry = ttk.Entry(mainframe, width=15, textvariable=file_chosen)
file_entry.grid(column=2, row=file_row, sticky=(W,E))
ttk.Label(mainframe, text="File:").grid(column=1, row=file_row, sticky=(E))
# button that opens file dialog
ttk.Button(mainframe, text="...", command=open_file, width=3).grid(
        column=3, row=file_row, sticky=(W))

# entry to search for evo
ttk.Label(mainframe, text="Type in evolution if known, or choose from list").grid(
        column=2,row=file_row+1, sticky=(W,E,S))
search_entry = ttk.Entry(mainframe, textvariable=search_chosen)
search_entry.grid(column=2, row=file_row+2, sticky=(E,W))
search_entry.bind("<KeyRelease>", onKeyRelease)
ttk.Label(mainframe, text="Search for Evolution: ").grid(column=1, row=file_row+2, sticky=E)

# list box that displays selectable evo poke search results
result_list = Listbox(mainframe, listvariable=list_results, height=10)
result_list.grid(row=file_row+4, column=2, stick=(W,E))
# bind for cursor selection
result_list.bind("<<ListboxSelect>>", onLeftClick)

# options
ultra_league = ttk.Checkbutton(mainframe, text="Show Ultra League Analysis",
        variable=show_ultra_league, onvalue=True, offvalue=False, takefocus=False)
ultra_league.grid(column=2, row=file_row+5)
master_league = ttk.Checkbutton(mainframe, text="Show Master League Analysis",
        variable=show_master_league, onvalue=True, offvalue=False, takefocus=False)
master_league.grid(column=2, row=file_row+6)

# button that will run main program from multi_poke_v1
ttk.Button(mainframe, text="Analyze", command=analyze).grid(column=2, row=file_row+7, sticky=(W,E))

# puts padding around all widgets
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=2)
for child in singleframe.winfo_children(): child.grid_configure(padx=5, pady=2)

# make cursor blink in this field first
single_poke_name.focus()
# makes pressing Enter key do same as press Calculate button
root.bind('<Return>', analyze)

# tells Tk to enter event loop, needed to make everything run
root.mainloop()


