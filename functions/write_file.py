import os, os.path
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file specified",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory.",
            ),   
        },
    ),
)


def write_content(file_path, content) -> str:
    try:
        with open(file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            
    except IsADirectoryError:
        return f'Error writing content to {file_path}: is a directory'
    except FileNotFoundError:
        return f'Error: the file at {file_path} does not exist.'
    except PermissionError:
        return f'Error: You do not have the required permission to access the file.'
    except OSError as e:
        return f"Error reading file: {e}"
        



def write_file(working_directory, file_path, content):
    # Relative path from root
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Absolute path to the working directory
    dir = os.path.abspath(working_directory)
    
    # Pathname up until the final directory (does not include files in said directory)
    path_to_last_dir = os.path.join(working_directory, os.path.dirname(file_path))
    
    if not absolute_path.startswith(dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(os.path.abspath(path_to_last_dir)):
        os.makedirs(os.path.abspath(path_to_last_dir))
    
    
    return write_content(absolute_path, content)
    