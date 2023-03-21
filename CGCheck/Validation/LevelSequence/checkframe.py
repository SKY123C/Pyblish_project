import pyblish.api
import unreal
from pathlib import Path
from util import utility
from baseclass import cginstance

@cginstance.set_class_attr(__file__)
class SequenceFrame(cginstance.BaseValidator):
    order = pyblish.api.ValidatorOrder
    label = "检查Sequence帧数是否与teamwork一致"
    aka_name = "CheckFrame"
    families = ["LevelSequence"]
    owner = "ChenTao"

    def process(self, instance):
        result, msg = self.check_frame(instance)
        self.set_attr(result, instance, cg_msg=msg)
        pyblish.api.emit("validated", context=instance.data)

    @classmethod
    def rebuild(cls, package_name=None):
        is_single = False if package_name else True
        package_name = package_name if package_name else utility.get_current_asset_name()
        
        instance_data = utility.get_instance_data(package_name, cls.aka_name)
        print(instance_data)
        if instance_data:
            if 'section' in instance_data:
                cls.repair_subsequence(instance_data)
            if 'framerange' in instance_data:
                cls.repair_sequence(instance_data)
            unreal.EditorAssetLibrary.save_asset(package_name)
        result = {"checkStatus": True, "btn_color": [0, 1, 0, 1], 'cg_msg': "修复成功"}
        pyblish.api.emit("repaired", aka=SequenceFrame.aka_name, package_name=package_name, is_single=is_single, attrs=result)
    
    @staticmethod
    def repair_subsequence(instance_data):
        all_section_list = instance_data.get('section')
        frame_range = instance_data.get('prframerange')
        for section in all_section_list:
            sequence = None
            if type(section) != unreal.MovieSceneCameraCutSection:
                sequence = section.get_sequence()
                sequence.set_playback_start(int(frame_range[0]))
                sequence.set_playback_end(int(frame_range[1])+1)
            section.set_is_locked(False)
            section.set_start_frame(int(frame_range[0]))
            section.set_end_frame(int(frame_range[1])+1)
            if sequence:
                unreal.EditorAssetLibrary.save_asset(sequence.get_path_name())
    
    @staticmethod
    def repair_sequence(instance_data):
        frame_range = instance_data.get('framerange')
        asset_data = instance_data.get('asset_data')
        asset = asset_data.get_asset()
        asset.set_playback_start(int(frame_range[0]))
        asset.set_playback_end(int(frame_range[1])+1)
    
    def get_all_subtrack_framerange(self, asset_data):
        sequence = asset_data.get_asset()
        #unreal.MovieSceneCameraCutTrack
        all_subtrack_list = []
        camera_subtrack_list = sequence.find_master_tracks_by_type(unreal.MovieSceneCameraCutTrack)
        movie_subtrack_list = sequence.find_master_tracks_by_type(unreal.MovieSceneSubTrack)
        all_subtrack_list = camera_subtrack_list + movie_subtrack_list
        result = []
        for subtrack in all_subtrack_list:
            all_sections_list = subtrack.get_sections()
            if all_sections_list:
                start_frame = all_sections_list[0].get_start_frame()
                end_frame = all_sections_list[0].get_end_frame() - 1
                result.append({"start": start_frame, "end":end_frame, "section": all_sections_list[0]})
        return result

    def check_frame(self, instance):
        msg = ''
        asset_data = instance.data["asset_data"]
        all_framerange_list = self.get_all_subtrack_framerange(asset_data)
        sequence_info = self.get_tw_sequence_info(instance.data['name'])
        result = None
        if not all_framerange_list:
            msg = '缺少子轨道'
        if sequence_info and all_framerange_list:
            result1 = self.check_subsequence_frame(instance, sequence_info, all_framerange_list)
            result2 = self.check_sequence_framerange(instance, sequence_info, asset_data)
            result = all([result1, result2])
        return result, msg
    
    def check_subsequence_frame(self, instance, sequence_info, all_framerange_list):
        start = sequence_info[0].get('shot.holdframe')
        end = sequence_info[0].get('shot.holdendframe')
        s_framerange = [start, end]
        if all(s_framerange):
            for info_dict in all_framerange_list:
                framerange = [info_dict.get('start'), info_dict.get('end')]
                if any(map(lambda x, y: x - int(y), framerange, s_framerange)):
                    section = info_dict.get('section')
                    if 'prframerange' not in instance.data:
                        instance.data['prframerange'] = s_framerange
                        instance.data['section'] = [section]
                    else:
                        instance.data['section'].append(section)
            return 'prframerange' not in instance.data

    def check_sequence_framerange(self, instance, sequence_info, asset_data):
        start = sequence_info[0].get('shot.start_frame')
        end = sequence_info[0].get('shot.end_frame')
        s_framerange = [start, end]
        if all(s_framerange):
            asset = asset_data.get_asset()
            if asset.get_playback_start() != int(start) or asset.get_playback_end()-1 != int(end):
                instance.data['framerange'] = s_framerange
            return 'framerange' not in instance.data

    def get_tw_sequence_info(self, package_name):
        tw = utility.get_tw_instance()
        proj = 'proj_iii'
        dir_path = unreal.Paths.get_path(package_name)
        shot = unreal.Paths.get_base_filename(dir_path)
        ani_entity = unreal.Paths.get_base_filename(unreal.Paths.get_path(unreal.Paths.get_path(dir_path)))
        id_list = tw.info.get_id(proj, 'shot', filter_list=[['shot.entity', '=', shot], 'and', ['ani.entity', '=', ani_entity]])
        info_list = {}
        if len(id_list) == 1:
            info_list = tw.info.get('proj_iii', 'shot', id_list, ['shot.holdframe', 'shot.holdendframe', 'shot.start_frame', 'shot.end_frame'])
        return info_list