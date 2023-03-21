import pyblish.api
import unreal
from pathlib import Path
from util import utility
from baseclass import cginstance


@cginstance.set_class_attr(__file__)
class MaterialAbcChannel(cginstance.BaseValidator):
    order = pyblish.api.ValidatorOrder
    label = "检查母材质球的Abc通道是否勾选"
    aka_name = "CheckMaterialAbcChannel"
    families = ["Material"]

    def process(self, instance):
        result = self.check_material_abc_channel(instance)
        self.set_attr(result, instance)
        pyblish.api.emit("validated", context=instance.data)




    def check_material_abc_channel(self, instance_data):
        asset_data = instance_data.data["asset_data"]
        material_asset = asset_data.get_asset()
        # print("material_asset----->", material_asset)
        geometry_cache_channel_check = material_asset.get_editor_property("used_with_geometry_cache")

        finalResult = geometry_cache_channel_check
        return finalResult



    @classmethod
    def rebuild(cls, package_name=None):

        is_single = False if package_name else True
        package_name = package_name if package_name else utility.get_current_asset_name()
        instance_data = utility.get_instance_data(package_name, cls.aka_name)
        print("instance_date---->", instance_data)
        asset_data = instance_data["asset_data"]
        material_asset = asset_data.get_asset()
        material_asset.set_editor_property("used_with_geometry_cache", True)

        # save the modified asset
        material_asset_path = material_asset.get_path_name()
        unreal.EditorAssetLibrary.save_asset(material_asset_path)

        result = {"checkStatus": True, "btn_color": [0, 1, 0, 1]}
        pyblish.api.emit("repaired", aka=cls.aka_name, package_name=package_name, is_single=is_single,
                         attrs=result)


        # instance_data = utility.get_instance_data(package_name, cls.aka_name)
        # if instance_data:
        #     if 'section' in instance_data:
        #         cls.repair_subsequence(instance_data)
        #     if 'framerange' in instance_data:
        #         cls.repair_sequence(instance_data)
        # result = {"checkStatus": True, "btn_color": [0, 1, 0, 1]}
        # pyblish.api.emit("repaired", aka=SequenceFrame.aka_name, package_name=package_name, is_signal=is_signal,
        #                  attrs=result)

