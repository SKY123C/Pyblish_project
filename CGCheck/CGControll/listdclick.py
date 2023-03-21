import unreal
import re
from CGControll import baseCtl
import importlib
from util import utility
importlib.reload(baseCtl)


class ListDClicked(baseCtl.BaseControll):
    
    @staticmethod
    @baseCtl.set_order(0)
    def set_current_asset_name(item_text):
        utility.set_current_asset_name(item_text)

    @staticmethod
    @baseCtl.set_order()
    def select_asset(item_text):
        item_text_list = re.findall(r"<.*?>(.*?)</>", item_text)
        item_text = item_text_list[0] if item_text_list else item_text
        unreal.EditorAssetLibrary.sync_browser_to_objects([item_text])


