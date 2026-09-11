import os
import json
from dotenv import load_dotenv
from groq import Groq

# Load .env
load_dotenv()

# Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Our actual Python tool
def calculator(a, b, operation):

    if operation == "add":
        return a + b

    elif operation == "subtract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":
        if b == 0:
            return "Cannot divide by zero"
        return a / b

    else:
        return "Unknown operation"

# Describe the tool to the LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Performs basic mathematical calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    },
                    "operation": {
                        "type": "string",
                        "enum": [
                            "add",
                            "subtract",
                            "multiply",
                            "divide"
                        ],
                        "description": "Mathematical operation"
                    }
                },
                "required": ["a", "b", "operation"]
            }
        }
    }
]

# User's question
num1 = float(input("Enter First Number:"))
num2 = float(input("Enter Second Number:"))
oper = input("Enter the operation:")
messages = [
    {
        "role": "user",
        "content": f"What is {num1} {oper} by {num2}?"
    }
]

# Ask the LLM
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# Look at the LLM response
message = response.choices[0].message
# 2. Get LLM's tool call
tool_call = message.tool_calls[0]
print("Tool name:", tool_call.function.name)
print("Arguments:", tool_call.function.arguments)
# 3. Extract arguments
arguments = json.loads(tool_call.function.arguments)

print(arguments)
# 4. Execute Python tool
result = calculator(
    arguments["a"],
    arguments["b"],
    arguments["operation"]
)
print("Tool result:", result)

# 5. Give LLM the tool result
messages.append(message)
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": str(result)
})

# 6. Ask LLM for final answer
final_response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=messages,
    tools=tools
)

# 7. Print final answer
final_answer = final_response.choices[0].message.content

print("Final answer:", final_answer)