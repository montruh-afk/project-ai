import os, os.path
from google.genai import types

schema_remove_empty_dir = types.FunctionDeclaration(
    name="remove_empty_dir",
    description="Removes an empty directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "dir_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the directory to remove",
            ),
        },
    ),
)

def remove_empty_dir(working_directory, dir_path):
    """Removes an empty directory.

    Args:
        dir_path (str): The path to the directory to remove.

    Returns:
        str: A message indicating success or failure.
    """
    dir = os.path.abspath(os.path.join(working_directory, dir_path))
    try:
        os.rmdir(dir)
        return f"Successfully removed empty directory '{dir_path}'"
    except FileNotFoundError:
        return "Error: Directory not found."
    except OSError as e:
        return f"Error removing directory: {e}"