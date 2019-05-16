# pytest

from multi_poke_v1 import read_stats

def test_read_stats_1():
    envelope = read_stats("poke_data_1.txt")
    assert len(envelope) == 8
    assert type(envelope[0][2]) is int
    assert type(envelope[0][3]) is int
    assert type(envelope[0][4]) is int
    
def test_read_stats_2():
    envelope = read_stats("poke_data_2.txt")
    assert len(envelope) == 3
    assert type(envelope[0][2]) is int
    assert type(envelope[0][3]) is int
    assert type(envelope[0][4]) is int
 
def test_read_stats_3():
    envelope = read_stats("poke_data_3.txt")
    assert len(envelope) == 13
    assert type(envelope[0][2]) is int
    assert type(envelope[0][3]) is int
    assert type(envelope[0][4]) is int
 
def test_read_stats_4():
    envelope = read_stats("poke_data_4.txt")
    assert len(envelope) == 9
    assert type(envelope[0][2]) is int
    assert type(envelope[0][3]) is int
    assert type(envelope[0][4]) is int
 
#if __name__ == "__main__":
#    test_read_stats()
