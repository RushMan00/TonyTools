import os
import shutil

def check_path_exists(path):
    path = path.replace("\\", "/")  # replace backslashes with forward slashes
    if os.path.exists(path):
        print(f"The path exists: {path}")
        return True
    else:
        print(f"The path does not exist: {path}")
        return False
def sort_files_by_creation(path, base_filename):
    path = path.strip().replace("\\", "/")  # strip leading/trailing spaces and replace backslashes with forward slashes
    path = path.strip()  # strip leading/trailing spaces

    # Getting all files
    files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    # Sorting files by creation time
    files.sort(key=lambda x: os.path.getctime(x))

    # Renaming and moving files
    for i, file in enumerate(files, start=1):
        _, ext = os.path.splitext(file)
        new_name = f"{base_filename}_{str(i).zfill(2)}{ext}"
        new_file = os.path.join(path, new_name)

        # Rename files
        shutil.move(file, new_file)
        print(f"Renamed file {file} to {new_file}")

if __name__ == "__main__":
    path = input("Enter a path: ").strip()  # strip leading/trailing spaces
    if check_path_exists(path):
        base_filename = input("Enter base filename: ").strip()  # strip leading/trailing spaces
        sort_files_by_creation(path, base_filename)