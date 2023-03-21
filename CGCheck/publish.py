import pyblish.util
import pyblish.api
import checkdata
from util import utility
import callback
import unreal    

def publish(context=None):
    utility.clear_data()
    plugins = check_plugin_enable()
    context = pyblish.util.collect()

    set_collect_map(context_list=context)
    #checkdata._COLLECTIONCONTEXT = context
    context = context if context is not None else pyblish.api.Context()
    total_frames = len(context)
    text_label = "Working!"
    with unreal.ScopedSlowTask(total_frames, text_label) as slow_task:
        slow_task.make_dialog(True)
        for result in pyblish.util._convenience_iter(context, plugins, None,
                                    order=pyblish.api.ValidatorOrder):
            if slow_task.should_cancel():
                break
            slow_task.enter_progress_frame(1, f"正在检查...")
    utility.set_item_color()


def check_plugin_enable():
    result = []
    validators_path = utility.get_all_plugin_path()
    all_validators_list = pyblish.api.discover(paths=validators_path)
    for plugin in all_validators_list:
        if utility.get_plugin_enable(plugin.aka_name):
            result.append(plugin)
    return result
            

def set_collect_map(**kwargs):
    context_List = kwargs.get('context_list')
    if context_List:
        for context in context_List:
            callback.context_map(context=context.data)
