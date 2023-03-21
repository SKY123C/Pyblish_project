import sys
import unreal
sys.path.append("C:/CgTeamWork_v6.2/bin/base")
import cgtw2
_current_contentbrowser_path = None
_asset_type = unreal.Material
_instance = None
_CURRENTSELECTED = None
_ASSETNAEMMAP = {"ObjectsMap":[]}
_FAILEDCHECKMAP = dict()
_TW = cgtw2.tw()
_CURRENTCLICKEDAKA = None
_VALIDATIONNAME = "Validation"
_COLLECTIONNAME = "Collection"
_ALLAKANAME = []
_ALLASSETNAME = []
_CHECKNUMBER = 0
_PLUGINENABLE = []
_COLLECTIONCONTEXT = []