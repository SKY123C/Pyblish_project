import pyblish.api
from util import utility

def context_map(**kwargs):
    context = kwargs.get("context")
    asset_name = context.get("name")      
    asset_map = utility.get_asset_map()
    if asset_map:
        all_objects = asset_map.get("ObjectsMap")
        for data in all_objects:
            if data.get("name") == asset_name:
                info_list = data.get("info")
                info_list.append(dict(context))
                break
        else:
            result = {"name":asset_name, "info":[dict(context)]}
            all_objects.append(result)

def assetmap(func):
    def wrapper(**kwargs):
        context_map(**kwargs)
        func(**kwargs)
    return wrapper


class Calls(object):

    @staticmethod
    @assetmap
    def on_validated(context):
        pass
    
    @staticmethod
    @assetmap
    def on_pluginFailed(context):
        pass
    
    @staticmethod
    def on_repaired(aka, package_name, is_single, attrs):
        utility.edit_assetmap_attr(aka, package_name, attrs, is_single)
        
def callback_init():
    pyblish.api.deregister_all_callbacks()
    for callback in set(dir(Calls))-set(dir(object)):
        if callback not in ['__dict__', '__module__', '__weakref__']:
            callback_name = callback.split('on_')[-1]
            pyblish.api.register_callback(callback_name, eval(f"Calls.{callback}"))

