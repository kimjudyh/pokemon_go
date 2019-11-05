# pokemon_go

This repository stores files for calculating the evolution CP and PVP stat product rank for a batch of pokemon.
Pokemon stats (CP, IVs) are written in a CSV file and inputted into the main python file, multi_poke_v1.py.

If multiple CSV files are to be analyzed, read_many_files.py can be used.

Requirements:
Postgresql, psycopg2, python3

## Installation
Install PostgreSQL. Install psycopg2:  
`$ pip install psycopg2`

## Setting up the database
Create a database called `mydb`:  
`$ createdb mydb`

Create a table in the database called `base_stats`  
`$ psql mydb -c 'create table base_stats(id varchar, species varchar, hp int, attack int, defense int);'`

Populate the table with base stats from pogostats_csv.csv  
`$ psql mydb -c "\copy base_stats FROM 'pogostats_csv.csv' (format csv, header true);"`

## Creating the input file
Create a csv file with the following columns: id, pokemon, CP, attack IV, defense IV, stamina IV. Save it in the same directory as multi_poke_v1.py.

It's highly recommended to analyze one type of pokemon. The names of the columns don't matter, but the order does. Refer to bagon1.csv for an example. 

| id | pokemon | CP | Atk IV | Def IV | Stam IV|
| ------ | ------ | ------ | ------ | ------ | ------ |
| 1 | bagon | 327 | 1 | 14 | 15 |


## Running the program
The file name can be changed inside multi_poke_v1.py, or can be called from the command line using read_many_files.py.

Analyzing one file:
`$ python3 read_many_files.py bagon1.csv`

Analyzing many files:
`$ python3 read_many_files.py bagon1.csv bagon2.csv bagon3.csv`

## Specifying the evolution pokemon
The program will ask for an evolution pokemon. Type in the pokemon's name (ex. shelgon) and press enter for the analysis.

## Output in terminal window
* Evolution: evolved pokemon  
* CP: evolution's CP  
* HP: evolution's HP  
* #Pwr^: number of power ups needed for evolved pokemon to reach CP1500  
* CP1500: the highest CP closest to 1500 that the evolved pokemon will reach  
* Rank: Great League PVP rank, based on the stat product  
* Stat Product: a metric for predicting a pokemon's effectiveness in PVP, based on their IVs and base stats  
* Percent of Max: percent of this pokemon's stat product divided by the max stat product  
```
56. Original stats:
CP: 327
|----------|--------|--------|--------|--------|--------|----------|-----|----|-----|------|
| Pokemon  | Level  |  ATK   |  DEF   |  STM   |  IV %  |Evolution | CP  | HP |#Pwr^|CP1500|
|----------|--------|--------|--------|--------|--------|----------|-----|----|-----|------|
|  bagon   |  11.0  |   1    |   14   |   15   | 66.67% | shelgon  | 589 | 78 | 34  | 1499 |
Rank: 7
Stat Product: 1826162.34
Percent of Max: 99.41%
```