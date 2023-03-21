from . import cginfo
import importlib
importlib.reload(cginfo)

def refresh_tab_info(aka_name):
    cginfo.CGInfo.set_all_info(aka_name=aka_name)

