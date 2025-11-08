import os
from dotenv import load_dotenv
from google import genai
import sys


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)


    if len(sys.argv) < 2:
        print("Missing required input")
        sys.exit(1)
    input = sys.argv[1:]
    response = client.models.generate_content(model='gemini-2.0-flash-001', contents=(f'"{input}"') if not isinstance(input, str) else input)

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    print(response.text)
    print(f'Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}')




if __name__ == "__main__":
    main()
