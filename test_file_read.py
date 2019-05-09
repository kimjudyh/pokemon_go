# pytest

from multi_poke_v1 import read_stats

def test_read_stats():
    envelope = read_stats("poke_data_4.txt")
    assert len(envelope) == 9
    assert type(envelope[0][2]) is int
    assert type(envelope[0][3]) is int
    assert type(envelope[0][4]) is int
    

if __name__ == "__main__":
    test_read_stats()
