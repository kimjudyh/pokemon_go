# test power up cost calculations
# stardust cost
# candy cost
# final level

from ..scripts.multi_poke_v1 import *

def set_up(pokemon, CP, IV_list, evo_pokemon):
    entry = [0, pokemon, CP] + IV_list
    dic_cp_mult = read_cp_mult()
    dic_stardust = read_stardust()
    dic_power_up = read_power_up_costs()
    base_stats = read_base_stats(pokemon)
    cp_mult, level = narrow_cp_mult(dic_cp_mult, dic_stardust, entry, base_stats)
    dic_evolve_stats = calc_evolve_cp(evo_pokemon, IV_list, level, cp_mult, 
            dic_cp_mult, dic_power_up)
    return level, dic_evolve_stats

'''
dic_evolve_stats['great_league'] = [calc_cp, calc_hp, power_up_count, cp_1500, \
            stardust_cost, candy_cost, level_1500]
    dic_evolve_stats['ultra_league'] = [cp_2500, power_up_2500, stardust_2500,
        candy_2500, level_2500]
    dic_evolve_stats['master_league'] = [cp_max, power_up_max, stardust_max, candy_max]
'''

list_of_dics = []
list_of_gampress_dics = []

level, dic_calc_1 = set_up("machop", 532, [15, 12, 10], "machamp")
dic_gg_1 = {'great_league': [1497, 9800, 10],
        'ultra_league': [2482, 86400, 78],
        'master_league': [2995, 246400, 268]}
list_of_dics.append(dic_calc_1)
list_of_gampress_dics.append(dic_gg_1)

level, dic_calc_1 = set_up("cresselia", 1614, [14, 14, 13], "cresselia")
dic_gg_1 = {'great_league': [1614, 0, 0],
        'ultra_league': [2482, 91000, 80],
        'master_league': [2825, 225000, 248]}
list_of_dics.append(dic_calc_1)
list_of_gampress_dics.append(dic_gg_1)

level, dic_calc_1 = set_up("swablu", 417, [14, 14, 15], "altaria")
dic_gg_1 = {'great_league': [1476, 48400, 42],
        'ultra_league': [1987, 234400, 256],
        'master_league': [1987, 234400, 256]}
list_of_dics.append(dic_calc_1)
list_of_gampress_dics.append(dic_gg_1)

level, dic_calc_1 = set_up("rhyhorn", 211, [11, 10, 11], "rhyperior")
dic_gg_1 = {'great_league': [1492, 19600, 26],
        'ultra_league': [2470, 66600, 70],
        'master_league': [3602, 267600, 296]}
list_of_dics.append(dic_calc_1)
list_of_gampress_dics.append(dic_gg_1)

level, dic_calc_1 = set_up("meditite", 473, [9, 11, 6], "medicham")
dic_gg_1 = {'great_league': [1315, 178000, 206],
        'ultra_league': [1315, 178000, 206],
        'master_league': [1315, 178000, 206]}
list_of_dics.append(dic_calc_1)
list_of_gampress_dics.append(dic_gg_1)

level, dic_calc_1 = set_up("dratini", 223, [14, 0, 1], "dragonite")
dic_gg_1 = {'great_league': [1461, 14000, 18],
        'ultra_league': [2469, 64500, 65],
        'master_league': [3527, 262000, 288]}
list_of_dics.append(dic_calc_1)
list_of_gampress_dics.append(dic_gg_1)


def test_costs():
    for calc, gg in zip(list_of_dics, list_of_gampress_dics):
        for i, ig in zip([3, 4, 5], [0, 1, 2]): 
            # 3: cp 1500, 4: stardust, 5: candy
            assert calc['great_league'][i] == gg['great_league'][ig]
        for j, jg in zip([0, 2, 3], [0, 1, 2]):
            # 0: cp 2500, 2: stardust, 3: candy
            assert calc['ultra_league'][j] == gg['ultra_league'][jg]
        for k, kg in zip([0, 2, 3], [0, 1, 2]):
            # 0: cp 2500, 2: stardust, 3: candy
            assert calc['master_league'][k] == gg['master_league'][kg]

