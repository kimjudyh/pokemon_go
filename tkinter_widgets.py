from tkinter import *
from tkinter import ttk
from tkinter import filedialog


evo_chosen = StringVar()
evo_entry['values'] = search_db

        # write top 10 to text box
        # set state to normal to enable write permission
        result_box['state'] = 'normal'
        # clear contents of text box
        result_box.delete('1.0', 'end')

        if len(search_db) > 10:
            list_results.set(search_db[0:10])
            for i in range(0,10):
                result_box.insert('end', search_db[i])
                result_box.insert('end', '\n')
        else:
            list_results.set(search_db)
            for result in search_db:
                result_box.insert('end', result)
                result_box.insert('end', '\n')
        result_box['state'] = 'disabled'


evo_entry = ttk.Combobox(mainframe, width=10, textvariable=evo_chosen)
evo_entry.grid(column=2, row=file_row+3, sticky=(W,E))
# initialize evo pokemon choices list as empty
evo_entry['values'] = []
ttk.Label(mainframe, text="Evolution:").grid(column=1, row=file_row+3, sticky=(E))

# make text box that shows top 10 search results
result_box = Text(mainframe, state='disabled', width=15, height=10)
result_box.grid(row=file_row+5, column=1, sticky=(W,E))

