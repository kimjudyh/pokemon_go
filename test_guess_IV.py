# test function guess_IV

from multi_poke_v1 import guess_IV, narrow_IV, read_stardust, read_base_stats,\
    read_cp_mult, narrow_cp_mult

def run_functions(entry):
    dic_cp_mult = read_cp_mult()
    dic_stardust = read_stardust()
    #base_stats = read_base_stats()
    d_list_levels, cp_mult = narrow_cp_mult(dic_cp_mult, dic_stardust, entry)
    stam_IV, atk_IV, def_IV, is_single = narrow_IV(entry)
    pokemon = entry[1]
    t_base_stats = read_base_stats(pokemon)
    #for poke in base_stats:
    #    if poke[0] == entry[1]:
    #        t_base_stats = poke[1:]
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

def test_bagon_1():
    entry = ['1', 'bagon', 932, 102, 5000, 'certainly', 'attack', 'certainly impressed']
    IV = run_functions(entry)
    assert len(IV) == 1
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 30.0
    assert i_stam == 12
    assert j_atk == 14
    assert k_def == 6

def test_bagon_2():
    entry = ['2', 'bagon', 913, 102, 5000, 'wonder', 'hp', 'exceeds']
    IV = run_functions(entry)
    assert len(IV) == 1
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 29.0
    assert i_stam == 15
    assert j_atk == 10
    assert k_def == 12

def test_bagon_3():
    entry = ['3', 'bagon', 908, 94, 5000, 'above average', 'attack', 'certainly impressed']
    IV = run_functions(entry)
    assert len(IV) == 1
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 30.0
    assert i_stam == 1
    assert j_atk == 14
    assert k_def == 9

def test_bagon_4():
    entry = ['4', 'bagon', 897, 97, 5000, 'certainly', 'attack', 'certainly impressed']
    IV = run_functions(entry)
    assert len(IV) == 2
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 29.0
    assert i_stam == 7
    assert j_atk == 13
    assert k_def == 10
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[1]
    assert i_lvl == 29.0
    assert i_stam == 8
    assert j_atk == 14
    assert k_def == 8

def test_bagon_5():
    entry = ['5', 'bagon', 896, 102, 5000, 'above average', 'hp', 'attack', 'noticeably']
    IV = run_functions(entry)
    assert len(IV) == 1
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 30.0
    assert i_stam == 12
    assert j_atk == 12
    assert k_def == 1

def test_bagon_6():
    entry = ['6', 'bagon', 875, 92, 4500, 'certainly', 'attack', 'defense', 'certainly impressed']
    IV = run_functions(entry)
    assert len(IV) == 1
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 28.0
    assert i_stam == 3
    assert j_atk == 14
    assert k_def == 14


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

def test_bagon_9():
    entry = ['9', 'bagon', 841, 94, 5000, 'not likely', 'defense', 'certainly impressed']
    IV = run_functions(entry)
    assert len(IV) == 1
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 29.0
    assert i_stam == 3
    assert j_atk == 4
    assert k_def == 13


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
 
def test_meltan_1():
    entry = ['1', 'meltan', 396, 70, 1900, 'not likely', 'defense', 'certainly impressed']
    IV = run_functions(entry)
    assert len(IV) == 2
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 15.0
    assert i_stam == 6 
    assert j_atk == 2
    assert k_def == 13
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[1]
    assert i_lvl == 15.0
    assert i_stam == 7
    assert j_atk == 1
    assert k_def == 14

def test_meltan_2():
    entry = ['2', 'meltan', 382, 73, 1900, 'not likely', 'hp', 'certainly impressed']
    IV = run_functions(entry)
    assert len(IV) == 2
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 15.0
    assert i_stam == 13 
    assert j_atk == 1
    assert k_def == 2
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[1]
    assert i_lvl == 15.0
    assert i_stam == 13
    assert j_atk == 2
    assert k_def == 0

def test_meltan_3():
    entry = ['3', 'meltan', 362, 64, 1600, 'above average', 'attack', 'noticeably']
    IV = run_functions(entry)
    assert len(IV) == 1
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 13.0
    assert i_stam == 4 
    assert j_atk == 12
    assert k_def == 9

def test_meltan_4():
    entry = ['4', 'meltan', 838, 95, 5000, 'above average', 'attack', 'certainly impressed']
    IV = run_functions(entry)
    assert len(IV) == 2
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 30.0
    assert i_stam == 0 
    assert j_atk == 13
    assert k_def == 11
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[1]
    assert i_lvl == 30.0
    assert i_stam == 1
    assert j_atk == 13
    assert k_def == 10

def test_meltan_5():
    entry = ['5', 'meltan', 823, 98, 5000, 'not likely', 'attack', 'noticeably']
    IV = run_functions(entry)
    assert len(IV) == 1
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 30.0
    assert i_stam == 4 
    assert j_atk == 11
    assert k_def == 7

def test_meltan_6():
    entry = ['6', 'meltan', 784, 101, 4500, 'certainly', 'defense', 'exceeds']
    IV = run_functions(entry)
    assert len(IV) == 1
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 28.0
    assert i_stam == 13 
    assert j_atk == 5
    assert k_def == 15
    
def test_meltan_7():
    entry = ['7', 'meltan', 727, 96, 5000, 'not likely', 'hp', 'attack', 'norm']
    IV = run_functions(entry)
    assert len(IV) == 1
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 29.0
    assert i_stam == 4 
    assert j_atk == 4
    assert k_def == 0

def test_meltan_8():
    entry = ['8', 'meltan', 711, 96, 4000, 'certainly', 'hp', 'defense', 'exceeds']
    IV = run_functions(entry)
    assert len(IV) == 1
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 25.0
    assert i_stam == 15 
    assert j_atk == 6
    assert k_def == 15

def test_meltan_9():
    entry = ['9', 'meltan', 683, 95, 4000, 'not likely', 'hp', 'noticeably']
    IV = run_functions(entry)
    assert len(IV) == 2
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[0]
    assert i_lvl == 26.0
    assert i_stam == 10 
    assert j_atk == 3
    assert k_def == 7
    i_lvl, i_stam, j_atk, k_def, IV_percent = IV[1]
    assert i_lvl == 26.0
    assert i_stam == 10
    assert j_atk == 4
    assert k_def == 5





'''
if __name__ == "__main__":
    test_meltan_3()
    test_bagon_5()
    test_bagon_7()
    test_bagon_8()
    '''
