import requests
from bs4 import BeautifulSoup
import tkinter
import customtkinter
from tkinter import ttk
import threading
import time

from multiprocessing import Pool
from multiprocessing import cpu_count
from multiprocessing import Manager
from tqdm import tqdm
import pyfiglet
from threading import Condition

#system settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("800x500")
app.title("WoWHead Arrayify")
app.resizable(False, False)

# Create labels, input field, and output box
input_label = customtkinter.CTkLabel(app, text="Input Box:")
input_label.grid(row=0, column=0)
input_field = customtkinter.CTkTextbox(app, height=10)
input_field.grid(row=1, column=0, sticky='nsew')

output_label = customtkinter.CTkLabel(app, text="Output Box:")
output_label.grid(row=0, column=1)
output_box = customtkinter.CTkTextbox(app)
output_box.grid(row=1, column=1, sticky='nsew')
# Create progress bar
progress = ttk.Progressbar(app, length=100, mode='determinate')
progress.grid(row=3, column=0, columnspan=2, sticky='ew')


# Create switch button
game_mode = customtkinter.StringVar(value="retail")
switch_button = customtkinter.CTkSwitch(app, text="Retail/Classic", variable=game_mode, onvalue="classic", offvalue="retail")
switch_button.grid(row=4, column=0, columnspan=2)


# Create dropdown menu
dropdown_options = ["Npcs", "Spells", "Objects"]
dropdown_var = tkinter.StringVar()
dropdown_var.set(dropdown_options[0])  # set default value to the first option
dropdown = tkinter.OptionMenu(app, dropdown_var, *dropdown_options)
dropdown.grid(row=5, column=0, columnspan=2)

def callback(*args):
    print("game_mode is now", game_mode.get())

game_mode.trace("w", callback)

# Configure the grid to expand properly
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(1, weight=1)



def update_progress_bar(counter, total_spells, done):
    while True:
        with done:
            if done.wait(timeout=0.1):  # update every 0.1 seconds or when done
                break
        progress['value'] = 100 * (counter.value / total_spells)
        app.update_idletasks()
    progress['value'] = 100  # ensure progress bar reaches 100% when done
def fetch_spell_info(args):
    spell_id, mode, dropdown_value, counter, lock = args
    if mode == "classic":
        if dropdown_value == "Npcs":
            url = f"https://www.wowhead.com/{mode}/npc={spell_id}"
        elif dropdown_value == "Objects":
            url = f"https://www.wowhead.com/{mode}/object={spell_id}"
        elif dropdown_value == "Spells":
            url = f"https://www.wowhead.com/{mode}/spell={spell_id}"
        else:
            return None
    if mode == "retail":
        if dropdown_value == "Npcs":
            url = f"https://www.wowhead.com/npc={spell_id}"
        elif dropdown_value == "Objects":
            url = f"https://www.wowhead.com/object={spell_id}"
        elif dropdown_value == "Spells":
            url = f"https://www.wowhead.com/spell={spell_id}"
        else:
            return None
    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    spell_name = soup.find("h1", {"class": "heading-size-1"}).text
    if spell_name == "Spells":
        return None

    with lock:
        counter.value += 1
    return f"[{spell_id}] = true, -- {spell_name} {url}"

def lookup_spells():
    # Clear the output box
    output_box['state'] = 'normal'
    output_box.delete('1.0', tkinter.END)

    spell_ids_raw = input_field.get("1.0", tkinter.END).strip()
    if ',' not in spell_ids_raw:
        spell_ids_raw = ', '.join(spell_ids_raw.split())
    spell_ids = set(map(int, spell_ids_raw.split(',')))
    mode = game_mode.get()
    dropdown_value = dropdown_var.get()

    with Manager() as manager:
        counter = manager.Value('i', 0)
        lock = manager.Lock()
        total_spells = len(spell_ids)
        done = Condition()
        progress_thread = threading.Thread(target=update_progress_bar, args=(counter, total_spells, done))
        progress_thread.start()
        with Pool(processes=min(36, total_spells)) as pool:
            results = list(tqdm(pool.imap(fetch_spell_info, [(id, mode, dropdown_value, counter, lock) for id in spell_ids]), total=total_spells))
        with done:
            done.notify_all()  # signal that all spells have been processed
    for result in filter(None, results):
        output_box.insert(tkinter.END, result + '\n') 
    output_box['state'] = 'disabled'
    # Update progress bar to 100% when done
    progress['value'] = 100
    time.sleep(1)  # wait for progress bar update thread to finish
# Create button to trigger spell lookup
lookup_button = customtkinter.CTkButton(app, text="Lookup", command=lambda: threading.Thread(target=lookup_spells).start())
lookup_button.grid(row=2, column=0, columnspan=2)

def main():
    app.mainloop()

if __name__ == "__main__":
    main() 