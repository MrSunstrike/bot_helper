import os


def check_and_create_file(file_path: str):
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("")
