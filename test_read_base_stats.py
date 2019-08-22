# test function read_base_stats

from multi_poke_v1 import read_base_stats

def test_meltan():
    base_stats = read_base_stats("meltan")

    assert base_stats[0] == 130
    assert base_stats[1] == 118
    assert base_stats[2] == 99

def test_skarmory():
    base_stats = read_base_stats("skarmory")
    
    assert base_stats[0] == 163
    assert base_stats[1] == 148
    assert base_stats[2] == 226



    
