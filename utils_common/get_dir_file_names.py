import os

cur_dir_files_names = []
def get_directory_file_names(full_dir_path):
    for entry_name in os.listdir(full_dir_path):
        full_file_path = os.path.join(full_dir_path, entry_name)
        if os.path.isfile(full_file_path):
            cur_dir_files_names.append(entry_name)
    return cur_dir_files_names
