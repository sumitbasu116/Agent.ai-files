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

# Simulated LLM decision
tool_call = {
    "name": "calculator",
    "arguments": {
        "a": 25,
        "b": 4,
        "operation": "multiply"
    }
}
# Application reads the LLM's decision
if tool_call["name"] == "calculator":
    args = tool_call["arguments"]
    result = calculator(
        args["a"],
        args["b"],
        args["operation"]
    )
print("Tool result:", result)