import requests
import tkinter as tk
from tkinter import ttk
from collections import Counter
from datetime import datetime
import os 
# Adds the necessary variables and working directory for the program to run.
os.chdir("C:\\Users\\mxchim2jdesspc\\desktop\\nozzlesearch")
nozzle_dict = {'H16': 'R047-010-035', 'H15': 'R047-007-035', 'S14': 'R07-013-070', 'S13': 'R07-010-070', 'S15': 'R07-018-070', 'S16': 'R07-025-070', 'Y14': 'R19-013-155-S', 'Y57': 'R19-037G-155-S', 'T57': 'R19-037G-155', 'Y58': 'R19-050G-155-S', 'Y59': 'R19-070G-155-S', 'L59': 'R36-070G-260', 'L60': 'R36-100G-260', 'J03': 'J03-H01', 'L58': 'R36-050G-260', 'H17': 'R047-013-035', 'J44': 'J44-H24', 'S12': 'R07-007-070', 'J16': 'J16-H08', 'K59': 'R19-070G-155-M', 'K58': 'R19-050G-155-M', 'K15': 'R19-018-155-M', 'K16': 'R19-025-155-M', 'K60': 'R19-100G-155-M', 'K57': 'R19-037G-155-M', 'J23': 'J23-H08M', 'L15': 'R36-018-260', 'L62': 'R36-200G-260', 'L56': 'R36-025G-260', 'L61': 'R36-150G-260', 'L57': 'R36-037G-260', 'L50': 'R36-100G-180', 'L51': 'R36-150G-180', 'S11': 'R07-004-070', 'T15': 'R19-018-155', 'T16': 'R19-025-155', 'T14': 'R19-013-155', 'T13': 'R19-010-155', 'L14': 'R36-013-260', '95Q': '95Q', 'H31': 'R047-004-037', 'J06': 'J06-H08', 'K18': 'R19-050-155-M', 'K14': 'R19-013-155-M', 'K61': 'R19-150G-155-M', 'J28': 'J28-H08M', 'N3N': 'AA4RE00', 'J34': 'J34-H24', 'K13': 'R19-010-155-M', 'K56': 'R19-025G-155-M', 'L17': 'R36-037-260', 'T17': 'R19-037-155', 'T58': 'R19-050G-155', 'L18': 'R36-050-260', 'T18': 'R19-050-155', 'L16': 'R36-025-260', 'S36': 'R07-025M-070', 'S17': 'R07-037-070', 'T59': 'R19-070G-155', 'T61': 'R19-150G-155', 'T19': 'R19-070-155', 'K17': 'R19-037-155-M', 'H18': 'R047-018-035', 'H35': 'R047-006WRS-037', 'K12': 'R19-007-155-M', 'K19': 'R19-070-155-M', 'S56': 'R07-025G-070', 'L20': 'R36-100-260', 'K20': 'R19-010-155-M', '55Q': '55Q'}
machine_list = ["NXT59", "NXT69", "NXT91", "NXT14", "NXT13"]
machine_dict = {'NXT59': 'L212A', 'NXT69': 'L212B', 'NXT14': 'L210', 'NXT13': 'L211'}
head_dict = {'R047': 'H24', 'R07': 'V12', 'R19': 'H08M', 'R36': 'H01', 'J16': 'Calibracion', 'J23': 'Calibracion', 'J06': 'Calibracion', 'J03': 'Calibracion', 'J44': 'Calibracion'}
nozzle_list = []
data = {}
# Searches for all the Nozzles that are not in use for the current job and adds them to a list. 
for machine in machine_list: 
	api_url = f"http://mxchim0nxapp04/fujiweb/fujimoni/ui/api/McUnitInfo?Machine={machine}"
	response = requests.get(api_url)
	if 200 <= response.status_code < 300:
		response_json = response.json()
	else:
		print(f"GET request to {machine} raised {response.status_code}. The program will continue to next machine.")
		continue
	for element in response_json["UnitInfo"]["Module"]:
		if "NozzleStation" in element:
			nozzle_holder = element["NozzleStation"]
			if "Nozzle" in nozzle_holder:
				for nozzle in element["NozzleStation"]["Nozzle"]:
					if nozzle['JobUse'] == '0':
						serial = nozzle["Serial"].split()
						if serial[0] in nozzle_dict:
							nozzle_list.append([nozzle_dict[serial[0]], [machine_dict[machine], element["@No"], nozzle['@No']]])
						else:
							nozzle_list.append([serial[0], [machine_dict[machine], element["@No"], nozzle['@No']]])
# Sorts the nozzle list into a layered dictionary data[head_type][nozzle_size]
for nozzle in nozzle_list:
    nozzle_values = nozzle[0].split('-')
    if len(nozzle_values) == 1:
        nozzle_values.append(nozzle_values[0])
        nozzle_values[0] = 'R36'
    if nozzle_values[0] in head_dict:
        head_type = head_dict[nozzle_values[0]]
    else:
        head_type = nozzle_values[0]
    nozzle_size = nozzle_values[1]
    if head_type in data:
        if nozzle_size in data[head_type]:
            data[head_type][nozzle_size].extend(nozzle[1:])
        else:
            data[head_type][nozzle_size] = nozzle[1:]
    else:
        data[head_type] = {}
        data[head_type][nozzle_size] = nozzle[1:]

# Initialize tkinter
root = tk.Tk()
root.title("Buscador de Nozzles")
root.minsize(width=300, height=400)

# Function to populate the second combobox based on selection from the first combobox
def update_second(event):
    subkeys = list(data[combobox1.get()].keys())
    combobox2['values'] = subkeys

# Function to display the table
def show_table():
    key1 = combobox1.get()
    key2 = combobox2.get()
    table_data = data[key1][key2]

    # Clear previous table if exists
    for widget in frame.winfo_children():
        widget.destroy()

    # Create table headers
    ttk.Label(frame, text="Linea").grid(row=0, column=0)
    ttk.Label(frame, text="Modulo").grid(row=0, column=1)
    ttk.Label(frame, text="Slot").grid(row=0, column=2)

    # Display table data
    for i, sublist in enumerate(table_data):
        ttk.Label(frame, text=sublist[0]).grid(row=i+1, column=0)
        ttk.Label(frame, text=sublist[1]).grid(row=i+1, column=1)
        ttk.Label(frame, text=sublist[2]).grid(row=i+1, column=2)

# Create and place widgets
# First combobox for selecting first level key
ttk.Label(root, text="Type").pack(pady=10)
combobox1 = ttk.Combobox(root, values=list(data.keys()), state="readonly")
combobox1.pack()
combobox1.bind("<<ComboboxSelected>>", update_second)

# Second combobox for selecting second level key
ttk.Label(root, text="Size").pack(pady=10)
combobox2 = ttk.Combobox(root, state="readonly")
combobox2.pack()

# Button to show the table
ttk.Button(root, text="Buscar", command=show_table).pack(pady=10)

# Frame to hold the table
frame = ttk.Frame(root)
frame.pack(pady=10)

# Start the tkinter main loop
root.mainloop()


	
