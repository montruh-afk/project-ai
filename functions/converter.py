from google.genai import types
from google.genai.types import Content, Part
from functions.config import *

def content_to_dict(content: Content) -> dict:
    return {
        "role": content.role,
        "parts": [
            {
                "text": p.text if hasattr(p, "text") else None,
                "function_call": (
                    {
                        "name": p.function_call.name,
                        "args": p.function_call.args,
                    }
                    if getattr(p, "function_call", None)
                    else None
                ),
                "function_response": (
                    {
                        "name": p.function_response.name,
                        "response": p.function_response.response,
                    }
                    if getattr(p, "function_response", None)
                    else None
                ),
            }
            for p in content.parts
        ],
    }


def dict_to_content(d: dict) -> Content:
    parts = []
    for p in d["parts"]:
        if p["function_call"]:
            parts.append(
                types.Part.from_function_call(
                    name=p["function_call"]["name"],
                    args=p["function_call"]["args"],
                )
            )
        elif p["function_response"]:
            parts.append(
                types.Part.from_function_response(
                    name=p["function_response"]["name"],
                    response=p["function_response"]["response"],
                )
            )
        else:
            parts.append(types.Part(text=p["text"]))

    return types.Content(role=d["role"], parts=parts)