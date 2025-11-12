import os, os.path
from functions.config import *


def read_file_content(file_path):
    file_content_string = ''
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file_content_string = f.read()
            if len(file_content_string) > MAX_CHARS:
                return file_content_string[:MAX_CHARS] + f'\nFile at "{file_path}" truncated at {MAX_CHARS} characters'
            return file_content_string
    except FileNotFoundError:
        return "Error: File does not exist"
    except PermissionError:
        return "Error: You don't have the required permissions to access this file"
    except OSError as e:
        return f"Error reading file: {e}"

def get_file_content(working_directory, file_path):
    # fp stands for file path
    relative_fp = os.path.join(working_directory, file_path)
    absolute_fp = os.path.abspath(relative_fp)
    if not absolute_fp.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(absolute_fp):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    return read_file_content(absolute_fp)