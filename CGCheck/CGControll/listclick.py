from util import utility
from CGControll import baseCtl
import pyblish.api
import importlib
importlib.reload(baseCtl)
importlib.reload(utility)


class ListClicked(baseCtl.BaseControll):

    @staticmethod
    @baseCtl.set_order(0)
    def set_current_asset_name(item_text):
        utility.set_current_asset_name(item_text)

    @staticmethod
    @baseCtl.set_order(1)
    def change_status_color(item_text):
        asset_map = utility.get_asset_map()
        all_objects = asset_map.get("ObjectsMap")
        if all_objects:
            utility.set_status_btn_color()
    
    @staticmethod
    @baseCtl.set_order(2)
    def display_diff_valition(item_text):
        validators_path = utility.get_all_plugin_path()
        all_validators_list = pyblish.api.discover(paths=validators_path)
        asset_map = utility.get_asset_map()
        all_object_info = asset_map.get("ObjectsMap")
        current_pacakge_name = utility.get_current_asset_name()
        ui_handle = utility.get_ui_handel()
        if all_object_info:
            for object_info in all_object_info:
                name = object_info.get("name")
                validator_info_list = object_info.get("info")
                if name == current_pacakge_name:
                    aka_name_list = [i.aka_name for i in all_validators_list]
                    diff = set([i.aka_name for i in all_validators_list]) - set([i.get("aka") for i in validator_info_list])
                    for validator_info in validator_info_list:
                        family = validator_info.get('family')
                        for validator in all_validators_list:
                            visibility = "Collapsed"
                            aka_name = validator.aka_name
                            if family in validator.families:
                                visibility = "Visible"
                            ui_handle.set_visibility(aka_name + '_horizentalbox', visibility)
                    # for aka_name in aka_name_list:
                    #     visibility = "Collapsed"
                    #     if aka_name not in diff:
                    #         visibility = "Visible"
                    #     ui_handle.set_visibility(aka_name + '_horizentalbox', visibility)
                    # break
                    


