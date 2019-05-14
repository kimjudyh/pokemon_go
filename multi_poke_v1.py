
# read and process pokemon data text file
def read_stats(filename):
    with open(filename, 'r') as pogo_file:
        pogo_list = pogo_file.readlines()
    #pogo_file = open(filename, "r")
    #pogo_list = pogo_file.readlines()
    #pogo_file.close()

    # testing - remove later
    print(pogo_list)

    # initialize list of lists
    envelope = []

    # get rid of \n at end of every entry in list
    for i in range(0, len(pogo_list)):
        if "\r" in pogo_list[i]:
            pogo_list[i] = pogo_list[i][:-1]
        if "\n" in pogo_list[i]:
            pogo_list[i] = pogo_list[i][:-1]
    # testing - remove later
    print(pogo_list)

    # put each poke's data into new list in envelope
    i = 0
    temp_list = []
    # testing - remove later
    print(len(pogo_list))

    # go through each line of pogo_list, find the empty line, and
    # place contents between empty lines into list and append to envelope list
    while i != len(pogo_list):
        # if line is empty, signal to add temp list to envelope list
        if pogo_list[i] == "":
            print(temp_list)
            envelope.append(temp_list)
            temp_list = []
            i += 1
        # if line has content, add to temp list, move to next line
        elif pogo_list[i] != "":
            temp_list.append(pogo_list[i])
            i += 1
        # if on the last line of pogo_list, add temp list to envelope
        if i == len(pogo_list):
            envelope.append(temp_list)

    # testing - remove later
    print(envelope)

    # convert numeric values CP, HP, stardust into ints
    for line in envelope:
        line[2] = int(line[2])  # cast cp as int
        line[3] = int(line[3])  # cast hp as int
        line[4] = int(line[4])  # cast stardust as int

    # testing - remove later
    print(envelope)

    return envelope

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



# some base stats.. from text file? or hard-coded in for now in v1
def read_base_stats():
    # [pokemon, stamina, attack, defense]
    base_stats = [["meltan", 130, 118, 99],
                  ["charmander", 118, 116, 93],
                  ["squirtle", 127, 94, 121],
                  ["bagon", 128, 134, 93],
                  ["salamence", 216, 277, 168]]
    return base_stats

# narrow down IV values using appraisal
def narrow_IV(entry):
    '''
    :param entry: list of following values..
        name: Pokemon species being evolved (str)
        CP: current CP (int)
        HP: current HP (int)
        stardust: amount of stardust needed to power up (int)
        appraisal: text from blanche (3+ strings)
    :return stam_IV: list of ints of narrowed down values
    :return atk_IV: list of ints of narrowed down values
    :return def_IV: list of ints of narrowed down values
    :return is_single: boolean of whether there is only one dominant IV, use to check
        later for IVs equalling the dominant IV when they shouldn't
    '''
    # extract data from input list
    name = entry[1]
    cp = entry[2]
    hp = entry[3]
    stardust = entry[4]
    appraisal = entry[5:]

    for entry in appraisal:
        entry = entry.lower()

    # create IV lists with all possible values 0-15
    stam_IV = list(range(0,16))
    atk_IV =  list(range(0,16))
    def_IV =  list(range(0,16))

    # set is_single to default True
    #is_single = True
    #two_stats = ""
    is_single = {"bool": True, "max":""}
    print(is_single)

    max_IV = []
    other_IV = []

    if "exceeds" in appraisal:
        max_IV = [15]   # 15
        # other stats can't be 15
        other_IV = list(range(0,15))    # 0-14
    elif "certainly impressed" in appraisal:
        max_IV = [13, 14]
        # other stats can't be >= 14
        other_IV = list(range(0,14))    # 0-13
    elif "noticeably" in appraisal:
        max_IV = list(range(8,13))  # 8-12
        # other stats can't be >=12
        other_IV = list(range(0,12))    # 0-11
    elif "norm" in appraisal:
        max_IV = list(range(0,8))   # 0-7
        # other stats can't be >=7
        other_IV = list(range(0,7))     # 0-6
    else:
        print("error with IV appraisal")

    #print("max_IV, other_IV: ", max_IV, other_IV)

    # Account for different lengths of appraisal list
    # one stat
    if len(appraisal) == 3:
        # Attack
        if "attack" in appraisal:
            atk_IV = max_IV
            def_IV = other_IV
            stam_IV = other_IV
            # set "max" key in is_single to attack
            is_single["max"] = "attack"
        # Defense
        elif "defense" in appraisal:
            def_IV = max_IV
            atk_IV = other_IV
            stam_IV = other_IV
            # set "max" key in is_single to defense
            is_single["max"] = "defense"
        # Stamina
        elif "hp" in appraisal:
            stam_IV = max_IV
            atk_IV = other_IV
            def_IV = other_IV
            # set "max" key in is_single to stamina
            is_single["max"] = "stamina"
        else:
            print("error with one stat")
    # two stats
    elif len(appraisal) == 4:
        # set "bool" key in is_single to False
        is_single["bool"] = False
        # Stamina & Defense
        if "attack" not in appraisal:
            stam_IV = max_IV
            def_IV = max_IV
            atk_IV = other_IV
            # set "max" key in is_single to "not attack"
            is_single["max"] = "not attack"
        # Stamina & Attack
        elif "defense" not in appraisal:
            stam_IV = max_IV
            atk_IV = max_IV
            def_IV = other_IV
            # set "max" key in is_single to "not defense"
            is_single["max"] = "not defense"
        # Attack & Defense
        elif "hp" not in appraisal:
            atk_IV = max_IV
            def_IV = max_IV
            stam_IV = other_IV
            # set "max" key in is_single to "not hp"
            is_single["max"] = "not hp"
        else:
            print("error with two stats")
    # three stats
    elif len(appraisal) == 5:
        is_single["bool"] = False
        atk_IV = max_IV
        def_IV = max_IV
        stam_IV = max_IV
        # set "max" key in is_single to "all"
        is_single["max"] = "all"
    else:
        print("error with appraisal length")

    # account for different length of appraisal list
    # one stat
    # if len(appraisal) == 3:
    #     # extract stat
    #     # ATTACK
    #     if appraisal[1] == "attack" and appraisal[2] == "exceeds":
    #         atk_IV = [15]
    #         # defense and stamina cannot equal 15
    #         stam_IV = stam_IV[0:15]
    #         def_IV = def_IV[0:15]
    #     elif appraisal[1] == "attack" and appraisal[2] == "certainly impressed":
    #         atk_IV = [13, 14]
    #         # defense and stamina cannot be >= 14
    #         stam_IV = stam_IV[0:14]
    #         def_IV = def_IV[0:14]
    #     elif  appraisal[1] == "attack" and appraisal[2] == "noticeably":
    #         atk_IV = list(range(8,13))      # 8-12
    #         # defense and stamina cannot be >= 12
    #         stam_IV = stam_IV[0:12]
    #         def_IV = def_IV[0:12]
    #     elif appraisal[1] == "attack" and appraisal[2] == "norm":
    #         atk_IV = list(range(0,8))       # 0-7
    #         # defense and stamina cannot be >= 7
    #         stam_IV = stam_IV[0:7]
    #         def_IV = def_IV[0:7]
    #
    #     # DEFENSE
    #     elif appraisal[1] == "defense" and appraisal[2] == "exceeds":
    #         def_IV = [15]
    #         # attack and stamina can't be 15
    #         stam_IV = stam_IV[0:15]
    #         atk_IV = atk_IV[0:15]
    #     elif appraisal[1] == "defense" and appraisal[2] == "certainly impressed":
    #         def_IV = [13, 14]
    #         # attack and stamina can't be >= 14
    #         stam_IV = stam_IV[0:14]
    #         atk_IV = atk_IV[0:14]
    #     elif appraisal[1] == "defense" and appraisal[2] == "noticeably":
    #         def_IV = list(range(8,13))      # 8-12
    #         # attack and stamina can't be >= 12
    #         stam_IV = stam_IV[0:12]
    #         atk_IV = atk_IV[0:12]
    #     elif appraisal[1] == "defense" and appraisal[2] == "norm":
    #         def_IV = list(range(0,8))       # 0-7
    #         # attack and stamina can't be >= 7
    #         stam_IV = stam_IV[0:7]
    #         atk_IV = atk_IV[0:7]
    #
    #     # STAMINA
    #     elif appraisal[1] == "hp" and appraisal[2] == "exceeds":
    #         stam_IV = [15]
    #         # attack and defense can't be 15
    #         atk_IV = atk_IV[0:15]
    #         def_IV = def_IV[0:15]
    #     elif appraisal[1] == "hp" and appraisal[2] == "certainly impressed":
    #         stam_IV = [13, 14]
    #         # attack and defense can't be >= 14
    #         atk_IV = atk_IV[0:14]
    #         def_IV = def_IV[0:14]
    #     elif  appraisal[1] == "hp" and appraisal[2] == "noticeably":
    #         stam_IV = list(range(8,13))      # 8-12
    #         # attack and defense can't be >= 12
    #         atk_IV = atk_IV[0:12]
    #         def_IV = def_IV[0:12]
    #     elif appraisal[1] == "hp" and appraisal[2] == "norm":
    #         stam_IV = list(range(0,8))       # 0-7
    #         # attack and defense can't be >= 7
    #         atk_IV = atk_IV[0:7]
    #         def_IV = def_IV[0:7]
    #     else:
    #         pass

    # two stats, set is_single to False
    # if len(appraisal) == 4:
    #     is_single = False
    #     # find the stat that doesn't appear to get the two stats
    #     # DEFENSE & STAMINA
    #     if "attack" not in appraisal \
    #             and appraisal[3] == "exceeds":
    #         def_IV = [15]           # 15
    #         stam_IV = [15]          # 15
    #         # attack can't be 15
    #         atk_IV = atk_IV[0:15]
    #         print("hp and defense exceeds")
    #         print("def", def_IV, "stam", stam_IV, "atk", atk_IV)
    #     elif "attack" not in appraisal \
    #             and appraisal[3] == "certainly impressed":
    #         def_IV = [13, 14]       # 13-14
    #         stam_IV = [13, 14]      # 13-14
    #         # attack can't be >= 14
    #         atk_IV = atk_IV[0:14]
    #         print("defense and hp")
    #     elif "attack" not in appraisal \
    #             and appraisal[3] == "noticeably":
    #         def_IV = list(range(8,13))  # 8-12
    #         stam_IV = def_IV.copy()
    #         # attack can't be >= 12
    #         atk_IV = atk_IV[0:12]
    #     elif "attack" not in appraisal \
    #             and appraisal [3] == "norm":
    #         def_IV = def_IV[0:8]    # 0-7
    #         stam_IV = stam_IV[0:8]  # 0-7
    #         # attack can't be >= 7
    #         atk_IV = atk_IV[0:7]
    #
    #     # ATTACK & STAMINA
    #     elif "defense" not in appraisal \
    #             and appraisal[3] == "exceeds":
    #         atk_IV = [15]       # 15
    #         stam_IV = [15]      # 15
    #         # defense can't be 15
    #         def_IV = def_IV[0:15]
    #         print("i'm at attack and stamina exceeds")
    #     elif "defense" not in appraisal \
    #             and appraisal[3] == "certainly impressed":
    #         atk_IV = [13, 14]   # 13-14
    #         stam_IV = [13, 14]  # 13-14
    #         # defense can't be >= 14
    #         def_IV = def_IV[0:14]
    #     elif "defense" not in appraisal \
    #             and appraisal[3] == "noticeably":
    #         atk_IV = atk_IV[8:13]   # 8-12
    #         stam_IV = stam_IV[8:13] # 8-12
    #         # defense can't be >= 12
    #         def_IV = def_IV[0:12]
    #     elif "defense" not in appraisal \
    #             and appraisal[3] == "norm":
    #         atk_IV = atk_IV[0:8]    # 0-7
    #         stam_IV = stam_IV[0:8]
    #         # defense can't be >= 7
    #         def_IV = def_IV[0:7]
    #
    #     # ATTACK & DEFENSE
    #     elif "hp" not in appraisal and appraisal[3] == "exceeds":
    #         def_IV = [15]       # 15
    #         atk_IV = [15]       # 15
    #         # stamina can't be 15
    #         stam_IV = stam_IV[0:15]
    #         print("i'm at attack and defense exceeds")
    #     elif "hp" not in appraisal \
    #             and appraisal[3] == "certainly impressed":
    #         def_IV = [13, 14]   # 13-14
    #         atk_IV = [13, 14]   # 13-14
    #         # stamina can't be >= 14
    #         stam_IV = stam_IV[0:14]
    #         print("i'm at attack and defense certainly impressed")
    #     elif "hp" not in appraisal and appraisal [3] == "noticeably":
    #         def_IV = def_IV[8:13]       # 8-12
    #         atk_IV = atk_IV[8:13]
    #         # stamina can't be >= 12
    #         stam_IV = stam_IV[0:12]
    #     elif "hp" not in appraisal and appraisal[3] == "norm":
    #         def_IV = def_IV[0:8]    # 0-7
    #         atk_IV = atk_IV[0:8]
    #         # stamina can't be >= 7
    #         stam_IV = stam_IV[0:7]
    # # three stats, set is_single to False
    # elif len(appraisal) == 5:
    #     is_single = False
    #     # must be all stats
    #     if appraisal[4] == "exceeds":
    #         atk_IV = [15]
    #         def_IV = [15]
    #         stam_IV = [15]
    #     elif appraisal[4] == "certainly impressed":
    #         atk_IV = [13, 14]
    #         def_IV = [13, 14]
    #         stam_IV = [13, 14]


    return stam_IV, atk_IV, def_IV, is_single#, two_stats

# narrow down cp multiplier range based on stardust.
def narrow_cp_mult(dic_cp_mult, dic_stardust, entry):
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
    # extract data from input list
    name = entry[1]
    cp = entry[2]
    hp = entry[3]
    stardust = entry[4]
    appraisal = entry[5:]

    cp_mult = []
    d_list_levels = {}
    list_levels = dic_stardust[stardust]
    for i in list_levels:
        # remove half levels
        if i.is_integer():
            cp_mult.append(dic_cp_mult[i])
            d_list_levels[dic_cp_mult[i]] = i

    #print("d_list_levels: ", d_list_levels)
    return d_list_levels, cp_mult

# function that guesses IVs
def guess_IV(cp_mult, stam_IV, atk_IV, def_IV, base_stats, entry, d_list_levels, is_single):
    '''
    Processes one pokemon's original stats and narrowed down IVs to guess the combo of
    level, attack IV, stamina IV, and defense IV that satisfies a given CP equation.
    :param cp_mult: list of narrowed down cp multipliers (float)
    :param stam_IV: list of narrowed down IVs (int)
    :param atk_IV: list of narrowed down IVs (int)
    :param def_IV: list of narrowed down IVs (int)
    :param base_stats: list of base stats for one pokemon, contains:
        [pokemon name (str), base stam (int), base atk (int), base def (int)]
    :param entry: list of original stats for one pokemon
    :param d_list_levels: dict of key cp multiplier (float): value level (float)
    :param is_single: tells if there is a singled out IV (True) or not (False)
    :return IV: list of lists of level & IV combos that work, contains:
        [level (float), stamina IV (int), attack IV (int), defense IV (int), percentage (float)]
    '''
    import math as m

    # extract data from input list
    name = entry[1]
    cp = entry[2]
    hp = entry[3]
    stardust = entry[4]
    appraisal = entry[5]
    appraisal = appraisal.lower()
    #print("appraisal:", appraisal)

    # extract base stats from base_stats list
    stam_base = base_stats[0]
    atk_base = base_stats[1]
    def_base = base_stats[2]
    
    # extract info from is_single dictionary
    single = is_single["bool"]
    max_stat = is_single["max"]
    print(is_single)

    # initialize empty vars
    stam_cp = []       # list of lists: [[stamina, cp_mult, level]]
    IV = []            # list of lists: [[cp_mult, stam, atk, def]]
    IV_sum = 0
    IV_percent = 0.0

    # guess stamina IV first, track which IV/level combo works
    # for each possibility of cp_mult (aka level)
    for i_cp in cp_mult:
        # go through possible values in stamina IV list
        for j_stam in stam_IV:
            # calculate hp, rounding down
            calc_hp = m.floor(i_cp*(stam_base + j_stam))
            # if actual and calculated hp are equal
            if hp == calc_hp:
                # use cp multiplier value to get level
                lvl = d_list_levels[i_cp]
                # add list of [stamina IV, cp multiplier, level] to stam_cp
                stam_cp.append([j_stam, i_cp, lvl])
            else:
                pass
    print("atk_IV", atk_IV)
    # guess attack, defense IVs
    # for each possibility in stam_cp list of lists
    for i_stcp in stam_cp:
        i_stam = i_stcp[0]  # assign stamina IV from each working combo
        i_cp = i_stcp[1]    # assign CP mult from matching working combo
        i_lvl = i_stcp[2]   # assign level from matching working combo
        # for each possible attack IV
        for j_atk in atk_IV:
            #print("j_atk", j_atk)
            # for each possible defense IV
            for k_def in def_IV:
                # calculate CP, rounding down
                calc_cp = m.floor(.1*(atk_base + j_atk)*\
                          m.sqrt(def_base + k_def)*\
                          m.sqrt(stam_base + i_stam)*i_cp**2)
                #print("calc_cp=", calc_cp)
                # if actual and calculated CP are equal
                if cp == calc_cp:
                    # calculate IV sum and IV percentage
                    IV_sum = i_stam + j_atk + k_def
                    IV_percent = IV_sum/45*100
                    print("IV sum", IV_sum)
                    print(j_atk, k_def, i_stam)
                    print(appraisal, max_stat)

                    # 1 stat: check for illegal duplicate IVs
                    if max_stat == "attack" and (j_atk == i_stam or j_atk == k_def):
                        break
                    elif max_stat == "defense" and (k_def == j_atk or k_def == i_stam):
                        break
                    elif max_stat == "stamina" and (i_stam == j_atk or i_stam == k_def):
                        break
                    # 2 stats: check that stamina and attack IVs equal
                    if max_stat == "not defense" and i_stam != j_atk:
                        break
                    # 2 stats: check that stamina and defense IVs equal
                    elif max_stat == "not attack" and i_stam != k_def:
                        break
                    # 2 stats: check that attack and defense IVs equal
                    elif max_stat == "not hp" and j_atk != k_def:
                        print("not hp", i_stam, j_atk, k_def)
                        break
                    # 3 stats: check that all three stats are equal 
                    if max_stat == "all" and \
                            (i_stam != j_atk or i_stam != k_def or j_atk != k_def):
                        break
                    # otherwise, check IV sum against appraisal
                    if appraisal == "wonder":
                        # sum of IVs >= 37
                        if IV_sum >= 37:
                            # add to IV list [level, stam IV, atk IV, def IV, percentage]
                            IV.append([i_lvl, i_stam, j_atk, k_def, IV_percent])
                        else:
                            break
                    elif appraisal == "certainly":
                        print(j_atk, k_def, i_stam)
                        # sum of IVs: 30-36
                        if IV_sum >=30 and IV_sum <= 36:
                            print("certainly", "IV_sum", IV_sum)
                            # add to IV list [level, stam IV, atk IV, def IV, percentage]
                            IV.append([i_lvl, i_stam, j_atk, k_def, IV_percent])
                        else:
                            break
                    elif appraisal == "above average":
                        # sum of IVs: 23-29
                        if IV_sum >= 23 and IV_sum <=29:
                            # add to IV list [level, stam IV, atk IV, def IV, percentage]
                            IV.append([i_lvl, i_stam, j_atk, k_def, IV_percent])
                        else:
                            break
                    elif appraisal == "not likely":
                        # sum of IVs: 0-22
                        if IV_sum <=22:
                            # add to IV list [level, stam IV, atk IV, def IV, percentage]
                            IV.append([i_lvl, i_stam, j_atk, k_def, IV_percent])
                        else:
                            break
                else:
                    pass

    return IV

def calc_evolve_cp(d_list_levels, IV):
    '''
    :param d_list_levels: dict of narrowed down key cp multiplier (float): 
        value level (float)
    :param IV: list of [level (float), stam IV (int), atk IV (int),
        def IV (int), IV percent (float)

    '''

    import math as m
    
    # user input on which pokemon(s) to evolve
    # user input on pokemon to evolve into

    evolve_stats = []

    for i_combo in IV:
        level = i_combo[0]
        stam_IV = i_combo[1]
        atk_IV = i_combo[2]
        def_IV = i_combo[3]

        # find those base stats
        atk_base = 277  # salamence
        def_base = 168  # salamence
        stam_base = 216 # salamence
        # use calc'd IVs, level, new base stats to calc CP
        for key, value in d_list_levels.items():
            if value == level:
                cp_mult = key
        # also calc HP
        # calculate CP, rounding down
        calc_cp = m.floor(.1*(atk_base + atk_IV)*\
                  m.sqrt(def_base + def_IV)*\
                  m.sqrt(stam_base + stam_IV)*cp_mult**2)
        # calculate hp, rounding down
        calc_hp = m.floor(cp_mult*(stam_base + stam_IV))

        evolve_stats.append([calc_cp, calc_hp])

    return evolve_stats 


# main part of file that calls functions in order
#################################################
def main():
    # read pokemon data from text file
    stats = read_stats("poke_data_4.txt")

    # read cp multiplier and level data from text file
    dic_cp_mult = read_cp_mult()
    #print(dic_cp_mult[5])

    # read stardust and level data from csv file
    dic_stardust = read_stardust()
    #print(dic_stardust[1300])

    # for now, get base stats of 3 pokemon
    base_stats = read_base_stats()

    # narrow down IVs using appraisal
    for entry in stats:
        # choose correct base stat for pokemon being analyzed
        for poke in base_stats:
            if poke[0] == entry[1]:
                t_base_stats = poke[1:]

        # narrow down IVs based on appraisal language
        t_stam_IV, t_atk_IV, t_def_IV, is_single = narrow_IV(entry)
        # narrow down levels & cp multipliers based on stardust
        t_list_levels, t_cp_mult = narrow_cp_mult(dic_cp_mult, dic_stardust, entry)
        print("t_list_levels", t_list_levels)
        # guess all level & IV combos that work
        t_IV = guess_IV(t_cp_mult, t_stam_IV, t_atk_IV, t_def_IV, t_base_stats, entry,
                        t_list_levels, is_single)

        # save appraisal data to display in report
        t_appraisal = entry[5:]

        # add info to pokemon's entry list [level, stam IV, atk IV, def IV, percentage]
        entry.append(t_IV)
        #print(entry)
        # format header and data
        hdr_fmt = "|{0:^10}|{1:^8}|{2:^8}|{3:^8}|{4:^8}|{5:^8}|"  # Header format
        dat_fmt = "|{0:^10}|{1:^8}|{2:^8}|{3:^8}|{4:^8}|{5:^8}|"  # Data   format

        #print("Original stats.. :", entry[2:5], t_appraisal)
        print("{}. Original stats:".format(entry[0]))
        print("CP: {}, HP: {}, Stardust: {}".format(entry[2], entry[3], entry[4]))
        print("Appraisal:", t_appraisal)
        #print("Here are level/IV combos that work:")

        # Display the report header
        print (hdr_fmt.format('----------', '--------', '--------',\
                              '--------', '--------', '--------'))
        print (hdr_fmt.format('Pokemon', 'Level', 'Stamina', 'Attack',\
                                'Defense', 'Percent'))
        print (hdr_fmt.format('----------', '--------', '--------',\
                              '--------', '--------', '--------'))

        # print IV report for pokemon
        for i in t_IV:
            pokemon = entry[1]
            level = i[0]
            stamina = i[1]
            attack = i[2]
            defense = i[3]
            percent = i[4]
            print(dat_fmt.format(pokemon, level, stamina, attack, defense,'{:,.2f}%'.format(percent)))

        print()

        evolve_stats = calc_evolve_cp(t_list_levels, t_IV)
        for i_combo, j_IV in zip(evolve_stats, t_IV):
            calc_cp = i_combo[0]
            calc_hp = i_combo[1]
            print(j_IV[:-1])
            print("Salamence CP: {} and HP: {}".format(calc_cp, calc_hp))

        #print("Salamence CP: ", calc_cp)
        #print("HP: ", calc_hp)

    #print(narrow_cp_mult.__doc__)


if __name__ == "__main__":
    main()
