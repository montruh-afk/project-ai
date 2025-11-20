import json
from functions.converter import *
from functions.config import *
from google.genai.types import Content, Part


def load_messages(initial_prompt: str):
    if LOG_PATH.exists():
        with LOG_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        # rebuild Content objects
        msgs = [dict_to_content(c) for c in data]
        # optionally append new prompt as a fresh turn
        if initial_prompt:
            msgs.append(Content(role="user", parts=[Part(text=initial_prompt)]))
        return msgs
    else:
        return [Content(role="user", parts=[Part(text=initial_prompt)])]
    
def save_messages(messages):
    data = [content_to_dict(c) for c in messages]
    with LOG_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)