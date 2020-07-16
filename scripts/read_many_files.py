import multi_poke_v1
from sys import argv

# the idea is that multiple csv files are to be read in one go
# the csv files contain one pokemon type, but can differ from each other

# how to use:
# $ python3 read_many_files.py poke1.csv poke2.csv poke3.csv

# option 1: only files specified
# argv = [useless string, file1, file2, file3, ...]

# option 2: 1 file, 1 evo poke specified
# argv = [useless string, evo poke, file1]
print(argv)

for key, value in enumerate(argv):
    if key == 0:
        continue
    elif "csv" not in value:
        continue
    else:
        print("file: ", value)
        poke_file = multi_poke_v1.file_input(value)
        multi_poke_v1.main()
        print("done")




