import os, os.path
from google.genai import types


schema_create_file = types.FunctionDeclaration(
    name="create_file",
    description="creates files in a directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_name": types.Schema(
                type=types.Type.STRING,
                description="The file to create, relative to the working directory. If not provided, aborts."
            ),
            "file_directory": types.Schema(
                type=types.Type.STRING,
                description="The directory where the file will be created, relative to the working directory. If not provided, aborts."
            )
        },
    ),
)


def create_dir(directory):
    os.mkdir(directory)
    return directory

def create(file_path, file_name):
    file = os.path.join(file_path, file_name)
    try:
        with open(file, "a"):
            return f'{file_name} was created successfully in {file_path}'
    except Exception as e:
        return f'An error occoured: {e}'


def create_file(working_directory, file_directory, file_name):
    # Absolute path to the working directory
    dir = os.path.abspath(working_directory)
    
    # Pathname up until the final directory (does not include files in said directory)
    absolute_path = os.path.abspath(os.path.join(working_directory, file_directory))
    print(absolute_path)
    
    if not absolute_path.startswith(dir):
        return f'Error: Cannot create a file in {file_directory} as it is outside the permitted working directory'
    if not os.path.exists(absolute_path):
        absolute_path = create_dir(absolute_path)
        return create(absolute_path, file_name)
    if os.path.isdir(absolute_path):
        return create(absolute_path, file_name)
    
    