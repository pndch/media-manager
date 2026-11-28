import os
import shutil

RESULT_FOLDER_PATH = r'E:\folder\result'
MEDIA_FOLDER_PATH = r'E:\folder\media'

def move_in_folder(names: list):
    for name in names:
        result_path_name = os.path.join(RESULT_FOLDER_PATH, name)
        media_path_name = os.path.join(MEDIA_FOLDER_PATH, name)

        shutil.move(media_path_name, result_path_name)

def move_out_folder(names: list):
    for name in names:
        result_path_name = os.path.join(RESULT_FOLDER_PATH, name)
        media_path_name = os.path.join(MEDIA_FOLDER_PATH, name)

        shutil.move(result_path_name, media_path_name)