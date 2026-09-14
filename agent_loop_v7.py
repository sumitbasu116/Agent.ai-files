import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------
# 1. Our actual tool
# -------------------------
def get_user_name():
    return "Sumit"

def calculator(a, b, operation):

    if operation == "add":
        return a + b

    elif operation == "subtract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    elif operation == "power":
        return a ** b

    else:
        raise ValueError("Unknown operation")

# -------------------------
# tool_registry
# -------------------------
tool_registry = {
    "calculator": calculator,
    "get_user_name": get_user_name
}

# -------------------------
# 2. Tool definition
# -------------------------

tools = [
    {
       "type": "function",
       "function": {
          "name":"get_user_name",
          "description": "This is the name of the user.",
          "parameters": {},
          "required":[]
        }
    },
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
            You are an AI assistant with access to tools.

            Tool usage rules:

            1. If a user request requires an operation that is supported
            by an available tool, MUST use that tool.

            2. Do NOT perform an operation yourself when an available tool
            can perform that operation.

            3. If an operation is NOT supported by any available tool,
            you may perform that operation yourself.

            4. After receiving a tool result, continue processing the user's
            request and determine whether another tool is required.

            5. Use tools as many times as necessary to complete the user's request.

            6. Do not invent or modify tool names.

            7. Only provide the final answer when the user's complete request
            has been handled.
            """
    },
    {
        "role": "user",
        "content": user_question
    }
]
state = { 
            "messages": messages, 
            "step": 0, 
            "tool_results": [],
            "status": "running"
         }

# -------------------------
# 4. AGENT LOOP
# -------------------------
while True:
    state["step"] += 1
    print(f"\n===== AGENT STEP {state['step']} =====")
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=state["messages"],
        tools=tools,
        tool_choice="auto"
    )
    message = response.choices[0].message

    # -------------------------
    # No tool needed
    # -------------------------
    if not message.tool_calls:
        state["status"] = "completed"
        print("\nFinal answer:",message.content)
        break
    # -------------------------
    # Tool requested
    # -------------------------
    state["messages"].append(message) # add the latest response

    for tool_call in message.tool_calls:
        tool_name=tool_call.function.name
        arguments = json.loads(
            tool_call.function.arguments
        )
        print("\nLLM requested tool:", tool_name)
        print("Arguments:",arguments)

        tool=tool_registry.get(tool_name)

        if tool is None:
            result=f"Unknown Tool:{tool_name}"
        else:
            try:
                # Automatically pass the arguments
                result=tool(**arguments)
            except Exception as e:
                result=f"Tool error:{str(e)}"

        state["tool_results"].append(
            {
                "tool": tool_name,
                "arguments": arguments,
                "result": result
            }
        )
        print("Tool result:", result)
        # Give the result back to the LLM
        state["messages"].append(
            {
                "role":"tool",
                "tool_call_id":tool_call.id,
                "content":str(result)
            }
        )
# ------ # 9. Display final Agent state # ------
print("\n===== FINAL STATE =====") 
print("\nAgent steps:", state["step"]) 
print("Status:", state["status"])
print("\nTool results:") 
for item in state["tool_results"]: 
    print(item)
