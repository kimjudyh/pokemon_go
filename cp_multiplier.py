
def f_cp_mult():
    cp_mult_file = open("cp_mult_data.txt", "r")
    cp_mult_list = cp_mult_file.readlines()
    cp_mult_file.close()

    del(cp_mult_list[0:1])

    dic_cp_mult = {}

    for entry in cp_mult_list:
        x = entry.find("\t")
        y = entry.find("\n")
        if "\n" not in entry:
            dic_cp_mult[entry[0:x]] = float(entry[x+1:])
        else:
            dic_cp_mult[entry[0:x]] = float(entry[x+1:y])

    print(dic_cp_mult)

    print(dic_cp_mult["1"])

    level = 1
    for i in range(0,40,1):
        print(dic_cp_mult[str(level)])
        level += 1

    return dic_cp_mult

d = f_cp_mult()