# python
import os, sys
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types
from google.genai.types import Content, Part
from variables import *



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

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Missing GEMINI_API_KEY")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    prompt, verbose = parse_args(sys.argv[1:])
    if not prompt:
        print("Missing required input: *prompt*")
        sys.exit(1)

    messages = [Content(role="user", parts=[Part(text=prompt)])]
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
    )

    if verbose:
        print(response.text)
        print(f'User prompt: {prompt}')
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    else:
        print(response.text)

if __name__ == "__main__":
    main()