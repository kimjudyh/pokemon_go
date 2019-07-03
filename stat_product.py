import math as m
from multi_poke_v1 import read_cp_mult, read_base_stats

dic_cp_mult = read_cp_mult()

pokemon = "vigoroth"
base_stats = read_base_stats(pokemon)
print(base_stats)

stam_base = base_stats[0]
atk_base = base_stats[1]
def_base = base_stats[2]

stam_IV = list(range(0,16))
atk_IV = list(range(0,16))
def_IV = list(range(0,16))

min_cpm_est = m.sqrt(14990/((atk_base+15)*m.sqrt((def_base+15)*(stam_base+15))))
max_cpm_est = m.sqrt(14990/((atk_base+0)*m.sqrt((def_base+0)*(stam_base+0))))
print(min_cpm_est)
print(max_cpm_est)

for key, value in dic_cp_mult.items():
    if (value > (min_cpm_est -.02)) and (value < (min_cpm_est)):
        min_cpm = value
        min_level = key
    if (value > (max_cpm_est)) and (value < (max_cpm_est + .02)):
        max_cpm = value
        max_level = key

print(min_cpm, "min cp mult")
print(max_cpm, "max cp mult")
print(min_level)

stat_product = []
for i_stam in stam_IV:
    for j_atk in atk_IV:
        for k_def in def_IV:
            S = stam_base + i_stam
            A = atk_base + j_atk
            D = def_base + k_def

            cp = m.floor(.1*A*m.sqrt(D*S)*min_cpm**2)
            if cp <= 1500:
                level = min_level
                while cp <= 1500:
                    level += .5
                    cp_mult = dic_cp_mult[level]
                    cp = m.floor(.1*A*m.sqrt(D*S)*cp_mult**2)
                level -= .5
                cp_mult = dic_cp_mult[level]
                cp = m.floor(.1*A*m.sqrt(D*S)*cp_mult**2)
                #print(cp)

            p = m.floor(S*cp_mult)*A*D*cp_mult**2
            #print(p)
            #todo: create data structure with IV combo, level, cp and stat product
            stat_product.append(p)

max_p = max(stat_product)
min_p = min(stat_product)
print("max", max_p)
print("min", min_p)
print(len(stat_product))


