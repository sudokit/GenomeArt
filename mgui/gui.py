import dearpygui.dearpygui as dpg

from icecream import ic

from PIL import Image
from . import utils


import numpy as np
import os.path as op

def extract_path_from_dialog(app_data) -> str:
    # print(app_data)
    path = app_data['current_path'] + '\\' + list(app_data['selections'].keys())[0]
    return path

def do_something_with_path(sender, app_data) -> None:
    path = extract_path_from_dialog(app_data)
    # dna = utils.parse_dna(path)
    dpg.set_value(item="filepath", value=path)

def handle_img_gen() -> None:
    filepath = dpg.get_value("filepath")
    if filepath == "":
        utils.show_info("Invalid filepath", "Please enter/select a filepath", None)
        return

    if not op.isfile(filepath):
        utils.show_info("Invalid filepath", "Please enter/select a valid filepath", None)
        return

    dna = utils.parse_dna(filepath)
    image_array = utils.populate_numpy_array(dna, rgba=True)
    width, height, _ = image_array.shape
    with dpg.texture_registry(show=False):
        dpg.add_static_texture(width=width, height=height, default_value=image_array/255.0, tag="tmp")

    with dpg.window(label="Preview", width=-1, height=-1):
        with dpg.plot(label="Image"):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="x axis")
            with dpg.plot_axis(dpg.mvPlotAxis, label="y axis"):
                dpg.add_image_series(label="img", texture_tag="tmp", bounds_min=[0, 0], bounds_max=[width, height])

def create_widgets() -> None:

    with dpg.file_dialog(directory_selector=False, show=False, callback=do_something_with_path, id="file_pick", width=700 ,height=400):
        dpg.add_file_extension(".*")
        dpg.add_file_extension("", color=(150, 255, 150, 255))
        dpg.add_file_extension(".txt", color=(0, 255, 0, 255), custom_text="[Text]")

    with dpg.window(label="Cool", width=800, height=600, no_move=True, no_resize=True, tag="main"):
        dpg.add_button(label="Select file", callback=lambda: dpg.show_item("file_pick"))
        dpg.add_same_line()
        dpg.add_input_text(default_value="", label="<path", tag="filepath")
        dpg.add_same_line()
        dpg.add_button(label="Generate image", callback=handle_img_gen)

def setup() -> None:
    dpg.create_context()
    dpg.setup_dearpygui()
    
def run() -> None:
    setup()
    create_widgets()
    dpg.create_viewport(title="DNA vis thing", width=800, height=600, resizable=False)
    dpg.show_viewport()
    dpg.start_dearpygui()
    destroy()

def destroy() -> None:
    dpg.destroy_context()