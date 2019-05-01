import math as m

# test values for bulbasaur
cp = 395
hp = 65
stardust = 1600
appraisal = ["certainly", "attack", "exceeds"]

# values from online calculator
# [level, stam, atk, def]
online_IV = [[13, 9, 15, 9],
             [13, 8, 15, 10]
             ]

# base values for bulbasaur
stam_base = 128
atk_base = 118
def_base = 111

# narrow IV range using appraisal
sum_IV = list(range(30, 37))    # 30-36
stam_IV = list(range(1, 16))    # 1-15
atk_IV = [15]
def_IV = list(range(1,16))      # 1-15

print(stam_IV)

# narrow CP multiplier range using stardust
d_level = {0.48168495:13, 0.4908558:13.5, 0.49985844:14, 0.508701765:14.5}
# level = [13, 13.5, 14, 14.5]
cp_mult = [0.48168495, 0.4908558, 0.49985844, 0.508701765]

# guess stamina IV first, track which IV/level combo works
stam_cp = []        # initialize list of stamina, CP mult combos that work
                    # stam_cp = [stamina, cp_mult, ...]
for i_cp in cp_mult:
    for j_stam in stam_IV:
        calc_hp = m.floor(i_cp*(stam_base + j_stam))
        print(calc_hp)
        if hp == calc_hp:
            stam_cp.append([j_stam, i_cp])
            print(stam_cp)
        else:
            pass


print(stam_cp)

# guess attack, defense IVs
IV = []     # initialize list of IV, CP mult combos that work
            # IV = [cp_mult, stam, atk, def...]
for i_stcp in stam_cp:
    print(i_stcp)
    i_stam = i_stcp[0]  # assign stamina IV from each working combo
    i_cp = i_stcp[1]    # assign CP mult from matching working combo
    print(i_stam, i_cp)
    for j_atk in atk_IV:
        print(j_atk)
        for k_def in def_IV:
            print(k_def)
            calc_cp = .1*(atk_base + j_atk)*\
                      m.sqrt(def_base + k_def)*\
                      m.sqrt(stam_base + i_stam)*i_cp**2
            print(m.floor(calc_cp))
            if cp == m.floor(calc_cp):
                IV.append([i_cp, i_stam, j_atk, k_def])
                print(IV)
            else:
                pass

print(IV)

# format header and data
hdr_fmt = "|{0:^10}|{1:^8}|{2:^12}|{3:^12}|{4:^12}|"  # Header format
dat_fmt = "|{0:^10}|{1:^8}|{2:^12}|{3:^12}|{4:^12}|"  # Data   format

print("Here are level/IV combos that work:\n")

# Display the report header
print (hdr_fmt.format('----------', '--------', '------------',\
                      '------------', '------------'))
print (hdr_fmt.format('Pokemon', 'Level', 'Stamina IV', 'Attack IV',\
                        'Defense IV'))
print (hdr_fmt.format('----------', '--------', '------------',\
                      '------------', '------------'))


for i in IV:
    print(dat_fmt.format("Bulbasaur", d_level[i[0]], i[1], i[2], i[3]))
    #print()
