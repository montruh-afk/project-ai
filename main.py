# python
import os, sys
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types
from functions.config import *
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.delete import schema_delete_file, delete_conversation_history, schema_delete_conversation_history
from functions.create_file import schema_create_file
from functions.load import *



# ensure the folder exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

def parse_args(argv):
    # treat the first argument as the prompt (quoted by the shell)
    prompt = None
    verbose = False
    clear = False
    if "--verbose" or "--Verbose" in argv:
        verbose = True
        prompt = ''.join(argv).replace("--verbose", '')
    if "--clear" or "--Clear" in argv:
        clear = True
        prompt = ' '.join(argv).replace("--clear", '').replace("--Clear", '')
    else:
        prompt = ' '.join(argv)
    return prompt, verbose, clear

runs = 0
prompt, verbose, clear = parse_args(sys.argv[1:])
messages = load_messages(prompt)

def call_function(function_call_part, verbose=False, get_part=False):
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"
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
        #max iterations defaults to 20
        while runs < MAX_ITERATIONS:
            result_parts = []
            
            
            load_dotenv()
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                print("Missing GEMINI_API_KEY")
                sys.exit(1)

            client = genai.Client(api_key=api_key)
            if not prompt:
                if clear:
                    print(delete_conversation_history())
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
                save_messages(messages)
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
            save_messages(messages)
            if verbose:
                print(f'User prompt: {prompt}')
                print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
                print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
            
            runs += 1
    except Exception as e:
        print(f'Something went wrong: {e}')
        save_messages(messages)

if __name__ == "__main__":
    main()