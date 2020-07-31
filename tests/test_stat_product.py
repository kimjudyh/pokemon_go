from ..scripts.stat_product import create_table, calc_stat_product, get_stat_product
from ..scripts.multi_poke_v1 import read_cp_mult, read_base_stats
import math as m

def test_azumarill():
    try:
        create_table("azumarill", "GL")
        calc_stat_product("azumarill", "GL")
    except Exception as e:
        print(e)
    PVP_stats = get_stat_product("azumarill", [8, 15, 15], "GL")

    assert PVP_stats[0] == 1
    assert round(PVP_stats[1]) == 2365612
    assert round(PVP_stats[2]) == 100


def test_skarmory():
    try:
        create_table("skarmory", "GL")
        calc_stat_product("skarmory", "GL")
    except Exception as e:
        print(e)
    PVP_stats = get_stat_product("skarmory", [0, 15, 14], "GL")

    assert PVP_stats[0] == 1
    assert round(PVP_stats[1]) == 2153020
    assert round(PVP_stats[2]) == 100


def test_medicham():
    try:
        create_table("medicham", "GL")
        calc_stat_product("medicham", "GL")
    except Exception as e:
        print(e)
    PVP_stats = get_stat_product("medicham", [15, 15, 15], "GL")

    assert PVP_stats[0] == 1
    assert round(PVP_stats[1]) == 1900834
    assert round(PVP_stats[2]) == 100


def test_lanturn():
    try:
        create_table("lanturn", "GL")
        calc_stat_product("lanturn", "GL")
    except Exception as e:
        print("table exists")
    PVP_stats = get_stat_product("lanturn", [0, 13, 14], "GL")

    assert PVP_stats[0] == 1
    assert round(PVP_stats[1]) == 2177678
    assert round(PVP_stats[2]) == 100


def test_bronzong():
    try:
        create_table("bronzong", "GL")
        calc_stat_product("bronzong", "GL")
    except Exception as e:
        print("table exists")
    PVP_stats = get_stat_product("bronzong", [1, 15, 14], "GL")

    assert PVP_stats[0] == 1
    assert round(PVP_stats[1]) == 2050565
    assert round(PVP_stats[2]) == 100

def test_altaria():
    try:
        create_table("altaria", "GL")
        calc_stat_product("altaria", "GL")
    except Exception as e:
        print("table exists")
    PVP_stats = get_stat_product("altaria", [0,14,15], "GL")

    assert PVP_stats[0] == 1
    assert round(PVP_stats[1]) == 2212160
    assert round(PVP_stats[2]) == 100


def test_deoxys_d():
    try:
        create_table("deoxys defense", "GL")
        calc_stat_product("deoxys defense", "GL")
    except:
        pass
    PVP_stats = get_stat_product("deoxys defense", [0,15,15], "GL")

    assert PVP_stats[0] == 1
    assert round(PVP_stats[1]) == 2305927
    assert round(PVP_stats[2]) == 100


def test_clefable():
    try:
        create_table("clefable", "UL")
        calc_stat_product("clefable", "UL")
    except:
        pass
    PVP_stats = get_stat_product("clefable", [13,13,14], "UL")

    assert round(PVP_stats[1]) == 3778626
    assert round(PVP_stats[2]) == 97


def test_togekiss():
    try:
        create_table("togekiss", "UL")
        calc_stat_product("togekiss", "UL")
    except:
        pass
    PVP_stats = get_stat_product("togekiss", [10,12,14], "UL")

    assert round(PVP_stats[1]) == 3811706
    assert round(PVP_stats[2]) == 97


def test_mewtwo():
    try:
        create_table("mewtwo", "ML")
        calc_stat_product("mewtwo", "ML")
    except:
        pass
    PVP_stats = get_stat_product("mewtwo", [15,15,15], "ML")

    assert PVP_stats[0] == 1
    assert round(PVP_stats[1]) == 6976430
    assert round(PVP_stats[2]) == 100


def test_dialga():
    try:
        create_table("dialga", "ML")
        calc_stat_product("dialga", "ML")
    except:
        pass
    PVP_stats = get_stat_product("dialga", [15,15,15], "ML")

    assert round(PVP_stats[1]) == 7081684
    assert round(PVP_stats[2]) == 100


def test_groudon():
    try:
        create_table("groudon", "ML")
        calc_stat_product("groudon", "ML")
    except:
        pass
    PVP_stats = get_stat_product("groudon", [15,15,15], "ML")

    assert round(PVP_stats[1]) == 7483094
    assert round(PVP_stats[2]) == 100







