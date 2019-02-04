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

def clicked(event):
    print(event)
    exit()
    
row = 0
for deviceName, device in config['devices'].items(): 
    lbl = Label(window, text=deviceName)
    lbl.grid(column=0, row=row)
    combo = ttk.Combobox(window)
    combo.state = "readonly"
    combo.grid(column=1, row=row)
    btn = Button(window, text="Trigger Action")
    btn['command'] = lambda deviceName=deviceName, combo=combo, qty=1 : lbp.perform_action_on_device(deviceName, combo.get(), qty)
    btn.grid(column=2, row=row)
    for actionName, action in device['actions'].items(): 
        values = combo['values']
        valuesList = list(values)
        valuesList.append(actionName)
        combo['values'] = valuesList
    combo.current(0) #set the selected item
    row = row + 1
        
 
window.mainloop()