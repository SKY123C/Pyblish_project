from . import utility

class TabBack(object):

    @staticmethod
    def set_check_and_widget_visility():
        tab_map = utility.get_tab_map()
        last_aka = utility.get_current_aka()
        handle = utility.get_ui_handle()
        is_one_check = False
        for tab in tab_map:
            aka = tab.get("Aka")
            result = handle.get_is_checked(aka)
            if result and aka not in last_aka:
                is_one_check = True
                utility.set_current_aka(aka)
                handle.set_collapsed(aka + "_sbox", False)
            else:
                handle.set_is_checked(aka, False)
                handle.set_collapsed(aka + "_sbox", True)
        if not is_one_check:
            handle.set_is_checked(last_aka, True)
            handle.set_collapsed(last_aka + "_sbox", False)
        

def callback():
    for callback in set(dir(TabBack))-set(dir(object)):
        if callback not in ['__dict__', '__module__', '__weakref__']:
            getattr(TabBack, callback)()