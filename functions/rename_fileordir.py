import os, os.path
from google.genai import types

schema_rename_fileordir = types.FunctionDeclaration(
    name="rename_fileordir",
    description="Renames a file or directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "old_path": types.Schema(
                type=types.Type.STRING,
                description="The current name of the file or directory along with its parent directory if not the working directory.",
            ),
            "new_path": types.Schema(
                type=types.Type.STRING,
                description="The new name of the file or directory along with its parent directory if not the working directory.",
            )
        },
    ),
)


def rename_fileordir(working_directory, old_path, new_path):
    """Renames a file or directory.

    Args:
        old_path (str): The current path to the file or directory.
        new_path (str): The new path to the file or directory.

    Returns:
        str: A message indicating success or failure.
    """
    old = os.path.abspath(os.path.join(working_directory, old_path))
    new = os.path.abspath(os.path.join(working_directory, new_path))
    try:
        os.rename(old, new)
        return f"Successfully renamed '{old}' to '{new}'"
    except FileNotFoundError:
        return "Error: File or directory not found."
    except Exception as e:
        return f"Error renaming file or directory: {e}"
