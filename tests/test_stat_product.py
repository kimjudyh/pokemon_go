from ..scripts.stat_product import create_table, calc_stat_product, get_stat_product
import math as m

def test_azumarill():
    try:
        create_table("azumarill")
        calc_stat_product("azumarill")
    except Exception as e:
        print(e)
    PVP_stats = get_stat_product("azumarill", [8, 15, 15])

    assert PVP_stats[0] == 1
    assert round(PVP_stats[1]) == 2365612
    assert round(PVP_stats[2]) == 100


def test_skarmory():
    try:
        create_table("skarmory")
        calc_stat_product("skarmory")
    except Exception as e:
        print(e)
    PVP_stats = get_stat_product("skarmory", [0, 15, 14])

    assert PVP_stats[0] == 1
    assert round(PVP_stats[1]) == 2153020
    assert round(PVP_stats[2]) == 100


def test_medicham():
    try:
        create_table("medicham")
        calc_stat_product("medicham")
    except Exception as e:
        print(e)
    PVP_stats = get_stat_product("medicham", [15, 15, 15])

    assert PVP_stats[0] == 1
    assert round(PVP_stats[1]) == 1900834
    assert round(PVP_stats[2]) == 100


def test_lanturn():
    try:
        create_table("lanturn")
        calc_stat_product("lanturn")
    except Exception as e:
        print("table exists")
    PVP_stats = get_stat_product("lanturn", [0, 13, 14])

    assert PVP_stats[0] == 1
    assert round(PVP_stats[1]) == 2177678
    assert round(PVP_stats[2]) == 100


def test_bronzong():
    try:
        create_table("bronzong")
        calc_stat_product("bronzong")
    except Exception as e:
        print("table exists")
    PVP_stats = get_stat_product("bronzong", [1, 15, 14])

    assert PVP_stats[0] == 1
    assert round(PVP_stats[1]) == 2050565
    assert round(PVP_stats[2]) == 100

def test_altaria():
    try:
        create_table("altaria")
        calc_stat_product("altaria")
    except Exception as e:
        print("table exists")
    PVP_stats = get_stat_product("altaria", [0,14,15])

    assert PVP_stats[0] == 1
    assert round(PVP_stats[1]) == 2212160
    assert round(PVP_stats[2]) == 100


def test_deoxys_d():
    try:
        create_table("deoxys defense")
        calc_stat_product("deoxys defense")
    except:
        pass
    PVP_stats = get_stat_product("deoxys defense", [0,15,15])

    assert PVP_stats[0] == 1
    assert round(PVP_stats[1]) == 2305927
    assert round(PVP_stats[2]) == 100
















