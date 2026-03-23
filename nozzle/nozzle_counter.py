import os
import requests
from collections import Counter
from datetime import datetime

# Import the configuration
from nozzle_mapping import MACHINE_LIST, NOZZLE_DICT

# ==========================================
# ETL PIPELINE FUNCTIONS
# ==========================================

def extract_telemetry(machines):
    """(Extract) Pulls live nozzle data from the REST APIs of the target machines."""
    raw_nozzles = []
    
    for machine in machines:
        api_url = f"http://yourserveraddress/fujiweb/fujimoni/ui/api/McUnitInfo?Machine={machine}"
        
        try:
            response = requests.get(api_url, timeout=10) # Added timeout to prevent infinite hangs
            if 200 <= response.status_code < 300:
                response_json = response.json()
            else:
                print(f"GET request to {machine} raised {response.status_code}. Press any key to continue to next machine.")
                input()
                continue
        except requests.RequestException as e:
            print(f"Network error when reaching {machine}: {e}. Press any key to continue.")
            input()
            continue

        # Parse nested JSON for nozzle serials
        nozzles = []
        for element in response_json.get("UnitInfo", {}).get("Module", []):
            if "NozzleStation" in element:
                nozzle_holder = element["NozzleStation"]
                if "Nozzle" in nozzle_holder:
                    nozzles.append(nozzle_holder["Nozzle"])
                    
        for element in nozzles:
            for nozzle in element:
                serial = nozzle.get("Serial", "").split()
                if serial:
                    raw_nozzles.append(serial[0])
                    
    return raw_nozzles

def transform_data(raw_nozzle_list):
    """(Transform) Aggregates counts and maps internal codes to human-readable SKUs."""
    nozzle_counter = dict(Counter(raw_nozzle_list))
    mapped_dict = {}
    unnamed_counter = 0

    # Translate codes to SKUs
    for key, count in nozzle_counter.items():
        if key in NOZZLE_DICT:
            mapped_dict[NOZZLE_DICT[key]] = count
        else:
            mapped_dict[key] = count
            unnamed_counter += 1

    # Sort dictionary alphabetically by SKU name
    sorted_dict = sorted(mapped_dict.items(), key=lambda x: x[0], reverse=True)

    # Format as CSV string
    csv_string = 'Nozzle,Cantidad\n'
    for item in sorted_dict:
        csv_string += f"{item[0]},{item[1]}\n"
        
    return csv_string

def load_report(csv_string):
    """(Load) Saves the generated report to the local file system."""
    current_date = datetime.now().strftime('%Y-%m-%d %H-%M')
    file_path = f'./Reports/Nozzle Report {current_date}.txt'
    
    # Ensure the Reports directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, 'w') as file:
        file.write(csv_string)
        
    print(f"\nReport successfully saved to: {file_path}")

# ==========================================
# MAIN EXECUTION
# ==========================================

def main():
    # Dynamically set working directory to the script's location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("Initiating IoT Hardware Audit...")
    
    # 1. Extract
    print(f"Pinging {len(MACHINE_LIST)} machines for telemetry...")
    raw_data = extract_telemetry(MACHINE_LIST)
    
    if not raw_data:
        print("No data extracted. Exiting.")
        return

    # 2. Transform
    print("Mapping internal machine codes to inventory SKUs...")
    final_csv_data = transform_data(raw_data)
    
    # 3. Load
    load_report(final_csv_data)
    
    print('\nProgram finished running. Press any key to close.')
    input()

if __name__ == "__main__":
    main()
