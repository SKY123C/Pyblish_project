import os

def get_all_plugin_path():
    result = []
    current_dir = os.path.dirname(__file__)
    for d in os.listdir(current_dir):
        full_path = os.path.join(current_dir, d)
        if os.path.isdir(full_path) and d != "__pycache__":
            result.append(full_path)
    return result