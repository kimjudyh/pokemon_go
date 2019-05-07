# test function narrow_IV

from multi_poke_v1 import narrow_IV

def test_perfect_stats():
    entry = ['1', 'caterpie', 32, 30, 400, 'wonder', 'attack', 'defense', 'hp', 'exceeds']
    stam_IV, atk_IV, def_IV, is_single, two_stats = narrow_IV(entry)
    assert stam_IV == [15]
    assert atk_IV == [15]
    assert def_IV == [15]
    assert is_single == False
    assert two_stats == ''