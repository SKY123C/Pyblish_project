import os
from . import tabdate
import unreal
import importlib
importlib.reload(tabdate)


def create_json(path=None, json_dict=None):
    if path:
        pass

def set_current_aka(aka):
    tabdate.CURRENTAKA = aka

def get_current_aka():
    return tabdate.CURRENTAKA

def get_tab_map():
    return tabdate.TABMAP

def get_widgets_path():
    return tabdate.WIDGETSPATH

def get_template_path():
    return tabdate.TEMPLATEPATH

def get_ui_handle():
    handle = unreal.PythonBPLib.get_chameleon_data("Python/CGCheck/checkui.json")
    return handle