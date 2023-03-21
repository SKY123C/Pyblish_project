from util import utility
import pyblish.api


class ValidationAkaList:
    aka_list = ["filename", "path", "owner", "families"]


class CGInfo(object):

    @staticmethod
    def set_all_info(**kwargs):
        aka_name = kwargs.get("aka_name")
        package_name = utility.get_current_asset_name()
        instance_data = utility.get_instance_data(package_name, aka_name)
        if instance_data:
            CGInfo.set_feedback(instance_data)
        CGInfo.set_plugin_info(aka_name)

    @staticmethod
    def set_feedback(instance_data):
        text = instance_data.get("cg_msg")
        handle = utility.get_ui_handel()
        handle.set_text('info_text_edit', text if text else '')

    @staticmethod
    def set_plugin_info(aka_name):
        validators_path = utility.get_all_plugin_path()
        all_validators_list = pyblish.api.discover(paths=validators_path)
        handle = utility.get_ui_handel()
        for validator in all_validators_list:
            if aka_name == validator.aka_name:
                break
        else:
            return
        
        for aka_suffix in ValidationAkaList.aka_list:
            text = None
            aka_name = "validation_" + aka_suffix
            if hasattr(validator, aka_suffix):
                text = str(getattr(validator, aka_suffix))
            handle.set_text(aka_name, text if text else '')


    @staticmethod
    def set_validation_info(**kwargs):
        handle = utility.get_ui_handel()
        for aka_suffix in ValidationAkaList.aka_list:
            text = kwargs.get(aka_suffix)
            aka_name = "validation_" + aka_suffix
            handle.set_text(aka_name, text if text else '')
            
