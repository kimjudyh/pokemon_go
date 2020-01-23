from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import psycopg2

from multi_poke_v1 import *


def db_search(search_value):
    # search for pokemon names that match search string
    # make results global so can be accessed in other functions
    global search_db
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
    # convert tuples in list into list

def set_single_search_results():
    try:
        single_list_results.set(search_db) 
    except Exception as e:
        print(e)


def set_evo_search_results():
    try:
        search_results.set(search_db)
        evo_entry['values'] = search_db

        # write top 10 to text box
        # first clear contents of text box
        result_box['state'] = 'normal'
        result_box.delete('1.0', 'end')
        if len(search_db) > 10:
            list_results.set(search_db[0:10])
            for i in range(0,10):
                result_box.insert('end', search_db[i])
                result_box.insert('end', '\n')
        else:
            list_results.set(search_db)
            for result in search_db:
                result_box.insert('end', result)
                result_box.insert('end', '\n')
        result_box['state'] = 'disabled'
    except Exception as e:
        print(e)

def onKeyReleaseSingle(event):
    # on key press, performs search of normal pokemon string in database
    search_value = pokemon_name.get()
    db_search(search_value)
    set_single_search_results()

def onKeyRelease(event):
    # on key press, performs search of evolution pokemon string in database

    search_value = search_chosen.get()
    db_search(search_value)
    set_evo_search_results()

def onLeftClick(event):
    # on left click, make list selection evolution pokemon

    # curselection returns tuple of index of item chosen: (2,) or second list item
    selection_tuple = result_list.curselection()

    try:
        # cast index as int after extracting from tuple
        selection_idx = int(selection_tuple[0])


        # get list of search results from combobox values (somehow only global list)
        select_from = search_db
        selection = select_from[selection_idx]

        # set combobox to list selection
        evo_chosen.set(selection)
    except:
        # nothing is selected, empty tuple
        pass


def onLeftClickSingle(event):
    selection_tuple = single_list.curselection()
    try:
        selection_idx = int(selection_tuple[0])
        select_from = search_db
        selection = select_from[selection_idx]
        pokemon_name.set(selection)
        single_poke_cp.focus()
    except:
        pass

def open_file(*args):
    # open a file dialog to choose file
    filename = filedialog.askopenfilename()
    file_chosen.set(filename)


def set_single_pokemon():
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

    evo_pokemon = evo_chosen.get()

    # read cp multiplier and level data from text file
    dic_cp_mult = read_cp_mult()
    #print(dic_cp_mult)

    # read stardust and level data from csv file
    dic_stardust = read_stardust()
    #print(dic_stardust[1300])

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
        #print("t_list_levels", t_list_levels)
       
        # calc evolution stats
        evolve_stats = calc_evolve_cp(evo_pokemon, t_IV, t_level, t_cp_mult, 
                dic_cp_mult, dic_power_up)
        #print(evolve_stats)

        # get PVP stat product
        try:
            #print("creating table for: {}".format(evo_pokemon))
            create_table(evo_pokemon)
            calc_stat_product(evo_pokemon)
        except Exception as e:
            #print(e)
            pass #print(e)

        PVP_stats = get_stat_product(evo_pokemon, t_IV)
        rank = PVP_stats[0]
        stat_product = PVP_stats[1]
        percent_max = PVP_stats[2]

        pokemon = entry[1]
        original_cp = entry[2]
        level = t_level 
        stamina = t_IV[2]
        attack = t_IV[0]
        defense = t_IV[1]
        percent = (stamina+attack+defense)/45*100

        evo_cp = evolve_stats[0]
        evo_hp = evolve_stats[1]
        power_up_count =evolve_stats[2]
        cp_1500 = evolve_stats[3]
        stardust_cost = evolve_stats[4]
        candy_cost = evolve_stats[5]


        # print ex: 53. trapinch --> flygon
        print("{}. {} --> {}".format(
            entry[0],
            pokemon,
            evo_pokemon,
            ))

        # color code rank
        if rank <= 200:
            rank_data = [colored(rank, 'green', attrs=['reverse', 'bold'])]
        elif rank <= 1000:
            rank_data = [colored(rank, 'green')]
        elif 1000 < rank <= 2000:
            rank_data = [colored(rank, 'yellow')]
        else:
            rank_data = [colored(rank, 'red')]

        # define headers and corresponding data to put in table
        headers1 = ['CP', 'Level', 'ATK', 'DEF', 'STM', 'IV %']
        data1 = [original_cp, level, attack, defense, stamina, '{:,.2f}%'.format(percent)]

        headers2 = ['Rank', 'Evo CP', '#Pwr^', 'Stardust', 'Candy', 'CP1500']
        data2 = rank_data + [evo_cp, power_up_count, stardust_cost, candy_cost, cp_1500]

        # use PrettyTable to make formatted table
        pt3 = PrettyTable(headers1 + headers2)
        pt3.add_row(data1 + data2)
        print(pt3)


        # optionally print stat product, percent of max
        #print("Stat Product: {:.2f}\nPercent of Max: {:,.2f}%".format(
        #    stat_product, percent_max))


        print()


def analyze(*args):
    try:
        single_entry = set_single_pokemon()
        print(single_entry)
        file_value = file_chosen.get()
        print(len(file_value))
        if len(file_value) > 0:
            poke_file = file_input(file_value)
            print("file: ", poke_file)
            evo_pokemon =  evo_pokemon_input(evo_chosen.get())
            print("evo poke: ", evo_pokemon)
            main()
            print('done')

        elif single_entry is not None:
            single_poke_analysis(single_entry)
            print('done')
        # close gui
        #root.destroy()
        # run analysis program
    except ValueError:
        pass


# make main window, give it a title
root = Tk()
root.title("PoGo Batch Analysis")

# create a Frame widget that holds all content, place in root
mainframe = ttk.Frame(root, padding='50 5 20 12')
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
evo_chosen = StringVar()
file_chosen = StringVar()
search_chosen = StringVar()
search_results = StringVar()

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
single_list_results = StringVar()
single_list = Listbox(mainframe, listvariable=single_list_results, height=5)
single_list.grid(row=single_row+1, column=2, stick=(W,E))
# bind for cursor selection
single_list.bind("<<ListboxSelect>>", onLeftClickSingle)

# instructions
instructions = Text(mainframe, state='disabled', wrap=WORD, width=30, height=14)
instructions.grid(row=0, rowspan=3, column=1, sticky=(W,E))
instructions['state'] = 'normal'
instructions.insert('1.0', 
        '''Input data for a single pokemon, or select a file to analyze. \
Search for the evolution pokemon and select from the list of results. \
Or directly type it into the Evolution drop-down menu field. \n
Click Analyze to see results. This window can remain open to switch to a \
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

# entry and button to search for evo
search_entry = ttk.Entry(mainframe, textvariable=search_chosen)
search_entry.grid(column=2, row=file_row+1, sticky=(E,W))
search_entry.bind("<KeyRelease>", onKeyRelease)
ttk.Label(mainframe, text="Search for Evolution: ").grid(column=1, row=file_row+1, sticky=E)
# ideally would get text and update combobox after each keystroke
# for now, use a button to search
ttk.Button(mainframe, text="Go", width=3, command=db_search).grid(
        column=3, row=file_row+1, sticky=(W))
# update combobox values

ttk.Label(mainframe, text="Type in evolution if known, or choose from list").grid(
        column=2,row=file_row+2)
evo_entry = ttk.Combobox(mainframe, width=10, textvariable=evo_chosen)
evo_entry.grid(column=2, row=file_row+3, sticky=(W,E))
# initialize evo pokemon choices list as empty
evo_entry['values'] = []
ttk.Label(mainframe, text="Evolution:").grid(column=1, row=file_row+3, sticky=(E))

# make text box that shows top 10 search results
result_box = Text(mainframe, state='disabled', width=15, height=10)
result_box.grid(row=file_row+5, column=1, sticky=(W,E))

list_results = StringVar()
result_list = Listbox(mainframe, listvariable=list_results, height=10)
result_list.grid(row=file_row+5, column=2, stick=(W,E))
# bind for cursor selection
result_list.bind("<<ListboxSelect>>", onLeftClick)

# button that will run main program from multi_poke_v1
ttk.Button(mainframe, text="Analyze", command=analyze).grid(column=2, row=file_row+4, sticky=(W,E))

# puts padding around all widgets
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
for child in singleframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# make cursor blink in this field first
single_poke_name.focus()
# makes pressing Enter key do same as press Calculate button
#root.bind('<Return>', analyze)

# tells Tk to enter event loop, needed to make everything run
root.mainloop()
