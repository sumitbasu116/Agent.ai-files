import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------
# 1. Our actual tool
# -------------------------

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

    elif operation == "power":
        return a ** b

    else:
        return "Unknown operation"

# -------------------------
# 2. Tool definition
# -------------------------

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
                            "divide",
                            "power"
                        ],
                        "description": "Mathematical operation"
                    }
                },
                "required": ["a", "b", "operation"]
            }
        }
    }
]
# -------------------------
# 3. User question
# -------------------------
user_question = input("Ask me anything:")
messages = [
    {
        "role": "system",
        "content": """
        You are an AI assistant with access to a calculator tool.

        When a calculation operation is supported by the calculator,
        prefer using the calculator instead of calculating it yourself.

        If an operation is not supported by the calculator,
        you may perform that operation yourself.

        After receiving a tool result, determine what to do next.
        Continue using tools when necessary.
        Only provide the final answer when the task is complete.
        """
    },
    {
        "role":"user",
        "content":user_question
    }
]
# -------------------------
# 4. AGENT LOOP
# -------------------------
while True:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    message = response.choices[0].message

    # -------------------------
    # No tool needed
    # -------------------------
    if not message.tool_calls:
        print("\nFinal answer:",message.content)
        break
    # -------------------------
    # Tool requested
    # -------------------------
    messages.append(message) # add the latest response

    for tool_call in message.tool_calls:
        tool_name=tool_call.function.name
        arguments = json.loads(
            tool_call.function.arguments
        )
        print("\nLLM requested tool:", tool_name)
        print("Arguments:",arguments)

        if tool_name=="calculator":
            result = calculator(
                arguments["a"],
                arguments["b"],
                arguments["operation"]
            )
        else:
            result="Unknown Tool"

        print("Tool result:", result)

        # Give the result back to the LLM
        messages.append(
            {
                "role":"tool",
                "tool_call_id":tool_call.id,
                "content":str(result)
            }
        )
