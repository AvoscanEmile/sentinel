"""
nozzle_mapping.py
Single Source of Truth for Fuji NXT API translations.
"""

# List the machines to be watched, these are just examples.
MACHINE_LIST = ["NXT14", "NXT13", "NXT59", "NXT69", "NXT91"]

# Maps internal machine IP/Name to physical factory lane
MACHINE_DICT = {
    'NXT59': 'ExampleLine1', 
    'NXT69': 'ExampleLine2', 
    'NXT14': 'ExampleLine3', 
    'NXT13': 'ExampleLine4', 
    'NXT91': 'ExampleLine5'
}

# Maps nozzle prefix to physical Head Type or Nozzle type
HEAD_DICT = {
    'R047': 'H24', 
    'R07': 'V12', 
    'R19': 'H08M', 
    'R36': 'H01', 
    'J16': 'Calibracion', 
    'J23': 'Calibracion', 
    'J06': 'Calibracion', 
    'J03': 'Calibracion', 
    'J44': 'Calibracion'
}

# Maps serial number prefixes on the nozzles to the HEADTYPE-SIZE-DETAILS-DETAILS mapping. 
NOZZLE_DICT = {
    'H16': 'R047-010-035', 'H15': 'R047-007-035', 'S14': 'R07-013-070', 'S13': 'R07-010-070', 
    'S15': 'R07-018-070', 'S16': 'R07-025-070', 'Y14': 'R19-013-155-S', 'Y57': 'R19-037G-155-S', 
    'T57': 'R19-037G-155', 'Y58': 'R19-050G-155-S', 'Y59': 'R19-070G-155-S', 'L59': 'R36-070G-260', 
    'L60': 'R36-100G-260', 'J03': 'J03-H01', 'L58': 'R36-050G-260', 'H17': 'R047-013-035', 
    'J44': 'J44-H24', 'S12': 'R07-007-070', 'J16': 'J16-H08', 'K59': 'R19-070G-155-M', 
    'K58': 'R19-050G-155-M', 'K15': 'R19-018-155-M', 'K16': 'R19-025-155-M', 'K60': 'R19-100G-155-M', 
    'K57': 'R19-037G-155-M', 'J23': 'J23-H08M', 'L15': 'R36-018-260', 'L62': 'R36-200G-260', 
    'L56': 'R36-025G-260', 'L61': 'R36-150G-260', 'L57': 'R36-037G-260', 'L50': 'R36-100G-180', 
    'L51': 'R36-150G-180', 'S11': 'R07-004-070', 'T15': 'R19-018-155', 'T16': 'R19-025-155', 
    'T14': 'R19-013-155', 'T13': 'R19-010-155', 'L14': 'R36-013-260', '95Q': '95Q', 
    'H31': 'R047-004-037', 'J06': 'J06-H08', 'K18': 'R19-050-155-M', 'K14': 'R19-013-155-M', 
    'K61': 'R19-150G-155-M', 'J28': 'J28-H08M', 'N3N': 'AA4RE00', 'J34': 'J34-H24', 
    'K13': 'R19-010-155-M', 'K56': 'R19-025G-155-M', 'L17': 'R36-037-260', 'T17': 'R19-037-155', 
    'T58': 'R19-050G-155', 'L18': 'R36-050-260', 'T18': 'R19-050-155', 'L16': 'R36-025-260', 
    'S36': 'R07-025M-070', 'S17': 'R07-037-070', 'T59': 'R19-070G-155', 'T61': 'R19-150G-155', 
    'T19': 'R19-070-155', 'K17': 'R19-037-155-M', 'H18': 'R047-018-035', 'H35': 'R047-006WRS-037', 
    'K12': 'R19-007-155-M', 'K19': 'R19-070-155-M', 'S56': 'R07-025G-070', 'L20': 'R36-100-260', 
    'K20': 'R19-010-155-M', '55Q': '55Q', 'H36': 'R047-011WRM-035', 'L19': 'R36-070-260', 
    'L49': 'R36-070G-180', 'L13': 'R36-010-260', 'L21': 'R36-150-260'
}
