import os
import unreal
import importlib
import checkdata
import re
import inspect
import Validation
import pyblish.api
import Collection
import CGControll

def create_temp_dir(dir_name):
    dir_path = os.path.join(os.getenv('TEMP'), dir_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def clear_data():
    checkdata._ASSETNAEMMAP = {"ObjectsMap":[]}

def clear_info_data():
    checkdata._PLUGINENABLE = []

def get_instance_data(package_name, plugin_name):
    asset_data_map = get_asset_map()
    asset_data_list = asset_data_map.get("ObjectsMap")
    if asset_data_list:
        for object_data in asset_data_list:
            name = object_data.get('name')
            if package_name == name:
                for instance_data in object_data.get('info'):
                    if plugin_name == instance_data.get('aka'):
                        return instance_data
    
def get_current_assets_data():
    package_name = get_current_asset_name()
    if package_name:
        return unreal.AssetRegistryHelpers.get_asset_registry().get_assets_by_package_name(package_name)

def get_failed_check():
    return checkdata._FAILEDCHECKMAP

def get_current_asset_name():
    return checkdata._CURRENTSELECTED

def set_current_asset_name(item_text):
    results = re.findall(r"<.*?>(.*?)</>", item_text)
    if results:
        checkdata._CURRENTSELECTED = results[0]
    else:
        checkdata._CURRENTSELECTED = item_text

def get_asset_map():
    return checkdata._ASSETNAEMMAP


def controll_callback(file_name, *kwargs):
    from CGControll import baseCtl
    module = importlib.import_module(f".{file_name}", package="CGControll")
    importlib.reload(module)
    all_controlls = get_all_classes(baseCtl.BaseControll, module)
    all_func = []
    for controll in all_controlls:
        for callback in set(dir(controll)).union(set(dir(baseCtl.BaseControll))) - set(dir(object)):
            func = eval(f"controll.{callback}")
            if callback not in ['__dict__', '__module__', '__weakref__'] and hasattr(func, '__call__'):
                all_func.append(func)
    all_func.sort(key=lambda x: x.order)
    for func in all_func:
        func(*kwargs)

def get_all_classes(object, module=None):
    result = object.__subclasses__()
    tmp = []
    if result:
        for subclass in result:
            tmp.extend(get_all_classes(subclass))
    if module:
        all_class_tuple = inspect.getmembers(module.__name__, inspect.isclass)
        for class_name, class_instance in all_class_tuple:
            if isinstance(class_instance, object):
                tmp.append(class_instance)
    return result + tmp


def get_ui_handel():
    return unreal.PythonBPLib.get_chameleon_data("Python/CGCheck/checkui.json")

def get_status_btn_name(aka):
    return aka + '_status_btn'

def set_item_color():
    asset_map = get_asset_map()
    handel = get_ui_handel()
    handel.set_list_view_items("listview", [])
    all_object = asset_map.get("ObjectsMap")
    result = []
    for data in all_object:
        validators = data.get("info")
        pacakge_name = data.get("name")
        check_state_list = [validator.get("btn_color")[0]for validator in validators if validator.get("btn_color")]
        if check_state_list:
            if any(check_state_list):
                rich_text = "<RichText.red>" + pacakge_name + "</>"
            else:
                rich_text = "<RichText.green>" + pacakge_name + "</>"
        else:
            rich_text = pacakge_name
        result.append(rich_text)
    handel.set_list_view_items("listview", result)


def set_status_btn_color():
    handle = get_ui_handel()
    current_package_name = get_current_asset_name()

    if current_package_name:
        asset_map = get_asset_map()
        for objeect_info in asset_map.get("ObjectsMap"):
            s_package_name = objeect_info.get('name')

            if s_package_name == current_package_name:
                info_list = objeect_info.get("info")
                for info in info_list:
                    aka_name = info.get("aka")
                    color = info.get("btn_color")

                    if color:
                        btn_status_name = get_status_btn_name(aka_name)
                        handle.set_button_color_and_opacity(btn_status_name, color)
                break

def edit_assetmap_attr(aka, package_name, attrs, is_single=False):
    asset_map = get_asset_map()
    all_objects_map = asset_map.get('ObjectsMap')
    for object_info in all_objects_map:
        d_package_name = object_info.get("name")
        if d_package_name == package_name:
            for validator in object_info.get('info'):
                validator_aka = validator.get('aka')
                if validator_aka == aka:
                    for key, value in attrs.items():
                        if key in validator:
                            validator[key] = value
    if is_single:
        set_item_color()
        set_status_btn_color()
        CGControll.refresh_tab_info(aka)



def orderfunction(order=None):
    def wrapper1(func, order=order):
        def wrapper2():
            func()
        wrapper2.order = order
        return wrapper2
    return wrapper1

def get_tw_instance():
    return checkdata._TW

def get_asset_type():
    return checkdata._asset_type


def register_all_plugin_path():
    pyblish.api.deregister_all_paths()
    register_all_collection_path()
    register_all_validation_path()

def register_all_collection_path():
    path = os.path.dirname(os.path.dirname(__file__))
    collection_path = os.path.join(path, get_collection_name())
    reload_module(collection_path, get_collection_name())
    pyblish.api.register_plugin_path(collection_path)

def register_all_validation_path():
    for i in Validation.get_all_plugin_path():
        name = os.path.basename(i)
        reload_module(i, get_validation_name() + '.' + name)
        
        pyblish.api.register_plugin_path(i)

def get_all_plugin_path():
    return Validation.get_all_plugin_path()

def get_all_colection_path():
    return Collection.get_plugin_path()
    
def get_validation_name():
    return checkdata._VALIDATIONNAME

def get_collection_name():
    return checkdata._COLLECTIONNAME

def reload_module(path, package):
    for fname in os.listdir(path):
        if fname != "__init__.py":
            name, file_type = os.path.splitext(fname)
            module = importlib.import_module(f'.{name}', package=package)
            importlib.reload(module)

def add_aka_name_list(aka_name_list):
    all_aka_name_list = get_aka_name_list()
    for aka_name in aka_name_list:
        if aka_name not in all_aka_name_list:
            all_aka_name_list.append(aka_name)
        else:
            unreal.log_warning(f"该检查项的Aka标识有重复：{aka_name}")


def get_aka_name_list():
    return checkdata._ALLAKANAME

def add_package_name(package_name_list):
    checkdata._ALLASSETNAME.extend(package_name_list)

def get_all_package_name():
    return checkdata._ALLASSETNAME


def set_check_number(number):
    checkdata._CHECKNUMBER = number

def get_check_number():
    return checkdata._CHECKNUMBER


def get_current_content_path():
    return checkdata._current_contentbrowser_path

def set_plugin_enable(aka_name, enable='禁止'):
    handle = get_ui_handel()
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

def get_plugin_enable(aka_name):
    result = None
    for item in checkdata._PLUGINENABLE:
        if item.get('aka_name') == aka_name:
            result =  item.get('enable')
            break
    return result
