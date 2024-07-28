import requests
from collections import Counter
from pydrive.drive import GoogleDrive 
from pydrive.auth import GoogleAuth 
import os 
os.chdir("C:\\Users\\mxchim2jdesspc\\desktop\\nozzlecounter")
nozzle_dict = {'H16': 'R047-010-035', 'H15': 'R047-007-035', 'S14': 'R07-013-070', 'S13': 'R07-010-070', 'S15': 'R07-018-070', 'S16': 'R07-025-070', 'Y14': 'R19-013-155-S', 'Y57': 'R19-037G-155-S', 'T57': 'R19-037G-155', 'Y58': 'R19-050G-155-S', 'Y59': 'R19-070G-155-S', 'L59': 'R36-070G-260', 'L60': 'R36-100G-260', 'J03': 'J03-H01', 'L58': 'R36-050G-260', 'H17': 'R047-013-035', 'J44': 'J44-H24', 'S12': 'R07-007-070', 'J16': 'J16-H08', 'K59': 'R19-070G-155-M', 'K58': 'R19-050G-155-M', 'K15': 'R19-018-155-M', 'K16': 'R19-025-155-M', 'K60': 'R19-100G-155-M', 'K57': 'R19-037G-155-M', 'J23': 'J23-H08M', 'L15': 'R36-018-260', 'L62': 'R36-200G-260', 'L56': 'R36-025G-260', 'L61': 'R36-150G-260', 'L57': 'R36-037G-260', 'L50': 'R36-100G-180', 'L51': 'R36-150G-180', 'S11': 'R07-004-070', 'T15': 'R19-018-155', 'T16': 'R19-025-155', 'T14': 'R19-013-155', 'T13': 'R19-010-155', 'L14': 'R36-013-260', '95Q': '95Q', 'H31': 'R047-004-037', 'J06': 'J06-H08', 'K18': 'R19-050-155-M', 'K14': 'R19-013-155-M', 'K61': 'R19-150G-155-M', 'J28': 'J28-H08M', 'N3N': 'AA4RE00', 'J34': 'J34-H24', 'K13': 'R19-010-155-M', 'K56': 'R19-025G-155-M', 'L17': 'R36-037-260', 'T17': 'R19-037-155', 'T58': 'R19-050G-155', 'L18': 'R36-050-260', 'T18': 'R19-050-155', 'L16': 'R36-025-260', 'S36': 'R07-025M-070', 'S17': 'R07-037-070', 'T59': 'R19-070G-155', 'T61': 'R19-150G-155', 'T19': 'R19-070-155', 'K17': 'R19-037-155-M', 'H18': 'R047-018-035', 'H35': 'R047-006WRS-037'}
machine_list = ["NXT59", "NXT69", "NXT91", "NXT14", "NXT13"]
nozzle_list = []
for machine in machine_list: 
	api_url = f"http://mxchim0nxapp04/fujiweb/fujimoni/ui/api/McUnitInfo?Machine={machine}"
	response = requests.get(api_url)
	if 200 <= response.status_code < 300:
		response_json = response.json()
	else:
		print(f"{machine} raised {response.status_code}. The program will continue to next machine.")
		continue
	nozzles = []
	nozzle_holder_counter = 0
	for element in response_json["UnitInfo"]["Module"]:
		nozzle_holder_counter += 1
		if "NozzleStation" in element:
			nozzle_holder = element["NozzleStation"]
			print(machine, nozzle_holder_counter, nozzle_holder, end="\n\n")
			if "Nozzle" in nozzle_holder:
				nozzles.append(element["NozzleStation"]["Nozzle"])
	for element in nozzles:
		for nozzle in element: 
			serial = nozzle["Serial"].split()
			nozzle_list.append(serial[0])
nozzle_counter = dict(Counter(nozzle_list))
last_dict = {}
unnamed_counter = 0
for key in nozzle_counter.keys():
	if key in nozzle_dict:
		last_dict[nozzle_dict[key]] = nozzle_counter[key]
	else:
		last_dict[key] = nozzle_counter[key]
		unnamed_counter += 1
sorted_dict = sorted(last_dict.items(), key=lambda x: x[1], reverse=True)
csv_string = 'Nozzle,Cantidad\n'
for item in sorted_dict:
	csv_string += ','.join([item[0], str(item[1])])
	csv_string += '\n'
input()

	
