import sys
import json
import os
import pyblish.api
import pyblish.util
import unreal
import importlib

UI_TEMP_PATH_NAME = "CGCheck"
UI_NAME = "UI.json"
UI_SOURCE = "Source.json"
CURRENT_DIR_PATH = os.path.dirname(__file__)
sys.path.append(CURRENT_DIR_PATH)
import checkdata
from util import utility
from baseclass import cginstance
importlib.reload(checkdata)
importlib.reload(utility)
importlib.reload(cginstance)

def write_all_widgets():
    validators_path = utility.get_all_plugin_path()
    all_validators_list = pyblish.api.discover(paths=validators_path)
    aka_name_list = []
    with open(os.path.join(CURRENT_DIR_PATH, UI_NAME), "w") as f:
        template_list = []
        result = {"SVerticalBox": {"Slots":template_list}}
        for validator in all_validators_list:
            aka = validator.aka_name
            label = validator.label
            template_str = get_template_str("template/template.json")
            location = validator.filename
            dir_name = validator.dir_path.stem
            class_name = validator.plugin_class
            callback_command = f'from Validation import {dir_name};importlib.reload({dir_name});{dir_name}.{location}.{class_name}.rebuild()'
            info_command = f"from CGControll import cginfo;importlib.reload(cginfo);cginfo.CGInfo.set_all_info(aka_name='{aka}')"
            enable_command = f"from CGCheck import util;util.utility.controll_callback('enable_click', '{aka}', %)"
            template = set_template_str(template_str, aka, label, aka, enable_command, aka, info_command, aka, callback_command, aka)
            template_list.append(json.loads(template))
            aka_name_list.append(aka)
            utility.set_plugin_enable(aka_name=aka)
        output_str = json.dumps(result, indent=4)
        utility.add_aka_name_list(aka_name_list)
        f.write(output_str[1:-1])

def set_template_str(template_str, *args):
    return template_str % args

def write_all_asset():
    folder_path = unreal.PythonBPLib.get_selected_folder()
    checkdata._current_contentbrowser_path = folder_path
    results = []
    if folder_path:
        asset_data_List = unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_path(folder_path[0], True)
        set_plugin_asset_number(asset_data_List)
        for asset_data in asset_data_List:
            results.append(str(asset_data.package_name))
        with open(os.path.join(CURRENT_DIR_PATH, UI_SOURCE), "w") as f1:
            with open(os.path.join(CURRENT_DIR_PATH, "template/templatesource.json"), 'r') as f2:
                dst_json = json.load(f2)
                dst_json['ListItemsSource'] = results
            output_str = json.dumps(dst_json, indent=4)
            f1.write(output_str[1:-1])
    utility.add_package_name(results)

def get_template_str(file_name):
    with open(os.path.join(CURRENT_DIR_PATH, file_name), "r", encoding="utf-8") as f:
        result = f.read()
        result = result.replace(" ", "").replace("\n", "")
    return result

def set_plugin_asset_number(asset_data_List):
    result = 0
    validators_path = utility.get_all_plugin_path()
    all_validators_list = pyblish.api.discover(paths=validators_path)
    for validator in all_validators_list:
        validator_families = validator.families
        for asset_data in asset_data_List:
            asset_class = str(asset_data.asset_class)
            if asset_class in validator_families or validator_families[0] == "*":
                result += 1
    all_collection_list = pyblish.api.discover(paths=[utility.get_all_colection_path()])
    result += len(all_collection_list)
    utility.set_check_number(result)
        
def clear_data():
    utility.clear_data()

def init():
    utility.register_all_plugin_path()
    clear_data()
    write_all_asset()
    write_all_widgets()


init()

