import requests
import tkinter as tk
from tkinter import ttk
from collections import defaultdict
import os

# Adds the necessary variables and working directory for the program to run.
os.chdir("C:\\Users\\mxchim2jdesspc\\desktop\\nozzlesearch")

nozzle_dict = {'H16': 'R047-010-035', 'H15': 'R047-007-035', 'S14': 'R07-013-070', 'S13': 'R07-010-070', 'S15': 'R07-018-070', 'S16': 'R07-025-070', 'Y14': 'R19-013-155-S', 'Y57': 'R19-037G-155-S', 'T57': 'R19-037G-155', 'Y58': 'R19-050G-155-S', 'Y59': 'R19-070G-155-S', 'L59': 'R36-070G-260', 'L60': 'R36-100G-260', 'J03': 'J03-H01', 'L58': 'R36-050G-260', 'H17': 'R047-013-035', 'J44': 'J44-H24', 'S12': 'R07-007-070', 'J16': 'J16-H08', 'K59': 'R19-070G-155-M', 'K58': 'R19-050G-155-M', 'K15': 'R19-018-155-M', 'K16': 'R19-025-155-M', 'K60': 'R19-100G-155-M', 'K57': 'R19-037G-155-M', 'J23': 'J23-H08M', 'L15': 'R36-018-260', 'L62': 'R36-200G-260', 'L56': 'R36-025G-260', 'L61': 'R36-150G-260', 'L57': 'R36-037G-260', 'L50': 'R36-100G-180', 'L51': 'R36-150G-180', 'S11': 'R07-004-070', 'T15': 'R19-018-155', 'T16': 'R19-025-155', 'T14': 'R19-013-155', 'T13': 'R19-010-155', 'L14': 'R36-013-260', '95Q': '95Q', 'H31': 'R047-004-037', 'J06': 'J06-H08', 'K18': 'R19-050-155-M', 'K14': 'R19-013-155-M', 'K61': 'R19-150G-155-M', 'J28': 'J28-H08M', 'N3N': 'AA4RE00', 'J34': 'J34-H24', 'K13': 'R19-010-155-M', 'K56': 'R19-025G-155-M', 'L17': 'R36-037-260', 'T17': 'R19-037-155', 'T58': 'R19-050G-155', 'L18': 'R36-050-260', 'T18': 'R19-050-155', 'L16': 'R36-025-260', 'S36': 'R07-025M-070', 'S17': 'R07-037-070', 'T59': 'R19-070G-155', 'T61': 'R19-150G-155', 'T19': 'R19-070-155', 'K17': 'R19-037-155-M', 'H18': 'R047-018-035', 'H35': 'R047-006WRS-037', 'K12': 'R19-007-155-M', 'K19': 'R19-070-155-M', 'S56': 'R07-025G-070', 'L20': 'R36-100-260', 'K20': 'R19-010-155-M', '55Q': '55Q', 'H36': 'R047-011WRM-035', 'L19': 'R36-070-260', 'L49': 'R36-070G-180', 'L13': 'R36-010-260', 'L21': 'R36-150-260'}
machine_list = ["NXT14", "NXT13", "NXT59", "NXT69", "NXT91"]
machine_dict = {'NXT59': 'L212A', 'NXT69': 'L212B', 'NXT14': 'L210', 'NXT13': 'L211', 'NXT91': 'L213B'}
head_dict = {'R047': 'H24', 'R07': 'V12', 'R19': 'H08M', 'R36': 'H01', 'J16': 'Calibracion', 'J23': 'Calibracion', 'J06': 'Calibracion', 'J03': 'Calibracion', 'J44': 'Calibracion'}
nozzle_list = []
data = defaultdict(lambda: defaultdict(list))

def dictionary_counter(data):
    result = {}
    for head_type, nozzle_sizes in data.items():
        result[head_type] = {}
        for nozzle_size, entries in nozzle_sizes.items():
            counts = {}
            for lane, module, slot, flag in entries:
                key = (lane, module)
                if key not in counts:
                    counts[key] = {'amount': 0, 'attention': ""}
                counts[key]['amount'] += 1
                if flag:
                    counts[key]['attention'] = "?"
            result[head_type][nozzle_size] = [
                [lane, module, counts[(lane, module)]['amount'], counts[(lane, module)]['attention']]
                for lane, module in counts
            ]
    return result

def fetch_data():
    global nozzle_list, data, counted_data
    nozzle_list.clear()
    data.clear()
    for machine in machine_list:
        api_url = f"http://mxchim0nxapp04/fujiweb/fujimoni/ui/api/McUnitInfo?Machine={machine}"
        try:
            response = requests.get(api_url, timeout=3)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)
            try:
                response_json = response.json()
            except ValueError:
                # Handle JSON decoding error
                print(f"Error decoding JSON for machine {machine}")
                continue
            if response_json is None:
                print(f"Received None for machine {machine}")
                continue
            unit_info = response_json.get("UnitInfo", {})
            module_list = unit_info.get("Module", [])
            for element in module_list:
                nozzle_station = element.get("NozzleStation", {})
                nozzle_list_data = nozzle_station.get("Nozzle", [])
                for nozzle in nozzle_list_data:
                    serial = nozzle.get("Serial", "").split()[0]
                    nozzle_info = nozzle_dict.get(serial, serial)
                    job_use = nozzle.get('JobUse')
                    nozzle_position = nozzle.get('NzlPosition')
                    element_no = element.get('@No')
                    nozzle_no = nozzle.get('@No')
                    if job_use == '0':
                        nozzle_list.append([nozzle_info, [machine_dict.get(machine, 'unknown'), element_no, nozzle_no, False]])
                    elif job_use == '1' and not nozzle_position:
                        nozzle_list.append([nozzle_info, [machine_dict.get(machine, 'unknown'), element_no, nozzle_no, True]])
        except requests.Timeout:
            # Handle request timeout specifically
            print(f"Request timed out for machine {machine}")
        except requests.RequestException as e:
            # Handle other HTTP request errors
            print(f"Request error for machine {machine}: {e}")

    # Sorts the nozzle list into a layered dictionary data[head_type][nozzle_size]
    for nozzle in nozzle_list:
        nozzle_values = nozzle[0].split('-')
        if len(nozzle_values) == 1:
            nozzle_values = ['R36', nozzle_values[0]]
        head_type = head_dict.get(nozzle_values[0], nozzle_values[0])
        nozzle_size = nozzle_values[1]
        data[head_type][nozzle_size].extend(nozzle[1:])
    
    counted_data = dictionary_counter(data)
    update_combobox1()

def update_combobox1():
    combobox1['values'] = list(counted_data.keys())
    if combobox1.get():
        update_second()

def update_second(event=None):
    subkeys = list(counted_data.get(combobox1.get(), {}).keys())
    combobox2['values'] = subkeys

def show_table():
    key1 = combobox1.get()
    key2 = combobox2.get()
    table_data = counted_data.get(key1, {}).get(key2, [])
    for widget in frame.winfo_children():
        widget.destroy()
    ttk.Label(frame, text="Linea").grid(row=0, column=0)
    ttk.Label(frame, text="Modulo").grid(row=0, column=1)
    ttk.Label(frame, text="Cantidad").grid(row=0, column=2)
    ttk.Label(frame, text="").grid(row=0, column=3)
    for i, sublist in enumerate(table_data):
        ttk.Label(frame, text=sublist[0]).grid(row=i+1, column=0)
        ttk.Label(frame, text=sublist[1]).grid(row=i+1, column=1)
        ttk.Label(frame, text=sublist[2]).grid(row=i+1, column=2)
        ttk.Label(frame, text=sublist[3]).grid(row=i+1, column=3)

def update_every_minute():
    fetch_data()
    root.after(30000, update_every_minute)

# GUI setup
root = tk.Tk()
root.title("Buscador de Nozzles")
root.minsize(width=300, height=400)

ttk.Label(root, text="Cabeza").pack(pady=10)
combobox1 = ttk.Combobox(root, state="readonly")
combobox1.pack()
combobox1.bind("<<ComboboxSelected>>", update_second)

ttk.Label(root, text="Tipo").pack(pady=10)
combobox2 = ttk.Combobox(root, state="readonly")
combobox2.pack()

ttk.Button(root, text="Buscar", command=show_table).pack(pady=10)
frame = ttk.Frame(root)
frame.pack(pady=10)

# Initial fetch and setup
fetch_data()
update_combobox1()

# Start the periodic update
root.after(30000, update_every_minute)  # Start the updates every minute

root.mainloop()



	
