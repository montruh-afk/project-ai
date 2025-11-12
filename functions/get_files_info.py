import os.path

def file_size(absolute_path) -> str:
    try:
        contents = []
        items = os.listdir(absolute_path)
        for item in items:
            path = os.path.join(absolute_path, item)
        
            contents.append(f'{item}: file_size={os.path.getsize(path)}, is_dir={os.path.isdir(path)}')
        return "\n".join(contents)
    except FileNotFoundError:
        return "Error: File does not exist"
    except PermissionError:
        return "You don't have the required permissions to access this folder"
    except OSError as e:
        return f"Error reading file: {e}"
    
    

def get_files_info(working_directory, directory="."):
    
    # relative path to file
    relative_path = os.path.join(working_directory, directory)
    # print(f'relative path: {relative_path}')
    
    # absolute path to second positional argument
    absolute_path = os.path.abspath(relative_path)
    # print(f'absolute path: {absolute_path}')
    
    # dir is the absolute path to the working directory
    dir = os.path.abspath(working_directory)
    # print(f'directory: {dir}')
    
    if not absolute_path.startswith(dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(absolute_path):
        return f'Error: "{directory}" is not a directory'
    return file_size(absolute_path)