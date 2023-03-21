import pyblish.api
import unreal
import checkdata
import pyblish.plugin
from util import utility


class materialAbcCollections(pyblish.api.ContextPlugin):
    order = pyblish.api.CollectorOrder
    def process(self, context):

        current_content_path = utility.get_current_content_path()[0]  # return a list
        asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
        all_material_dictList = unreal.PythonBPLib.get_assets_data_by_class([current_content_path], ['Material'])
        if all_material_dictList:
            for eachItem in all_material_dictList:
                material_path = str(eachItem.object_path)
                asset_data = asset_registry.get_asset_by_object_path(material_path)
                if asset_data:
                    context.create_instance(name=str(asset_data.package_name), asset_data=asset_data, family="Material")


        # folder_path = utility.get_current_content_path()
        # all_asset_list = unreal.EditorAssetLibrary.list_assets(folder_path[0])
        # asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
        # for asset_str in all_asset_list:
        #     dirname = os.path.dirname(asset_str)
        #     asset_data = asset_registry.get_asset_by_object_path(asset_str)
        #     if asset_data:
        #         class_name = str(asset_data.asset_class)
        #         if class_name == "LevelSequence" and not dirname.endswith(("SubTrack", "shots")) and unreal.EditorAssetLibrary.does_directory_exist(unreal.Paths.combine([dirname, 'SubTrack'])):
        #             context.create_instance(name=str(asset_data.package_name), asset_data=asset_data, family="LevelSequence")
        #
