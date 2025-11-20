import os, os.path
from google.genai import types


schema_delete_file = types.FunctionDeclaration(
    name="delete_file",
    description="Deletes files, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to delete, relative to the working directory. If not provided, aborts.",
            ),
        },
    ),
)

schema_delete_conversation_history = types.FunctionDeclaration(
    name="delete_conversation_history",
    description="Deletes the .json file that holds the conversation history, does not accept any arguments."
    )

def delete_conversation_history(working_directory=None):
    try:
        os.remove(os.path.abspath("./functions/saves/conversation_log.json"))
        return f'Successfully cleared conversation history'
    except FileNotFoundError:
        return f'It seems our conversation logs are missing'
    except Exception as e:
        return f'Error: {e}'


def delete(absolute_path, file_path):
    try:
        os.remove(absolute_path)
        return f'Deleted {file_path}'
    except Exception as e:
        return f'An error occoured: {e}'


def delete_file(working_directory, file_path):
     # Relative path from root
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Absolute path to the working directory
    dir = os.path.abspath(working_directory)
    
    # Pathname up until the final directory (does not include files in said directory)
    path_to_last_dir = os.path.join(working_directory, os.path.dirname(file_path))
    
    if not absolute_path.startswith(dir):
        return f'Error: Cannot alter any files in the directory which "{file_path}" is located in as it is outside the permitted working directory'
    if os.path.isdir(absolute_path):
        return f'Due to security concerns, I am not able to delete entire directories'
    if not os.path.exists(absolute_path):
        return 'File does not exist'
    return delete(absolute_path, file_path)