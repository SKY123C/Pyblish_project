from . import(
            utility,
            tabback,
        )
import json
import os
import importlib
importlib.reload(utility)
importlib.reload(tabback)


class MTab(object):

    def __init__(self) -> None:
        self.tab_map = utility.get_tab_map()
        self.file_package = FilePackage()
    
    def pcg_create_widgets(self):
        pass

    def package_widget(self):
        self.pcg_create_widgets()
        current_aka = None
        for tab in self.tab_map:
            aka = tab.get("Aka")
            label = tab.get("Label")
            json_path = tab.get("UI")
            check_state = tab.get("CheckState")
            self.file_package.set_label_and_widget(aka, label, json_path, check_state=check_state)
            if check_state:
                current_aka = aka
        utility.set_current_aka(current_aka)
        self.file_package.write_disk()


class FilePackage(object):

    def __init__(self) -> None:
        self.get_check_box_dict()

    
    def get_check_box_dict(self):
        check_box_path = os.path.join(utility.get_template_path(), "checkbox.json")
        with open(check_box_path, "r") as f:
            self.check_box = json.load(f)
    
    def add_tab_label(self, label_dict):
        self.check_box.get("SVerticalBox").get("Slots")[0].get("SHorizontalBox").get("Slots").append(label_dict)
    

    def set_label_and_widget(self, aka_name, label, json_path, check_state):
        self.set_label_info(aka_name, label, check_state)
        self.set_widget_info(aka_name, json_path, check_state)

    def set_label_info(self, aka_name, label, check_state):
        tab_label_path = os.path.join(utility.get_template_path(), "tablabel.json")
        result = self.convert_str_to__dict(tab_label_path, aka_name, label)
        result.get("SBox").get("Content").get("SBorder").get("Content").get("SCheckBox").update({"IsChecked": check_state,"OnCheckStateChanged": "cgtab.tabback.callback()"})
        self.add_tab_label(result)
    
    def set_widget_info(self, aka_name, json_path, check_state):
        widget_path = os.path.join(utility.get_template_path(), "widget.json")
        result = self.convert_str_to__dict(widget_path, aka_name)
        result.get("SBox").update({"Visibility": "Visible" if check_state else "Collapsed"})
        self.add_tab_widget(result, json_path)

    def add_tab_widget(self, widget_tmp, json_path):
        widgets_path = os.path.join(utility.get_widgets_path(), json_path)
        with open(widgets_path, "r", encoding="utf-8") as f:
            result = json.load(f)
            widget_tmp.get("SBox").get("Content").update(result)
        self.check_box.get("SVerticalBox").get("Slots")[1].get("SBorder").get("Content").get("SVerticalBox").get("Slots").append(widget_tmp)

    def convert_str_to__dict(self, path, *args):
        with open(path, "r", encoding="utf-8") as f:
            result = f.read()
            result = result.replace(" ", "").replace("\n", "")
            result = result % args
            obj_dict = json.loads(result)
        return obj_dict
    
    def write_disk(self):
        path = os.path.join(os.path.dirname(__file__), "tab.json")
        with open(path, "w") as f:
            result = json.dumps(self.check_box, indent=4)
            f.write(result[1:-1])



main = MTab()
main.package_widget()