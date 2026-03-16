import os
import threading
import requests
import tkinter as tk
from tkinter import ttk
from collections import defaultdict

# Import the shared configuration (Single Source of Truth)
from nozzle_mapping import MACHINE_LIST, MACHINE_DICT, HEAD_DICT, NOZZLE_DICT

class NozzleDashboard(tk.Tk):
    """
    Real-time IoT Desktop Dashboard for Fuji NXT Nozzle Inventory.
    Periodically fetches, transforms, and displays live machine telemetry.
    """
    def __init__(self):
        super().__init__()
        
        # Window Configuration
        self.title("Buscador de Nozzles")
        self.minsize(width=300, height=400)
        
        # Application State
        self.raw_nozzle_list = []
        self.structured_data = defaultdict(lambda: defaultdict(list))
        self.counted_data = {}
        
        # Initialize UI Components
        self.setup_ui()
        
        # Initiate the first data fetch and start the 30-second loop
        self.trigger_background_fetch()
        self.schedule_periodic_update()

    def setup_ui(self):
        """Constructs the dashboard interface."""
        # Head Type Selection
        ttk.Label(self, text="Cabeza").pack(pady=10)
        self.combo_head = ttk.Combobox(self, state="readonly")
        self.combo_head.pack()
        self.combo_head.bind("<<ComboboxSelected>>", self.update_size_combobox)
        
        # Nozzle Size Selection
        ttk.Label(self, text="Tipo").pack(pady=10)
        self.combo_size = ttk.Combobox(self, state="readonly")
        self.combo_size.pack()
        
        # Search Button
        ttk.Button(self, text="Buscar", command=self.render_table).pack(pady=10)
        
        # Data Grid Frame
        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(pady=10)

    # ==========================================
    # DATA PIPELINE & BACKGROUND TASKS
    # ==========================================

    def trigger_background_fetch(self):
        """Fires off the API request sequence in a separate thread to prevent UI freezing."""
        threading.Thread(target=self.fetch_api_data, daemon=True).start()

    def schedule_periodic_update(self):
        """Schedules the dashboard to refresh its data every 30 seconds."""
        self.trigger_background_fetch()
        self.after(30000, self.schedule_periodic_update)

    def fetch_api_data(self):
        """(Extract & Transform) Reaches out to the machines and parses the JSON."""
        temp_nozzle_list = []
        temp_data = defaultdict(lambda: defaultdict(list))
        
        for machine in MACHINE_LIST:
            api_url = f"http://mxchim0nxapp04/fujiweb/fujimoni/ui/api/McUnitInfo?Machine={machine}"
            try:
                # 1-second timeout keeps the thread agile if a machine is offline
                response = requests.get(api_url, timeout=1)
                response.raise_for_status() 
                response_json = response.json()
                
                if not response_json:
                    continue
                
                # Parse Nested JSON Hierarchy
                module_list = response_json.get("UnitInfo", {}).get("Module", [])
                for element in module_list:
                    nozzle_station = element.get("NozzleStation", {})
                    nozzle_list_data = nozzle_station.get("Nozzle", [])
                    
                    for nozzle in nozzle_list_data:
                        if not isinstance(nozzle, dict):
                            continue
                        
                        # Extract flags and identifiers
                        serial = nozzle.get("Serial", "").split()[0]
                        nozzle_info = NOZZLE_DICT.get(serial, serial)
                        job_use = nozzle.get('JobUse')
                        nozzle_position = nozzle.get('NzlPosition')
                        element_no = element.get('@No')
                        nozzle_no = nozzle.get('@No')
                        machine_lane = MACHINE_DICT.get(machine, 'unknown')
                        
                        # Logic: Is it available, or is it abandoned in the machine?
                        if job_use == '0':
                            temp_nozzle_list.append([nozzle_info, [machine_lane, element_no, nozzle_no, False]])
                        elif job_use == '1' and not nozzle_position:
                            temp_nozzle_list.append([nozzle_info, [machine_lane, element_no, nozzle_no, True]])
                            
            except (requests.RequestException, ValueError):
                # Silently fail on network/parsing errors so the dashboard keeps running
                continue

        # Restructure data into a hierarchical dictionary: data[head_type][nozzle_size]
        for nozzle in temp_nozzle_list:
            nozzle_values = nozzle[0].split('-')
            if len(nozzle_values) == 1:
                nozzle_values = ['R36', nozzle_values[0]]
                
            head_type = HEAD_DICT.get(nozzle_values[0], nozzle_values[0])
            nozzle_size = nozzle_values[1]
            temp_data[head_type][nozzle_size].extend(nozzle[1:])
        
        # Safely update the application state
        self.raw_nozzle_list = temp_nozzle_list
        self.structured_data = temp_data
        self.counted_data = self.aggregate_counts(temp_data)
        
        # Thread-safe GUI update: Push the refresh to the main thread
        self.after(0, self.update_head_combobox)

    def aggregate_counts(self, data):
        """Processes the structured data to count quantities and flag anomalies."""
        result = {}
        for head_type, nozzle_sizes in data.items():
            result[head_type] = {}
            for nozzle_size, entries in nozzle_sizes.items():
                counts = {}
                for lane, module, slot, needs_attention in entries:
                    key = (lane, module)
                    if key not in counts:
                        counts[key] = {'amount': 0, 'attention': ""}
                    
                    counts[key]['amount'] += 1
                    
                    # The "?" flag indicates an abandoned or unassigned nozzle
                    if needs_attention:
                        counts[key]['attention'] = "?"
                        
                result[head_type][nozzle_size] = [
                    [lane, module, counts[(lane, module)]['amount'], counts[(lane, module)]['attention']]
                    for lane, module in counts
                ]
        return result

    # ==========================================
    # UI RENDER METHODS
    # ==========================================

    def update_head_combobox(self):
        """Populates the first combobox with available Head Types."""
        self.combo_head['values'] = list(self.counted_data.keys())
        if self.combo_head.get():
            self.update_size_combobox()

    def update_size_combobox(self, event=None):
        """Populates the second combobox based on the Head Type selection."""
        subkeys = list(self.counted_data.get(self.combo_head.get(), {}).keys())
        self.combo_size['values'] = subkeys

    def render_table(self):
        """Clears the old grid and draws the data table for the selected nozzle."""
        key_head = self.combo_head.get()
        key_size = self.combo_size.get()
        table_data = self.counted_data.get(key_head, {}).get(key_size, [])
        
        # Purge existing widgets in the frame
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
            
        # Draw Headers
        headers = ["Linea", "Modulo", "Cantidad", ""]
        for col_idx, text in enumerate(headers):
            ttk.Label(self.grid_frame, text=text, font=("TkDefaultFont", 9, "bold")).grid(row=0, column=col_idx, padx=5, pady=2)
            
        # Draw Rows
        for row_idx, sublist in enumerate(table_data):
            for col_idx, value in enumerate(sublist):
                ttk.Label(self.grid_frame, text=value).grid(row=row_idx+1, column=col_idx, padx=5)


if __name__ == "__main__":
    # Dynamically set working directory to the script's location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Launch the application
    app = NozzleDashboard()
    app.mainloop()
