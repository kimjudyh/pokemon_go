import multi_poke_v1
from sys import argv

# the idea is that multiple csv files are to be read in one go
# the csv files contain one pokemon type, but can differ from each other

print(argv)

for key, value in enumerate(argv):
    if key == 0:
        continue
    else:
        print("file: ", value)
        poke_file = multi_poke_v1.file_input(value)
        multi_poke_v1.main()
        print("done")




