from sys import argv

def create_table(pokemon, league_name):
    '''
    pokemon: string
    Creates a POSTGRESQL table in specified database named after input pokemon.
    Table has columns: Rank, Stamina IV, Attack IV, Defense IV, Stat Product,
    and Percent of Max.
    '''
    import math as m
    import psycopg2
    from psycopg2 import sql

    # create connection to database mydb
    db = psycopg2.connect(database = "mydb")

    # create cursor to go through database
    cur = db.cursor()

    # convert pokemon string variable into something that can be passed into
    # query as a table name. Append the league name
    table_name = sql.Identifier(pokemon.lower() + "_" + league_name)

    # create new table that is named after pokemon
    cur.execute(sql.SQL(
    '''CREATE TABLE {} 
        (rank   int,
        stam_IV int,
        atk_IV  int,
        def_IV  int,
        stat_product float,
        percent_max float
        )''').format(table_name))

    db.commit()
    db.close()

def calc_stat_product(pokemon, league_name):
    '''
    pokemon: string
    Calculates PVP stat product for all 4096 IV combinations.
    Places results into a POSTGRESQL table in specified database.
    Sorts table by ascending rank/descending stat product..
    '''
    import math as m
    try:
        from ..scripts.multi_poke_v1 import read_cp_mult, read_base_stats
    except:
        from multi_poke_v1 import read_cp_mult, read_base_stats
        
    import psycopg2
    from psycopg2 import sql
    from sys import exit

    # create connection to database mydb
    db = psycopg2.connect(database = "mydb")

    # create cursor to go through database
    cur = db.cursor()

    # convert pokemon string variable into something that can be passed into
    # query as a table name
    table_name = sql.Identifier(pokemon.lower() + "_" + league_name)

    dic_cp_mult = read_cp_mult()

    try:
        base_stats = read_base_stats(pokemon)
    except Exception as e:
        print(e)

    #print(base_stats)

    stam_base = base_stats[0]
    atk_base = base_stats[1]
    def_base = base_stats[2]

    stam_IV = list(range(0,16))
    atk_IV = list(range(0,16))
    def_IV = list(range(0,16))

    if league_name == "GL":
        max_cp = 1500
    elif league_name == "UL":
        max_cp = 2500
    elif league_name == "ML":
        max_cp = 9000
    else:
        print("League name " + league_name + " is invalid")
        exit(1)

    #min_cpm_est = m.sqrt(14990/((atk_base+15)*m.sqrt((def_base+15)*(stam_base+15))))
    #max_cpm_est = m.sqrt(14990/((atk_base+0)*m.sqrt((def_base+0)*(stam_base+0))))
    #print(min_cpm_est)
    #print(max_cpm_est)

    #for key, value in dic_cp_mult.items():
    #    if (value > (min_cpm_est -.02)) and (value < (min_cpm_est)):
    #        min_cpm = value
    #        min_level = key
    #    if (value > (max_cpm_est)) and (value < (max_cpm_est + .02)):
    #        max_cpm = value
    #        max_level = key
    #else:

    # Start at level 1.
    min_level = 1
    min_cpm = dic_cp_mult[min_level]

    #print(min_cpm, "min cp mult")
    #print(max_cpm, "max cp mult")
    #print(min_level)

    stat_product = []
    for i_stam in stam_IV:
        for j_atk in atk_IV:
            for k_def in def_IV:
                S = stam_base + i_stam
                A = atk_base + j_atk
                D = def_base + k_def

                cp = m.floor(.1*A*m.sqrt(D*S)*min_cpm**2)
                if cp <= max_cp:
                    level = min_level
                    while cp <= max_cp and level < 40:
                        level += .5
                        cp_mult = dic_cp_mult[level]
                        cp = m.floor(.1*A*m.sqrt(D*S)*cp_mult**2)
                    if cp > max_cp: # we exit the previous loop when the max cp is exceeded
                        level -= .5
                    cp_mult = dic_cp_mult[level]
                    cp = m.floor(.1*A*m.sqrt(D*S)*cp_mult**2)
                    #print(cp)

                p = m.floor(S*cp_mult)*A*D*cp_mult**2

                # insert IV combo and stat product into pokemon's table
                cur.execute(sql.SQL(
                        '''INSERT INTO {} (stam_IV, atk_IV, def_IV, stat_product,
                        percent_max)
                        VALUES (%s, %s, %s, %s, %s)''').format(table_name),\
                                [i_stam, j_atk, k_def, p, p])


                stat_product.append(p)

    max_p = max(stat_product)
    min_p = min(stat_product)
    print(league_name, "max=", max_p)
    print(league_name, "min=", min_p)
    print(len(stat_product))

    # update percent with stat_product/max stat_product
    cur.execute(sql.SQL(
        '''UPDATE {} SET percent_max = percent_max/(%s)*100''').format(table_name),
        [max_p])

    # sort by stat_product descending and add the rank
    cur.execute(sql.SQL(
        '''WITH temp AS (SELECT *, ROW_NUMBER() OVER(ORDER BY stat_product DESC)
        AS rn FROM {})
        UPDATE {} SET rank = (SELECT rn FROM temp WHERE
        temp.stam_IV = {}.stam_IV AND temp.atk_IV = {}.atk_IV
        AND temp.def_IV = {}.def_IV)''').format(table_name, table_name, table_name,
            table_name, table_name))


    db.commit()
    db.close()

def get_stat_product(pokemon, IV_list, league_name):
    '''
    pokemon: string
    IV_list: list of 3 IVs: [attack IV, defense IV, stamina IV]
    returns PVP_stats: list of [rank, stat product, percent of max]
    '''

    import psycopg2
    from psycopg2 import sql
    import sys

    atk_IV = IV_list[0]
    def_IV = IV_list[1]
    stam_IV = IV_list[2]

    db = psycopg2.connect(database = "mydb")
    cur = db.cursor()
    table_name = sql.Identifier(pokemon.lower() + "_" + league_name)

    cur.execute(sql.SQL(
        '''SELECT rank, stat_product, percent_max FROM {} WHERE
        atk_IV = (%s) AND def_IV = (%s) AND stam_IV = (%s)''').format(table_name),
        [atk_IV, def_IV, stam_IV])

    PVP_stats = cur.fetchall()

    # TODO: if empty table, need to drop table, create, and calc


    try:
        PVP_stats = list(PVP_stats[0])
        db.close()
    except Exception as e:
        print(e)
        print('Empty table, probably')
        print(f'Dropping table for {pokemon}')
        cur.execute(sql.SQL(
            '''DROP TABLE IF EXISTS {}''').format(table_name))
        db.commit()
        db.close()
        sys.exit(0)

    #print("pvp stat product debug", PVP_stats)

    return PVP_stats



if __name__ == "__main__":
    # allow pokemon to be specified from command line:
    # python3 stat_product.py pokemon
    script, pokemon = argv
    # create table if it doesn't exist, calc stat product
    leagues = {"GL":1500,
               "UL":2500,
               "ML":9000}
    try:
        for league, max_cp in leagues.items(): 
            create_table(pokemon, league)
            calc_stat_product(pokemon, league)
    # if table exists, move on
    except Exception as e:
        print(e)
    get_stat_product("medicham", [15,15,15], "GL")
    get_stat_product("medicham", [15,15,15], "UL")
    get_stat_product("medicham", [15,15,15], "ML")
