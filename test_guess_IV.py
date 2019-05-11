# test function guess_IV

from multi_poke_v1 import guess_IV, narrow_IV, read_stardust, read_base_stats,\
    read_cp_mult, narrow_cp_mult

def run_functions(entry):
    dic_cp_mult = read_cp_mult()
    dic_stardust = read_stardust()
    base_stats = read_base_stats()
    d_list_levels, cp_mult = narrow_cp_mult(dic_cp_mult, dic_stardust, entry)
    stam_IV, atk_IV, def_IV, is_single = narrow_IV(entry)
    for poke in base_stats:
        if poke[0] == entry[1]:
            t_base_stats = poke[1:]
    IV = guess_IV(cp_mult, stam_IV, atk_IV, def_IV, t_base_stats, entry, d_list_levels, is_single)
    return IV

def test_meltan_3():
    entry = ['3', 'meltan', 362, 64, 1600, 'above average', 'attack', 'noticeably']
    IV = run_functions(entry)

    #IV: [[i_lvl, i_stam, j_atk, k_def, IV_percent]]

    assert len(IV) == 1
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 13.0
    assert i_stam == 4
    assert j_atk == 12
    assert k_def == 9

def test_bagon_5():
    entry = ['5', 'bagon', 896, 102, 5000, 'above average', 'hp', 'attack', 'noticeably']
    IV = run_functions(entry)
    assert len(IV) == 1
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 30.0
    assert i_stam == 12
    assert j_atk == 12
    assert k_def == 1

def test_bagon_7():
    entry = ['7', 'bagon', 846, 95, 5000, 'not likely', 'attack', 'noticeably']
    IV = run_functions(entry)
    assert len(IV) == 2
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 29.0
    assert i_stam == 5
    assert j_atk == 10
    assert k_def == 4
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[1]
    assert i_lvl == 30.0
    assert i_stam == 2
    assert j_atk == 9
    assert k_def == 1

def test_bagon_8():
    entry = ['8', 'bagon', 841, 97, 5000, 'not likely', 'defense', 'noticeably']
    IV = run_functions(entry)
    assert len(IV) == 3
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 29.0
    assert i_stam == 8
    assert j_atk == 2
    assert k_def == 12
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[1]
    assert i_lvl == 29.0
    assert i_stam == 8
    assert j_atk == 4
    assert k_def == 9
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[2]
    assert i_lvl == 30.0
    assert i_stam == 5
    assert j_atk == 1
    assert k_def == 9

def test_charmander_2():
    '''
    testing this charmander because: single stat (defense), but hp and attack
    are equal
    '''
    entry = ['2', 'charmander', 284, 55, 1300, 'certainly', 'defense', 'exceeds']
    IV = run_functions(entry)
    assert len(IV) == 1
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 11.0
    assert i_stam == 8
    assert j_atk == 8
    assert k_def == 15
 
'''
if __name__ == "__main__":
    test_meltan_3()
    test_bagon_5()
    test_bagon_7()
    test_bagon_8()
    '''
