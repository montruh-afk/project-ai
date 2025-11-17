# python
import os, sys
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types
from google.genai.types import Content, Part
from variables import *
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file



def parse_args(argv):
    # treat the first argument as the prompt (quoted by the shell)
    prompt = None
    verbose = False
    if "--verbose" in argv:
        verbose = True
        prompt = ' '.join(argv).replace("--verbose", '')
    else:
        prompt = ' '.join(argv)
    return prompt, verbose

prompt, verbose = parse_args(sys.argv[1:])

def call_function(function_call_part, verbose=False):
    args = function_call_part.args
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
    function_result = function_name[function_call_part.name](**function_call_part.args)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
                )
            ],
        )



def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Missing GEMINI_API_KEY")
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    
    if not prompt:
        print("Missing required input: *prompt*")
        sys.exit(1)
    
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
            ]
        )
    
    messages = [Content(role="user", parts=[Part(text=prompt)])]
    
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=SYSTEM_PROMPT)
    ) 
    
    
    
    if not response.function_calls:
        print(response.text)
    else:
        for functions in response.function_calls:
            result = call_function(functions, verbose)
            if not result.parts[0].function_response.response:
                raise Exception("An Unrecoverable error occoured")
            elif verbose:
                print(f"-> {result.parts[0].function_response.response}")
            
    if verbose:
        print(f'User prompt: {prompt}')
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

if __name__ == "__main__":
    main()