import os
import shutil

extensiontofile = {
    ".jpg": "Images",
    ".docx": "Word documents",
    ".m4a": "M4a files",
    ".pptx": "Powerpoint slides",
    ".bat": "Batch files",
    ".txt": "Text files",
    ".aseprite": "Aseprite files",
    ".png": "Images",
    ".py": "Python files",
    ".mp4": "Videos",
    ".pdf": "Pdf files",
    ".xlsx": "Excel spreadsheets",
    ".rtf": "Word documents",
    ".jpeg": "Images",
    ".mp4": "Videos",
    ".pptm": "Powerpoint slides",
    ".exe": "Executables",
    ".msi": "Microsoft install_wizards",
    ".msix": "Microsoft install_wizards"
}

directory = input("Copy the desired file directory to be organised: ")
def folder_creations(directory):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isdir(file_path):
            continue
        extension = os.path.splitext(file)[-1].lower()
        if extension in extensiontofile:
            try:
                os.mkdir(directory + "/" + extensiontofile[extension])
                print(f"made directory {extensiontofile[extension]}")
            except FileExistsError:
                pass
            except PermissionError:
                print("Lack of permissions, cannot organise this directory.")
                return
            except Exception as error:
                print(f"An error occurred: {error}")
        else:
            try:
                name = str(file).split(".", 1)
                print(name)
                os.mkdir(directory + "/" + name[1] + " files")
                print(f"made directory {name[1] + " files"}")
                extensiontofile["." + name[1]] = name[1] + " files"
            except FileExistsError:
                pass
            except PermissionError:
                print("Lack of permissions, cannot organise this directory.")
                return
            except Exception as error:
                print(f"An error occurred: {error}")

def organize_files(directory):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isdir(file_path):
            continue
        extension = os.path.splitext(file)[-1].lower()
        try:
            new_dir = os.path.join(directory, extensiontofile[extension])
            new_dir = os.path.join(new_dir, file)
        except Exception as error:
            print(f"An error occurred: {error}")
            continue
        shutil.move(os.path.join(directory, file), new_dir)

folder_creations(directory)
organize_files(directory)

wait = input()