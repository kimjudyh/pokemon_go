# pytest

from multi_poke_v1 import read_stats

def test_read_stats_1():
    pokemon_list = read_stats("./input_files/poke_data_1.csv")
    assert len(pokemon_list) == 6
    assert type(pokemon_list[0][2]) is int
    assert type(pokemon_list[0][3]) is int
    assert type(pokemon_list[0][4]) is int
    assert type(pokemon_list[0][5]) is int
    
def test_read_stats_2():
    pokemon_list = read_stats("./input_files/poke_data_2.csv")
    assert len(pokemon_list) == 20
    assert type(pokemon_list[0][2]) is int
    assert type(pokemon_list[0][3]) is int
    assert type(pokemon_list[0][4]) is int
 
def test_read_stats_3():
    pokemon_list = read_stats("./input_files/poke_data_3.csv")
    assert len(pokemon_list) == 9
    assert type(pokemon_list[0][2]) is int
    assert type(pokemon_list[0][3]) is int
    assert type(pokemon_list[0][4]) is int
 
def test_read_stats_4():
    pokemon_list = read_stats("./input_files/poke_data_4.csv")
    assert len(pokemon_list) == 11
    assert type(pokemon_list[0][2]) is int
    assert type(pokemon_list[0][3]) is int
    assert type(pokemon_list[0][4]) is int
 
#if __name__ == "__main__":
#    test_read_stats()
