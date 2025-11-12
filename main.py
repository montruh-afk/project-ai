# python
import os, sys
from dotenv import load_dotenv
import google.genai as genai
from google.genai.types import Content, Part



def parse_args(argv):
    # treat the first argument as the prompt (quoted by the shell)
    prompt = None
    verbose = False
    rest = []
    for a in argv:
        if a == "--verbose":
            verbose = True
        elif prompt is None:
            prompt = a
        else:
            rest.append(a)
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
        model="gemini-2.0-flash-001",
        contents=messages,
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