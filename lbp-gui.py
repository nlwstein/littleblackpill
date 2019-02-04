from Tkinter import *
import ttk
from lbp import littleblackpill
import json

# Initialize config: 
config = json.loads(open('config.json').read())

# Initialize LBP: 
lbp = littleblackpill()

window = Tk()
window.title("LittleBlackPill")
window.geometry('350x200')

# Generate each device's row: 
row = 0
for deviceName, device in config['devices'].items(): 

    # Add a label: 
    lbl = Label(window, text=deviceName)
    lbl.grid(column=0, row=row)
    
    # Add an action dropdown: 
    combo = ttk.Combobox(window)
    combo.state = "readonly"
    combo.grid(column=1, row=row)

    # Add button to trigger the LBP functionality and wire it up accordingly: 
    btn = Button(window, text="Trigger Action")
    btn.grid(column=2, row=row)
    btn['command'] = lambda deviceName=deviceName, combo=combo, qty=1 : lbp.perform_action_on_device(deviceName, combo.get(), qty)
    
    # Insert records for each available action: 
    for actionName, action in device['actions'].items(): 
        values = combo['values']
        valuesList = list(values)
        valuesList.append(actionName)
        combo['values'] = valuesList

    # Set the selected item to the first one in the config: 
    combo.current(0) 
    
    # Create the next device one row down: 
    row = row + 1

# Trigger the main loop for the GUI: 
window.mainloop()