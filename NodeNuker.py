import os
import shutil

def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Deleted: {folder_path}")
    except Exception as e:
        print(f"Failed to delete {folder_path}. Reason: {e}")

def find_and_delete(target_folders):
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name in target_folders:
                folder_path = os.path.join(root, dir_name)
                delete_folder(folder_path)

if __name__ == "__main__":
    target_folders = ['node_modules', 'venv']
    find_and_delete(target_folders)
