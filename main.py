# python
import os, sys
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types
from google.genai.types import Content, Part
from functions.config import *
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.delete import schema_delete_file, delete_conversation_history, schema_delete_conversation_history
from functions.create_file import schema_create_file
from functions.load import *
from functions.rename_fileordir import schema_rename_fileordir
from functions.remove_empty_dir import schema_remove_empty_dir

load_dotenv()

# ensure the folder exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

def parse_args(argv):
    prompt = None
    verbose = False
    clear = False
    try:
        if "--verbose" in argv:
            verbose = True
            argv.remove("--verbose")
        if "--clear" in argv:
            clear = True
            argv.remove("--clear")
    except ValueError:
        pass  # Handle the case where the flag is not in the list
    prompt = ' '.join(argv)
    return prompt, verbose, clear

runs = 0
prompt, verbose, clear = parse_args(sys.argv[1:])
messages = load_messages(prompt)

def call_function(function_call_part, verbose=False, get_part=False):
    args = dict(function_call_part.args)
    args["working_directory"] = "."
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    if function_call_part.name not in ALLOWED_OPERATIONS:
        return types.Content(
            role="tool", 
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )
    function_result = function_name[function_call_part.name](**args)
    tool_content = types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
                )
            ],
        )
    
    return tool_content


def main():
    try:
        global runs
        while runs < MAX_ITERATIONS:
            result_parts = []
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                print("Missing GEMINI_API_KEY")
                sys.exit(1)

            client = genai.Client(api_key=api_key)
            if not prompt:
                if clear:
                    print(delete_conversation_history("."))
                else:
                    print("Missing required input: A prompt\nCommands: --clear to clear conversation history, --verbose to show more info")
                sys.exit(1)
            
            
            available_functions = types.Tool(
                function_declarations=[
                    schema_get_files_info,
                    schema_get_file_content,
                    schema_run_python_file,
                    schema_write_file,
                    schema_delete_file, 
                    schema_create_file,
                    schema_remove_empty_dir,
                    schema_rename_fileordir
                    ]
                )
            
            
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT)
            ) 
            
            finished = (not response.function_calls) and bool(response.text)
            if finished:
                print(response.text)
                try:
                    save_messages(messages)
                except Exception as e:
                    print(f"Error saving messages: {e}")
                if verbose:
                    print(f'User prompt: {prompt}')
                    print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
                    print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
                break
            else:
                for functions in response.function_calls:
                    result = call_function(functions, verbose)
                    if not result.parts[0].function_response.response:
                        raise Exception("An Unrecoverable error occoured")
                    elif verbose:
                        print(f"-> {result.parts[0].function_response.response}")
                    result_parts.append(result.parts[0])
           
            if response.candidates:
                    for c in response.candidates:
                        if c and c.content:
                            messages.append(c.content)
                        
            if result_parts:
                messages.append(types.Content(role="user", parts=result_parts)) 
            try:
                save_messages(messages)
            except Exception as e:
                print(f"Error saving messages: {e}")

            runs += 1
    except Exception as e:
        print(f'Something went wrong: {e}')
        try:
            save_messages(messages)
        except Exception as e:
            print(f"Error saving messages: {e}")

if __name__ == "__main__":
    main()
