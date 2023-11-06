import re
from PIL import Image
import math
import numpy as np
from icecream import ic
import sys
import time
import dearpygui.dearpygui as dpg

def dna_to_color(dna: str) -> tuple[int, int, int]:
    dnaMatch = {
        "A": (255,   0,     0),
        "T": (0,     255,   0),
        "G": (0,     0,     255),
        "C": (255,    255,     0),
    }
    return dnaMatch.get(dna, None)

# from: https://github.com/hoffstadt/DearPyGui/discussions/1002 (thanks!)
def show_info(title, message, selection_callback):

    # guarantee these commands happen in the same frame
    with dpg.mutex():

        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()

        with dpg.window(label=title, modal=True, no_close=True) as modal_id:
            dpg.add_text(message)
            dpg.add_button(label="Ok", width=75, user_data=(modal_id, True), callback=lambda: dpg.hide_item(modal_id))

    # guarantee these commands happen in another frame
    dpg.split_frame()
    width = dpg.get_item_width(modal_id)
    height = dpg.get_item_height(modal_id)
    dpg.set_item_pos(modal_id, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])

def populate_numpy_array(dna: str, rgba: bool = False) -> np.ndarray:
    dna_len = dna.count("A") + dna.count("T") + dna.count("G") + dna.count("C")
    nImage = np.zeros((math.ceil(math.sqrt(dna_len)), math.ceil(math.sqrt(dna_len)), 3 if not rgba else 4), dtype=np.uint8)

    width, height, _ = nImage.shape
    print(nImage.shape)
    class Done(Exception): pass
    iterations = 0
    
    try:
        for y in range(height):
            for x in range(width):
                current_color = dna_to_color(dna[iterations])
                if current_color == None:
                    continue
                nImage[x, y] = list(current_color) if not rgba else list(current_color) + [255]
                iterations += 1
                if iterations == len(dna):
                    raise Done

    except (IndexError, Done):
        ic(f"image resolution: {math.ceil(math.sqrt(dna_len))}x{math.ceil(math.sqrt(dna_len))}")
        ic(f"dna length: {dna_len}")
        ic(f"iterations done: {iterations}")
        ic("As: {} Ts: {} Gs: {} Cs: {}".format(dna.count("A"), dna.count("T"), dna.count("G"), dna.count("C")))
        print("Done visualizing")
        return nImage

    
def parse_dna(path: str) -> str:
    print("opening file: " + path)
    dna = ""
    start = time.time()
    with open(path, 'r') as file:
        dna = file.read().strip()
        file.close()
        dna = re.sub('>.*', '', dna)
        dna = dna.replace('\n', '')
    print("Done reading file")
    print(f"Done in {time.time() - start}")
    return dna