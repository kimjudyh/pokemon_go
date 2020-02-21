#!/bin/bash

psql mydb -c 'drop table base_stats'
psql mydb -c 'create table base_stats(id varchar, species varchar, hp int, attack int, defense int);'
psql mydb -c "\copy base_stats FROM 'pogostats_csv.csv' (format csv, header true);"
