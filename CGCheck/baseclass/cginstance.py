import pyblish.api
from pathlib import Path


class BaseValidator(pyblish.api.InstancePlugin):

    def set_attr(self, result, instance, **kwargs):
        color = [0,1,0,1] if result else [1,0,0,1]
        instance.data["checkStatus"] = result
        instance.data["aka"] = self.aka_name
        instance.data["btn_color"] = color
        instance.data["rebuild"] = type(self).rebuild
        for key, value in kwargs.items():
            instance.data[key] = value

def set_class_attr(file_path):
    
    def wrapper1(class_instance, file_path=file_path):
        def wrapper2():
            class_instance.plugin_class = class_instance.__name__
            class_instance.filename = Path(file_path).stem
            class_instance.dir_path = Path(file_path).parent
            class_instance.path = "CGCheck" + str(Path(file_path).parent).split("CGCheck")[1]
            return class_instance
        return wrapper2()
    return wrapper1

