from util import utility
import importlib
import unreal
importlib.reload(utility)

def repair():
    asset_map = utility.get_asset_map()
    all_objects_info = asset_map.get("ObjectsMap")
    if all_objects_info:
        total_frames = len(all_objects_info)
        text_label = "Working!"
        with unreal.ScopedSlowTask(total_frames, text_label) as slow_task:
            slow_task.make_dialog(True)
            for data in all_objects_info:
                package_name = data.get("name")
                check_info_list = data.get("info")
                for info in check_info_list:
                    check_status = info.get("checkStatus")
                    if not check_status:
                        method = info.get('rebuild')
                        if method:
                            method(package_name)
                    if slow_task.should_cancel():
                        break
                    slow_task.enter_progress_frame(1, "正在修复...")
        utility.set_item_color()
    unreal.SystemLibrary.collect_garbage()