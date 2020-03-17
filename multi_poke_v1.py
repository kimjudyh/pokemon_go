#!/usr/bin/python3
# This file contains the following functions:
# file_input
# evo_pokemon_input
# get_display_option
# read_stats
# read_cp_mult
# read_stardust
# read_power_up_costs
# read_base_stats
# narrow_IV
# guess_IV
# calc_evolve_cp
# display_great_league
# display_ultra_league
# display_master_league
# main


from sys import argv
from prettytable import PrettyTable
from termcolor import colored

# choose how input file is chosen
def file_input(a_file = None):
    '''
    input:
    poke_file: string, if no value is given, defaults to None

    '''
    global poke_file

    # option 1: manually change here:
    if not a_file:
        poke_file = "oneoff1.csv"
        # option 2: change while program is running
        #option = input("Input file is currently {}. Choose a new file? Y or N\n".format(poke_file))
        #option = option.lower()
        #if option == "y":
        #    poke_file = input("New file? ex. poke.csv\n")
        return poke_file
    elif a_file:
        # option 3: provide an argument to this function
        poke_file = a_file
        return poke_file


# give option to define evolution pokemon externally
def evo_pokemon_input(e_poke=None):
    global evo_pokemon
    if e_poke is None:
        pass
    else:
        evo_pokemon = e_poke
        return evo_pokemon


# get external status on whether to display Ultra League analysis
def get_display_option(state1, state2):
    # called in pogo_gui to get checkbox state
    global show_ultra_state
    global show_master_state

    show_ultra_state = state1
    show_master_state = state2
    #return show_ultra_state
    

# read and process pokemon data csv file
def read_stats(filename=None, single_entry=None):
    import csv
    
    pokemon_list = []

    if filename is not None and single_entry is None: 
        # multiple entries from CSV file

        # initialize variables
        count = 0

        # open csv file, use csv reader
        pokemon_file = open(filename, newline = '')
        read_file = csv.reader(pokemon_file)

        for i_row in read_file:
            # skip first line
            if count == 0:
                count += 1
                continue
            # cast certain entries as ints
            i_row[0] = int(i_row[0])    # id
            i_row[2] = int(i_row[2])    # cp
            i_row[3] = int(i_row[3])    # atk IV
            i_row[4] = int(i_row[4])    # def IV
            i_row[5] = int(i_row[5])    # stam IV
            # add each row to list
            pokemon_list.append(i_row)

        pokemon_file.close()

    elif filename is None and single_entry is not None:
        # single entry from the GUI
        pokemon_list.append(single_entry)
    print(pokemon_list)

    return pokemon_list

# read and process cp multiplier data text file
def read_cp_mult():
    '''
    returns dictionary with key: level (float), value: cp multiplier (float)
    each level has a unique cp multiplier
    '''
    with open("cp_mult_data.txt", "r") as cp_mult_file:
        cp_mult_list = cp_mult_file.readlines()

    #cp_mult_file = open("cp_mult_data.txt", "r")
    #cp_mult_list = cp_mult_file.readlines()
    #cp_mult_file.close()

    # remove header lines that label columns
    del(cp_mult_list[0:1])

    # initialize empty dictionary
    dic_cp_mult = {}

    # remove \t and \n, place level and cp_mult pairs into dictionary
    for entry in cp_mult_list:
        x = entry.find("\t")
        y = entry.find("\n")
        if "\n" not in entry:
            dic_cp_mult[float(entry[0:x])] = float(entry[x+1:])
        else:
            dic_cp_mult[float(entry[0:x])] = float(entry[x+1:y])

    # testing to see if works - remove later
    # level = 1
    # for i in range(0,40,1):
    #     print(dic_cp_mult[str(level)])
    #     level += 1

    return dic_cp_mult

def read_stardust():
    '''
    returns dictionary with key: stardust (int), value: list of levels (floats)
    each stardust value has up to 4 corresponding levels
    '''
    import csv

    # initialize variables
    stardust_list = []
    dic_stardust = {}
    count = 0

    # open csv file, use csv reader
    try:
        stardust_file = open("stardust_data.csv", newline = '')
        read_file = csv.reader(stardust_file)
    except Exception as e:
        print("file processing error: " + str(e))

    # go line by line through csv file
    for i_row in read_file:
        # skip first line
        if count == 0:
            count += 1
            continue
        # cast all entries in row as a float
        for j_entry in range(0,len(i_row)):
            if i_row[j_entry] == '':
                continue
            else:
                i_row[j_entry] = float(i_row[j_entry])
        # add row to list
        stardust_list.append(i_row)
    # testing - remove later
    #print(stardust_list)

    # delete last two empty entries of list
    stardust_list[-1] = stardust_list[-1][0:3]
    #print(stardust_list)
    stardust_file.close()


    # write list into a dictionary
    for entry in stardust_list:
        # cast the stardust as an int
        dic_stardust[int(entry[0])] = entry[1:]

    return dic_stardust


def read_power_up_costs():
    '''
    returns dictionary with key: level (int), value: dictionary with keys:
    'stardust': int
    'candy': int
    ex. {10.5: {'stardust': 1000, 'candy': 1}}
    '''
    import csv

    dic_power_up = {}
    count = 0

    with open("power_up_costs.csv", newline='') as power_up_file:
        read_file = csv.reader(power_up_file)
        for row in read_file:
            # skip first line
            if count == 0:
                count += 1
                continue
            dic_power_up[float(row[0])] = {'stardust': int(row[1]), 'candy': int(row[2])}

    return dic_power_up


# some base stats.. from text file? or hard-coded in for now in v1
def read_base_stats(pokemon):
    '''
    param pokemon: string of pokemon's name
    return base_stats: list [stamina, attack, defense]
    '''
    # [pokemon, stamina, attack, defense]
    import psycopg2
    import sys

    # create connection to database (mydb)
    db = psycopg2.connect(database = "mydb")

    # create cursor to go through database
    cur = db.cursor()

    # use cursor to execute SQL queries
    # retrieve base stats of given pokemon by passing in pokemon name as a tuple of one
    cur.execute(
            "SELECT hp, attack, defense FROM base_stats WHERE species = (%s)",\
                    (pokemon.title(),))
    
    # store query results (list of tuples)
    base_stats = cur.fetchall()

    # close database connection
    db.close()

    # convert tuples in list into list
    try:
        base_stats = list(base_stats[0])
    except Exception as e:
        print("{} doesn't exist. Try again?\n".format(pokemon))
        sys.exit(0)
    '''
    base_stats = [["meltan", 130, 118, 99],
                  ["charmander", 118, 116, 93],
                  ["squirtle", 127, 94, 121],
                  ["bagon", 128, 134, 93],
                  ["salamence", 216, 277, 168]]
    '''
    return base_stats

# narrow down cp multiplier range based on stardust.
def narrow_cp_mult(dic_cp_mult, dic_stardust, entry, base_stats):
    '''
    :param dic_cp_mult: dictionary of level (float): cp multiplier (float)
    :param dic_stardust: dictionary of stardust (int): list of levels (floats)
    :param stardust: stardust value (int)
    :param entry: list of pokemon's stats [name, cp (int), hp (int), stardust (int),
                    appraisal (3+ strings)]
    :return d_list_levels: dictionary of narrowed down cp mult (float): level (float)
    :return cp_mult: list of cp multipliers for each level that maps to stardust value
        ex. if stardust is 1300, levels can be 11, 11.5, 12, 12.5. cp_mult will contain 4 values.
    '''
    import math as m
    import sys

    # extract data from input list
    name = entry[1]
    cp = entry[2]
    atk_IV = entry[3]
    def_IV = entry[4]
    stam_IV = entry[5]

    stam_base = base_stats[0]
    atk_base = base_stats[1]
    def_base = base_stats[2]

    cp_mult = []
    d_list_levels = {}
    # get list of levels from stardust dictionary associated with given stardust
    #list_levels = dic_stardust[stardust]

    for key, value in dic_stardust.items():
        list_levels = value
        cp_mult = []
        for i in list_levels:
            # remove half levels
            #if i.is_integer():
                # get cp multiplier from cp_mult dictionary associated with level i
            cp_mult.append(dic_cp_mult[i])
                # populate dictionary of key: cp_mult, value: level
            d_list_levels[dic_cp_mult[i]] = i

        # guess real level from narrowed down list
        for i_cpm in cp_mult:
            # calculate cp
            calc_cp = m.floor(.1*(atk_base + atk_IV)*\
                    m.sqrt(def_base + def_IV)*\
                    m.sqrt(stam_base + stam_IV)*i_cpm**2)

            if cp == calc_cp:
                real_cp_mult = i_cpm
                real_level = d_list_levels[i_cpm]
                return real_cp_mult, real_level

    try:
        return real_cp_mult, real_level
    except Exception as e:
        print("ERROR: Wrong IVs inputted for entry {}\n".format(entry[0]))

        #sys.exit(0)
        
    #print("level", real_level)


def calc_evolve_cp(evo_pokemon, IV_list, level, cp_mult, dic_cp_mult, dic_power_up):
    '''
    :param evo_pokemon: string of evolution pokemon
    :param d_list_levels: dict of narrowed down key cp multiplier (float): 
        value level (float)
    :param IV: list of lists of [level (float), stam IV (int), atk IV (int),
        def IV (int), IV percent (float)
    :param dic_cp_mult: dict of level (float): cp multiplier (float) of all 40 levels
    :return evolve_stats: list of lists of [cp (int), hp (int)] 
    '''

    import math as m
    
    # user input on which pokemon(s) to evolve
    # user input on pokemon to evolve into

    # initialize vars for stardust and candy cost
    stardust_cost = 0
    candy_cost = 0

    # initialize var for number of power ups
    power_up_count = 0

    # assign IVs from IV_list
    stam_IV = IV_list[2]
    atk_IV = IV_list[0]
    def_IV = IV_list[1]

    # find those base stats
    base_stats = read_base_stats(evo_pokemon)
    stam_base = base_stats[0]
    atk_base = base_stats[1]
    def_base = base_stats[2]

    # calculate CP, rounding down
    calc_cp = m.floor(.1*(atk_base + atk_IV)*\
              m.sqrt(def_base + def_IV)*\
              m.sqrt(stam_base + stam_IV)*cp_mult**2)
    # calculate hp, rounding down
    calc_hp = m.floor(cp_mult*(stam_base + stam_IV))

    #print("cp, hp", calc_cp, calc_hp)

    # calculate closest cp to 1500
    cp_1500 = calc_cp
    #print("cp 1500", cp_1500)
    hp_1500 = calc_hp 
    cp_mult_1500 = cp_mult
    level_1500 = level

    # check if calc_cp is already over 1500
    if cp_1500 <= 1500:
        while cp_1500 <= 1500 and level_1500 < 40.0:
            # use level to get how much stardust, candy to power up
            stardust_cost += dic_power_up[level_1500]['stardust']
            candy_cost += dic_power_up[level_1500]['candy']

            # add to power up count, add 0.5 level
            power_up_count += 1
            level_1500 += 0.5
            
            # get new cp multiplier
            cp_mult_1500 = dic_cp_mult[level_1500]
            #print("cp_mult", cp_mult_1500)

            # calculate CP, rounding down
            cp_1500 = m.floor(.1*(atk_base + atk_IV)*\
                    m.sqrt(def_base + def_IV)*\
                    m.sqrt(stam_base + stam_IV)*cp_mult_1500**2)

            # calculate hp, rounding down
            hp_1500 = m.floor(cp_mult_1500*(stam_base + stam_IV))
        # since while loop will give cp over 1500, need to get the level below
        # and recalculate cp and hp
        if level_1500 == 40.0:
            pass
        else:
            power_up_count -= 1
            level_1500 -= 0.5
            stardust_cost -= dic_power_up[level_1500]['stardust']
            candy_cost -= dic_power_up[level_1500]['candy']

        cp_mult_1500 = dic_cp_mult[level_1500]
        # calculate CP, rounding down
        cp_1500 = m.floor(.1*(atk_base + atk_IV)*\
                m.sqrt(def_base + def_IV)*\
                m.sqrt(stam_base + stam_IV)*cp_mult_1500**2)
        # calculate hp, rounding down
        hp_1500 = m.floor(cp_mult_1500*(stam_base + stam_IV))

    # calculate closest CP to 2500 for Ultra League
    # start where Cp 1500 calcs left off
    cp_2500 = cp_1500
    cp_mult_2500 = cp_mult_1500
    level_2500 = level_1500
    stardust_2500 = stardust_cost
    candy_2500 = candy_cost
    power_up_2500 = power_up_count

    if level_2500 == 40.0:
        pass
    elif cp_2500 <= 2500:
        while cp_2500 <= 2500 and level_2500 < 40.0:
            stardust_2500 += dic_power_up[level_2500]['stardust']
            candy_2500 += dic_power_up[level_2500]['candy']
            power_up_2500 += 1
            level_2500 += 0.5
            cp_mult_2500 = dic_cp_mult[level_2500]
            cp_2500 = m.floor(.1*(atk_base + atk_IV)*\
                    m.sqrt(def_base + def_IV)*\
                    m.sqrt(stam_base + stam_IV)*cp_mult_2500**2)
        if level_2500 == 40.0:
            pass
        else:
            power_up_2500 -= 1
            level_2500 -= 0.5
            stardust_2500 -= dic_power_up[level_2500]['stardust']
            candy_2500 -= dic_power_up[level_2500]['candy']

        # calculate final values
        cp_mult_2500 = dic_cp_mult[level_2500]
        cp_2500 = m.floor(.1*(atk_base + atk_IV)*\
                m.sqrt(def_base + def_IV)*\
                m.sqrt(stam_base + stam_IV)*cp_mult_2500**2)

    # calculate max CP for Master League
    # start where cp 2500 calcs left off
    cp_max = cp_2500
    cp_mult_max = cp_mult_2500
    level_max = level_2500
    stardust_max = stardust_2500
    candy_max = candy_2500
    power_up_max = power_up_2500

    if level_max == 40.0:
        pass
    else:
        # calculate CP at level 40
        cp_mult_max = dic_cp_mult[40.0]
        cp_max = m.floor(.1*(atk_base + atk_IV)*\
                    m.sqrt(def_base + def_IV)*\
                    m.sqrt(stam_base + stam_IV)*cp_mult_max**2)
        while level_max < 40.0:
            stardust_max += dic_power_up[level_max]['stardust']
            candy_max += dic_power_up[level_max]['candy']
            power_up_max += 1
            level_max += 0.5

    dic_evolve_stats = {}
    dic_evolve_stats['great_league'] = [calc_cp, calc_hp, power_up_count, cp_1500, \
            stardust_cost, candy_cost]
    dic_evolve_stats['ultra_league'] = [cp_2500, power_up_2500, stardust_2500, candy_2500]
    dic_evolve_stats['master_league'] = [cp_max, power_up_max, stardust_max, candy_max]

    #evolve_stats = [calc_cp, calc_hp, power_up_count, cp_1500, stardust_cost, candy_cost,\
            #cp_2500, power_up_2500, stardust_2500, candy_2500]

    return dic_evolve_stats 


def display_great_league(PVP_stats, entry, t_level, t_IV, dic_evolve_stats, evo_pokemon):
    '''
    Display analysis for great league. Operates within loop of pokemon batch.
    '''

    # from PVP_stats, entry, t_level, t_IV, evolve_stats,
    # assign to variables for readability
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

    evolve_stats = dic_evolve_stats['great_league']
    evo_cp = evolve_stats[0]
    evo_hp = evolve_stats[1]
    power_up_count = evolve_stats[2]
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

    return


def display_ultra_league(PVP_stats, entry, t_level, t_IV, dic_evolve_stats):
    '''
    Display analysis for ultra league. Operates within loop of pokemon batch.
    '''
    # from PVP_stats, entry, t_level, t_IV, evolve_stats,
    # assign to variables for readability
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

    evolve_stats = dic_evolve_stats['ultra_league']
    power_up_count = evolve_stats[1]
    cp_2500 = evolve_stats[0]
    stardust_cost = evolve_stats[2]
    candy_cost = evolve_stats[3]

    print('\tUltra League Analysis:')
    
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
    headers1 = ['#Pwr^', 'Stardust', 'Candy', 'CP2500']
    data1 = [power_up_count, stardust_cost, candy_cost, cp_2500]

    # use PrettyTable to make formatted table
    pt3 = PrettyTable(headers1)
    pt3.add_row(data1)
    print(pt3)


    return

def display_master_league(PVP_stats, entry, t_level, t_IV, dic_evolve_stats):
    '''
    Display analysis for master league in a table.
    '''
    # from PVP_stats, entry, t_level, t_IV, evolve_stats,
    # assign to variables for readability
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

    evolve_stats = dic_evolve_stats['master_league']
    power_up_count = evolve_stats[1]
    cp_max = evolve_stats[0]
    stardust_cost = evolve_stats[2]
    candy_cost = evolve_stats[3]

    print('\tMaster League Analysis:')
    
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
    headers1 = ['#Pwr^', 'Stardust', 'Candy', 'Max CP']
    data1 = [power_up_count, stardust_cost, candy_cost, cp_max]

    # use PrettyTable to make formatted table
    pt3 = PrettyTable(headers1)
    pt3.add_row(data1)
    print(pt3)

    print()

    return


# main part of file that calls functions in order
#################################################
def main():
    from stat_product import get_stat_product, create_table, calc_stat_product

    # set poke_file as global so that files can be fed in
    # see read_many_files.py for usage
    global poke_file
    global evo_pokemon
    global single_entry
    global show_ultra_state
    
    # read pokemon data from text file
    try:
        # poke_file has been defined in read_many_files.py as global var
        stats = read_stats(poke_file)
    except:
        # poke_file hasn't been defined
        poke_file = file_input()
        stats = read_stats(poke_file)


    # ask for evolution pokemon (assumes only one pokemon species in file)
    if len(argv) == 2 and "csv" not in argv[1]:
        # evolution input from command line, and input not mistaken for csv file
        evo_pokemon = argv[1].lower()
        print("Using target pokemon: {}".format(evo_pokemon))
    elif len(argv) >= 3 and "csv" not in argv[1]:
        # argv has [useless string, evo pokemon, poke file]
        evo_pokemon = argv[1].lower()
    elif len(argv) >= 2 and "csv" in argv[1]:
        # no evo pokemon specified from command line, only files
        evo_pokemon = input("Evolution pokemon?\n").lower()
        print('Evolution pokemon chosen: ', evo_pokemon)
    else:
        try:
            print('Evolution pokemon chosen: ', evo_pokemon)
        except:
            evo_pokemon = input("Evolution pokemon?\n").lower()

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
        dic_evolve_stats = calc_evolve_cp(evo_pokemon, t_IV, t_level, t_cp_mult, 
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

        # display Great League analysis
        display_great_league(PVP_stats, entry, t_level, t_IV, dic_evolve_stats, evo_pokemon)

        # optionally display Ultra League analysis based on checkbox in GUI
        try:
            if show_ultra_state:
                display_ultra_league(PVP_stats, entry, t_level, t_IV, dic_evolve_stats)
            if show_master_state:
                display_master_league(PVP_stats, entry, t_level, t_IV, dic_evolve_stats)
        except Exception as e:
            print(e)

        
    #print(narrow_cp_mult.__doc__)


if __name__ == "__main__":
    main()
