import pyblish.api
import unreal
import checkdata
import pyblish.plugin
import os
from util import utility


class collect1(pyblish.api.ContextPlugin):
    order = pyblish.api.CollectorOrder
    def process(self, context):
        folder_path = utility.get_current_content_path()
        all_asset_list = unreal.EditorAssetLibrary.list_assets(folder_path[0])
        asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
        for asset_str in all_asset_list:
            dirname = os.path.dirname(asset_str)
            asset_data = asset_registry.get_asset_by_object_path(asset_str)
            if asset_data:
                if asset_data.get_class() == unreal.LevelSequence.static_class() and not dirname.endswith(("SubTrack", "shots")) and unreal.EditorAssetLibrary.does_directory_exist(unreal.Paths.combine([dirname, 'SubTrack'])):
                    context.create_instance(name=str(asset_data.package_name), asset_data=asset_data, family="LevelSequence")
