import os
import shutil

extensiontofile = {
    ".jpg": "Images",
    ".docx": "Word_documents",
    ".m4a": "M4a_files",
    ".pptx": "Powerpoint_slides",
    ".bat": "Batch_files",
    ".txt": "Text_files",
    ".aseprite": "Aseprite_files",
    ".png": "Images",
    ".py": "Python_files",
    ".mp4": "Videos",
    ".pdf": "Pdf_files",
    ".xlsx": "Excel_spreadsheets",
    ".rtf": "Word_documents",
    ".jpeg": "Images",
    ".mp4": "Videos",
    ".pptm": "Powerpoint_slides",
    ".exe": "Executables",
    ".msi": "Microsoft_install_wizards",
    ".msix": "Microsoft_install_wizards"
}

directory = input("Copy the desired file directory to be organised: ")

for file in os.listdir(directory):
    file_path = os.path.join(directory, file)
    if os.path.isdir(file_path):
        continue
    extension = os.path.splitext(file)[-1].lower()
    try:
        os.mkdir(directory + "/" + extensiontofile[extension])
        print(f"made directory {extensiontofile[extension]}")
    except FileExistsError:
        pass
    except PermissionError:
        print("Lack of permissions, cannot organise this directory.")
    except Exception as error:
        print(f"An error occurred: {error}")

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

wait = input()