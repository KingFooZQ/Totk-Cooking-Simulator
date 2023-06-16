import os, sys
import traceback

try:
    os.chdir(sys._MEIPASS)
except:
    pass

import tkinter as tk
from tkinter import ttk
from simulator import TotkCookSim


sim = TotkCookSim()
root = tk.Tk()
text_list = []
for i in range(5):
    text_list.append( tk.StringVar())


def cook_button(event):
    materials = []
    for text in text_list:
        if text.get().strip():
            materials.append(text.get().strip())
    area_lang = combobox.get()
    result_srt = ''
    try:
        result = sim.cook(materials, area_lang=area_lang)
        for k, v in result.items():
            result_srt += f'{k}: {v}\n'
            output_text.delete('1.0', tk.END)
            output_text.insert('1.0', result_srt)
    except Exception as e:
        traceback.print_exc()
        output_text.delete('1.0', tk.END)
        output_text.insert('1.0', '程序出错了')
        output_text.insert('1.0', 'something goes wrong')



def create_input_frame(container):
    frame = ttk.Frame(container)

    for i in range(5):
        entry = ttk.Entry(frame, textvariable=text_list[i], state='write',width=13, font={'size':15}, justify='center')
        entry.grid(column=i, row=0, sticky=tk.E, padx=5, pady=5, ipadx=0, ipady=0)

    return frame

def create_output_frame(container):
    frame = ttk.Frame(container)

    return frame


root.title('王国之泪-料理模拟器 | Totk-Cooking-Simulator   v0.0.1')

window_width = 600
window_height = 400

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


icon_rel_path = './assets/icon.ico'
root.iconbitmap(icon_rel_path)


# layout on the root window
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

input_frame = create_input_frame(root)
input_frame.grid(column=0, row=0)

btn = ttk.Button(root, text='Cook')
btn.grid(column=0, row=1, sticky=tk.N, padx=5, pady=5, ipadx=0, ipady=0)
btn.bind('<Button-1>', cook_button)

output_text = tk.Text(root, height=15, width=70)
output_text.configure(font={'size': 30})
output_text.grid(column=0, row=2, sticky=tk.N, padx=5, pady=5, ipadx=0, ipady=0)
# output_frame = create_output_frame(root)
# output_frame.grid(column=0, row=2)
output_text = tk.Text(root, height=15, width=70)
output_text.configure(font={'size': 30})
output_text.grid(column=0, row=2, sticky=tk.N, padx=5, pady=5, ipadx=0, ipady=0)

combobox_var = tk.StringVar()
combobox_var.set('CNzh')
combobox = ttk.Combobox(root, textvariable=combobox_var, width=5)
combobox['values'] = ('CNzh', 'EUde','EUen', 'EUes', 'EUfr', 'EUit', 'EUnl', 'EUru', 'JPja', 'KRko', 'TWzh', 'USen', 'USes', 'USfr')
combobox['state'] = 'readonly'
combobox.grid(column=0, row=3, sticky=tk.N, padx=5, pady=5, ipadx=0, ipady=0)


root.mainloop()