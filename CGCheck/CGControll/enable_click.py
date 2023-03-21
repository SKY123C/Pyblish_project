import unreal
import re
from CGControll import baseCtl
import importlib
from util import utility
import checkdata
importlib.reload(baseCtl)


class BoxEnable(baseCtl.BaseControll):


    @staticmethod
    @baseCtl.set_order(1)
    def set_plugin_enable(aka_name, enable='禁止'):
        handle = utility.get_ui_handel()
        if handle:
            enable = handle.get_combo_box_selected_item(aka_name + '_enable_combobox')
        enable_map = {"启用": True, "禁止": False}
        for item in checkdata._PLUGINENABLE:
            if item.get('aka_name') == aka_name:
                item['enable'] = enable_map.get(enable)
                break
        else:
            result = {'aka_name': aka_name, 'enable': enable_map.get(enable)}
            checkdata._PLUGINENABLE.append(result)

    @staticmethod
    @baseCtl.set_order(2)
    def change_btn_color(aka_name, enable='禁止'):
        handle = utility.get_ui_handel()
        if handle:
            btn_status_name = utility.get_status_btn_name(aka_name)
            handle.set_button_color_and_opacity(btn_status_name, [0.24,0.24,0.24,1])

