import os, os.path
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes python files with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to run, relative to the working directory. If not provided, runs the file in the working directory itself.",
            ),
        },
    ),
)

def running(dir, file_path, args=[]):
        try:
            process = subprocess.run(["python", file_path, *args], capture_output=True, text=True, cwd=dir, timeout=30)
            return_code = process.returncode
            
            if not process.stderr and not process.stdout:
                return "No output produced."
            return f'STDOUT: {process.stdout}\nSTDERR: {process.stderr if process.stderr else None}\n{'' if return_code == 0 else f'Process exited with code {return_code}'}'
        except Exception as e:
            return f"Error: executing Python file: {e}"

def run_python_file(working_directory, file_path, args=[]):
    abspth = os.path.abspath(os.path.join(working_directory, file_path))
    dir = os.path.abspath(working_directory)
    
    if not abspth.startswith(dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not abspth.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    if not os.path.exists(abspth):
        return f'Error: File "{file_path}" not found.'
    
    return running(dir, file_path, args)