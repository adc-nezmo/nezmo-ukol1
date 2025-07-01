import os
import openai
from dotenv import load_dotenv
import json

# Načti klíč z .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
print("DEBUG API KEY:", os.getenv("OPENAI_API_KEY"))  # To by mělo vypsat začátek klíče

# TADY vytvoř klienta!
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def add(a: int, b: int) -> int:
    return a + b

tools = [
    {
        "type": "function",
        "function": {
            "name": "add_two_numbers",
            "description": "Sečte dvě celá čísla",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "První číslo"},
                    "b": {"type": "integer", "description": "Druhé číslo"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

messages = [
    {"role": "user", "content": "Kolik je 47 + 55?"}
]

response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)

message = response.choices[0].message

if hasattr(message, "tool_calls") and message.tool_calls:
    for tool_call in message.tool_calls:
        if tool_call.function.name == "add_two_numbers":
            args = json.loads(tool_call.function.arguments)
            vysledek = add(args["a"], args["b"])
            print(f"Výsledek z Python funkce: {vysledek}")
else:
    print(message.content)