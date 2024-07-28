import tkinter as tk
from tkinter import ttk

# Example data structure (replace with your actual data)
data = {
    "Type1": {
        "Size1": [["Line1", "Mod1", "Slot1"], ["Line2", "Mod2", "Slot2"]],
        "Size2": [["Line3", "Mod3", "Slot3"], ["Line4", "Mod4", "Slot4"]]
    },
    "Type2": {
        "Size1": [["Line5", "Mod5", "Slot5"], ["Line6", "Mod6", "Slot6"]],
        "Size2": [["Line7", "Mod7", "Slot7"], ["Line8", "Mod8", "Slot8"]]
    }
}

# Initialize tkinter
root = tk.Tk()
root.title("Buscador de Nozzles")
root.minsize(width=400, height=300)

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
    ttk.Label(frame, text="Linea").grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")
    ttk.Label(frame, text="Modulo").grid(row=0, column=1, padx=5, pady=5, sticky="w")
    ttk.Label(frame, text="Slot").grid(row=0, column=2, padx=(5, 10), pady=5, sticky="w")

    # Display table data
    for i, sublist in enumerate(table_data):
        ttk.Label(frame, text=sublist[0]).grid(row=i+1, column=0, padx=(10, 5), pady=5, sticky="w")
        ttk.Label(frame, text=sublist[1]).grid(row=i+1, column=1, padx=5, pady=5, sticky="w")
        ttk.Label(frame, text=sublist[2]).grid(row=i+1, column=2, padx=(5, 10), pady=5, sticky="w")

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
