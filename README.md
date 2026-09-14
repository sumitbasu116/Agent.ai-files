# Agentic AI flow
## Part 1
```
1.hello_ai.py
2.agent_v1.py
3.agent_v2.py
```
Here, we have written a calculator using Python as the programming language. We are then trying to replicate a simple Agentic AI flow.
The LLM should understand the user's request and decide whether it needs to call the calculator tool. Whenever the user asks for a mathematical operation, the LLM should identify the required operation and the input numbers, and then call the calculator.
#### Our calculator currently supports five operations: `Addition,Subtraction,Multiplication,Division,Power`
>
        USER
          ↓
        LLM
          ↓
    Tool selection
          ↓
    Python function
          ↓
       Result
          ↓
        LLM
          ↓
    Final response
          ↓
        USER
## Part 2
```
agent_v3.py
```
Here, the agent becomes little powerful, it can now think directly from the user questions and extract the argument instead of hardcoding it in the program. It can also think and reply if an operation is not supported.
```
                User question
                     ↓
                    LLM
                     ↓
                LLM understands the question
                 ┌─────────┴─────────┐
LLM selects calculator       LLM final answer(if operation not supported)
     ↓                                ↓
LLM determines arguments        LLM does not have answer from the Python Calculator tool
     ↓
Python executes calculator
     ↓
Result
     ↓
LLM final answer
```
### Results:
```
Ask me a calculation:  multiply 25 and 26
{'a': 25, 'b': 26, 'operation': 'multiply'}
Result from python calculate function: 650
Final answer: The product of 25 and 26 is **650**.

Ask me a calculation: modulas of 2 and 1
LLM does not have answer from the Python Calculator tool
```
## Part 3
```
agent_v4.py
```
Here, the agent becomes more powerful. It can decide whether to call the Calculator tool to perform a mathematical operation, or answer the user's question directly using the LLM's own knowledge.
For example:
User: "What is 25 multiplied by 4?"
→ Agent decides to call the Calculator tool.
User: "What is Machine Learning?"
→ Agent decides that no tool is required and answers directly using the LLM.
```
                    User
                      │
                      ▼
                    LLM
                      │
             tool_choice="auto"
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
       Tool required?       No tool
             │                 │
            YES                NO
             │                 │
             ▼                 ▼
       calculator()       Answer directly
             │                 │
             ▼                 │
          result                │
             │                 │
             └────────┬─────────┘
                      ▼
                    User
```
### Results
```
Ask me a calculation: divide 3 by 3
{'a': 3, 'b': 3, 'operation': 'divide'}
Result from python calculate function: 1.0
Final answer: 3 divided by 3 equals **1**.

Ask me a calculation: Hello! who are you?
LLM answer: Hi there! I’m ChatGPT, an AI language model created by OpenAI.
```
> The only difference b/n agent v3 and agent v4 is that Agent v4 can answer the operations or question which is not in the tool or python calculator function.
### important point
`tool_choice="auto"` does not mean:
It means:
> **The LLM is allowed to decide whether to request a tool call.**
<br>The application still executes the tool.

## Part 4
```
agent_loop.py
```
Till **Part 3**, we have only one tool. What if there is a need of multiple tools. E.g. multiply 200,5 then add 3 to it.
Let's understand few concepts first.
### Agent vs normal LLM
#### Normal LLM call:
```
User
 ↓
LLM
 ↓
Answer
```
#### LLM with one tool call:
```
User
 ↓
LLM
 ↓
Tool
 ↓
LLM
 ↓
Answer
```
#### Agent:
```
User
 ↓
LLM
 ↓
Decide
 ↓
Tool
 ↓
Result
 ↓
LLM
 ↓
Decide
 ↓
Tool
 ↓
Result
 ↓
LLM
 ↓
...
 ↓
Final answer
```
So an Agent is not simply:
> An LLM with tools.

A more useful mental model is: **Interview Question**
> An Agent is an LLM-driven decision loop that can repeatedly choose actions/tools, observe their results, and continue until it can produce a final answer.

Take your existing code and think of the flow as:
>
    while True:
    Ask LLM: "What should I do?"
    ├── Tool call?
    │      ↓ YES
    │   Execute calculator
    │      ↓
    │   Give result back to LLM
    │      ↓
    │   Go back to the top
    │
    └── No tool call
           ↓
       Final answer
           ↓
          break
The important part is that the LLM gets another chance to `make a decision` after `every tool result`.<br>
Now, check the `agent_loop.py` program and understand the step by step.
<br> The crucial line is:
<br> `while True:`
Because, after calculating multiply 200,5, <br> The program doesn't say:
> I'm done.

It says:<br> 
> Let's ask the LLM what I should do next.

That's the core idea behind the Agent Loop.<br>
We also used:
> for tool_call in message.tool_calls:

rather than:<br>
> message.tool_calls[0]

because an LLM can potentially request multiple tools in one response.<br>
Let's understand: `messages.append(message)`
#### What is message?
Earlier we did:
```
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)
message = response.choices[0].message
```
Suppose the user asks:
```
Multiply 25 and 26
```
The LLM may return something like:
```
message:
    role = assistant
    content = None
    tool_calls =
        calculator(
            a = 25,
            b = 26,
            operation = "multiply"
        )
```
**So `message` represents the LLM's latest response.**
#### What is inside messages?
Remember that `messages` is our conversation history.<br>
Initially:
```
messages = [
    {
        "role": "user",
        "content": "Multiply 25 and 26"
    }
]
```
So:
```
messages
   |
   └── User: Multiply 25 and 26
```
Then we call the LLM.<br>
The LLM says:<br>
> I want to use the calculator.
That response is stored in:<br>
```
message
```
But notice:<br>
**It is not automatically added to messages.** <br>
That's why we do:<br>
```
messages.append(message)
```
#### Why do we need to add it?
Because the next LLM call needs to know what happened previously.<br>
We want our conversation history to become:
```
User:
Multiply 25 and 26

Assistant:
I want to call calculator with:
a = 25
b = 26
operation = multiply

Tool:
650
```
So we do:
```
messages.append(message)
```
which adds the LLM's tool-call response.<br>
Then:
```
messages.append({
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": str(result)
})
```
adds the tool result.<br>
Now `messages` contains:
```
┌─────────────────────────────────────┐
│ User                                │
│ Multiply 25 and 26                  │
├─────────────────────────────────────┤
│ Assistant                           │
│ Call calculator(25, 26, multiply)   │
├─────────────────────────────────────┤
│ Tool                                │
│ Result = 650                        │
└─────────────────────────────────────┘
```
Then we call the LLM again:
```
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)
```
The LLM now sees the complete history.
#### what is Role?
**`role` tells us who produced the message.**
You can think of the conversation as having different participants:
```
"user"       → the user
"assistant"   → the LLM
"tool"       → a tool/application result
```
For example:
```
# User message
{
    "role": "user",
    "content": "What is 25 * 26?"
}
```
Then the LLM might respond:
```
# Assistant message
{
    "role": "assistant",
    "tool_calls": [...]
}
```
Then our Python application executes the calculator and sends the result back:
```
# Tool result message
{
    "role": "tool",
    "tool_call_id": "...",
    "content": "650"
}
```
#### What is tool_call_id?
This part:
```
"tool_call_id": tool_call.id
```
Suppose the LLM says:
```
Assistant:
Please call calculator
ID = abc123
```
Your application executes it:
```
result = calculator(25, 26, "multiply")
```
and gets:
```
650
```
Then we send:
```
{
    "role": "tool",
    "tool_call_id": "abc123",
    "content": "650"
}
```
The `tool_call_id` tells the LLM:
> This result belongs to the tool call with ID abc123.<br>

**It's basically a `correlation` ID.** <br>
**This is our first multi-tool Agent example.**
#### What happens after the below code? How LLM finally printing the result as we never added a request statement to LLM after that?
```
messages.append(
    {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": str(result)
    }
)
```
This is a loop, not a single request.<br>
Then the loop continues automatically:
```
while True:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
```
So the model is called again with the updated conversation, including:<br>
-> the original user message<br>
-> the assistant message that requested the tool<br>
-> the tool result message<br>
At that next model call, the LLM sees the tool output and decides:<br>
-> either call another tool,<br>
**or**<br>
-> produce a normal final answer
Then this line triggers:
```
if not message.tool_calls:
    print("\nFinal answer:", message.content)
    break
```
So the final answer is printed by the LLM in the next iteration of the loop, not in the same tool-call block.

### Results
Example 1:
```
Ask me anything:multiply 20,10 then add 10,30

LLM requested tool: calculator
Arguments: {'a': 20, 'b': 10, 'operation': 'multiply'}
Tool result: 200

LLM requested tool: calculator
Arguments: {'a': 10, 'b': 30, 'operation': 'add'}
Tool result: 40

Final answer: Here are the results of the calculations you requested:

1. **Multiplication**: \(20 \times 10 = 200\)  
2. **Addition**: \(10 + 30 = 40\)
```
Example 2:
```
Ask me anything:multiply 20,10 then add 10,30 and then tell my name

LLM requested tool: calculator
Arguments: {'a': 20, 'b': 10, 'operation': 'multiply'}
Tool result: 200

LLM requested tool: calculator
Arguments: {'a': 10, 'b': 30, 'operation': 'add'}
Tool result: 40

Final answer: - **Multiplication (20 × 10)**: 200  
- **Addition (10 + 30)**: 40  

I don’t have any information about your name. If you’d like me to remember it, just let me know!
```
**Important Example:**
```
Ask me anything:multiply 20,10 then add 10,30 then modulas them

LLM requested tool: calculator
Arguments: {'a': 20, 'b': 10, 'operation': 'multiply'}
Tool result: 200

LLM requested tool: calculator
Arguments: {'a': 10, 'b': 30, 'operation': 'add'}
Tool result: 40

LLM requested tool: calculator
Arguments: {'a': 200, 'b': 40, 'operation': 'add'}
Tool result: 240

Final answer: Here’s the step‑by‑step calculation:

1. **Multiply 20 and 10**  
   \(20 \times 10 = 200\)

2. **Add 10 and 30**  
   \(10 + 30 = 40\)

3. **Modulo (remainder of 200 ÷ 40)**  
   \(200 \div 40 = 5\) with a remainder of **0**.

So, the result of “multiplying 20 and 10, adding 10 and 30, then taking the modulo of the two results” is **0**.
```
current behavior:
```
LLM
 ↓
"Since I know how to calculate everything,
I'll just answer the whole question."
 ↓
Final answer
```
is allowed by `tool_choice="auto"`.<br>
`auto` means:<br>
> Use a tool when you think it is appropriate.

It does not mean:<br>
> Use the calculator whenever a calculation appears.

So the LLM is currently deciding that it can answer the entire calculation itself.
## Part 5
**what is the issue in `Part 4`?**
we haven't explicitly instructed the LLM:
> Prefer using the calculator whenever the operation is supported by the calculator.

So the model has too much freedom.<br>
We can improve this with the tool description.<br>
Instead of:
```
"description": "Performs basic mathematical calculations."
```
we can say:
```
"description": """
Performs mathematical calculations.

Use this tool whenever the user asks you to perform
an operation supported by this calculator.

Supported operations:
add, subtract, multiply, divide, power.

Do not use this tool for unsupported operations.
"""
```
Now we're giving the LLM a clearer policy.

```
agent_loop_v2.py
```
We now have:
```
                    ┌───────────────┐
                    │      LLM      │
                    └───────┬───────┘
                            │
                     What next?
                            │
              ┌─────────────┴─────────────┐
              ↓                           ↓
       Tool available?              No suitable tool
              ↓                           ↓
        Execute tool                LLM handles it
              ↓                           ↓
         Tool result                Continue/final
              │
              └──────────→ LLM
```
### Results
Example 1:
```
Ask me anything:multiply 20,10 then add 10,30 then modulas them

LLM requested tool: calculator
Arguments: {'a': 20, 'b': 10, 'operation': 'multiply'}
Tool result: 200

LLM requested tool: calculator
Arguments: {'a': 10, 'b': 30, 'operation': 'add'}
Tool result: 40

Final answer: The result is **0**.
```
**Important Example 2:**
```
Ask me anything:tell my name then multiply 20,10 then add 10,30

LLM requested tool: calculator
Arguments: {'a': 20, 'b': 10, 'operation': 'multiply'}
Tool result: 200

LLM requested tool: calculator
Arguments: {'a': 10, 'b': 30, 'operation': 'add'}
Tool result: 40

Final answer: I’m sorry, but I don’t know your name.

**Calculations**  
- 20 × 10 = **200**  
- 10 + 30 = **40**
```
**If we look at `Important Example 2` , we have asked `tell my name` first. According to our below code, it should stop executing further calculation**
```
if not message.tool_calls:
        print("\nFinal answer:",message.content)
        break
```
`break` means, it will come out of the `while True` loop and stop the execution.<br>
Instead, LLM does something intelligent here and reorder the operations or tasks.<br>
## Part 6
As of now we don't know whether LLM reorders this or not by doing task planning. However, if we really want that the LLM should follow the ordering then all the tools should be defined. Hence, we have to introduce a new python function to get the user name and include that in the tools.
```
agent_loop_v3.py
```
### Few important understanding
```
LLM
  ↓
decides / requests an action
  ↓
Your Python program
  ↓
executes the function
  ↓
result
  ↓
LLM
```
**Especially understand:** <br>
LLM does not execute Python functions. <br>
Your application executes them. <br>
tool_calls is the LLM's request. <br>
role="tool" carries the result back. <br>
tool_call_id connects the result to the request. <br>
we've already learned most of this.
**Multiple tool calls in one LLM response**
You currently have:
```
for tool_call in message.tool_calls:
```
This is important.<br>
The LLM can potentially return:
```
tool_call 1 → calculator
tool_call 2 → get_user_name
tool_call 3 → calculator
```
in **one response.**
```
LLM response
    ↓
tool
    ↓
LLM response
    ↓
tool
    ↓
LLM response
```
**Tool selection vs tool execution**<br>
This distinction is fundamental.<br>
The LLM makes the decision.<br>
Python performs the action.<br>
Think:
> LLM = brain/decision maker<br>
Python tools = capabilities/actions

This distinction becomes extremely important later with LangGraph, MCP, APIs, databases, etc.<br>
**Tool schemas / structured arguments**
You've already seen:
```
{
  "a": 20,
  "b": 10,
  "operation": "multiply"
}
```
For example:
```
"operation": {
    "type": "string",
    "enum": ["add", "subtract", "multiply", "divide"]
}
```
The schema tells the LLM:
> This is what this tool expects.

You should understand:
```
description
properties
type
required
enum
```
## Part 7 : Dynamic Tool Calling
Here, we will do dynamic tool calling by python application. Imagine , we have 100s of tools, then we end up writing 100s of if-else conditions for each.<br>
We can achieve this by using `first-class function` concept in Python.<br>
The concept is that a function call can be invoked via a variable.<br>
**Step by step:** <br>
**First,** let's include `tool_registry` map/dictionary into our program.
```
tool_registry = {
    "calculator": calculator,
    "get_user_name": get_user_name
}
```
**Second,** include parameter and required details in `get_user_name` function as without this, python will not able to understand about what should be the arguments.
```
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
.....................rest of the tool information.....................
```
**Third,** create a variable `tool` and get the tool name from `tool_registry` for the `tool_call.function.name`.
```
tool=tool_registry.get(tool_call.function.name)
```
**Fourth,** now `tool` variable represents the function name `calculator` or `get_user_name`.<br>
**Similar way,** `tool()` will represents the function `calculator()` or `get_user_name()`.<br>
We have the function arguments from `tool_call.function.arguments`, which we can literally pass as a parameter for `tool()` like below.
```
        if tool is None:
            result=f"Unknown Tool:{tool_name}"
        else:
            # Automatically pass the arguments
            result=tool(**arguments)
```
**Now,** ur code looks truly like a dynamically tool calling agent. Thanks to python.
Full code in:
```
agent_loop_v4.py
```
### Results
Example 1:
```
Ask me anything:print my name first, then multiply 1251 and 789, next, print my name again.

LLM requested tool: get_user_name
Arguments: {}
Tool result: Sumit

LLM requested tool: calculator
Arguments: {'a': 1251, 'b': 789, 'operation': 'multiply'}
Tool result: 987039

Final answer: Sumit
987039
Sumit
```
**Complex Example 2:**
```
Ask me anything:print my name first, then convert my name into decimal digits as per 26 English alphabet, like A should be 1,B should be 2 etc. Next, multiple that with 123 

LLM requested tool: get_user_name
Arguments: {}
Tool result: Sumit

LLM requested tool: calculator
Arguments: {'a': 82, 'b': 123, 'operation': 'multiply'}
Tool result: 10086

Final answer: Name: Sumit  
Numeric value of name (sum of alphabet positions): 82  
82 multiplied by 123 equals: 10,086
```
Here, the Agent is now demonstrating **two different kinds of capability:**
```
Capability                  Who performs it?
------------------------------------------------
Get user's name             Python tool
Convert letters → numbers   LLM
Multiplication              Python tool
```
This is a simple example of **dependent steps.**
## Part 8 : Teach the Agent to handle tool errors safely.
What if the `tools` object contains wrong information about a function. The our Agent can crash. How can our agent handle it safely?
```
calculator
{"a": 20}
```
would fail because `b` is missing.
Example 1: where parameter information is missing
```
raise self._make_status_error_from_response(err.response) from None
groq.BadRequestError: Error code: 400 - {'error': {'message': "Tool call validation failed: tool call validation failed: attempted to call tool 'calculator<|channel|>commentary' which was not in request.tools", 'type': 'invalid_request_error', 'code': 'tool_use_failed', 'failed_generation': '{"name": "calculator<|channel|>commentary", "arguments": {"a":1251,"operation":"multiply"}}'}}
```
Example 2: divide by 0
```
Ask me anything:divide 12 by 0

Final answer: Error: division by zero is undefined.
```
But, our program defines something as below. And we are expection that error message.
```
elif operation == "divide":
        if b == 0:
            return "Cannot divide by zero"
        return a / b
```
We can achieve this via `Python programming error handling mechanism`.**
**step 1:** <br>
We need to do `raise ValueError(message)`,instead of returning a string in our program.<br>
```
elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
```
**step 2:** <br>
We need to do the tool execution call in a `try..except` block and pass the error back to the LLM.
```
        if tool is None:
            result=f"Unknown Tool:{tool_name}"
        else:
            try:
                # Automatically pass the arguments
                result=tool(**arguments)
            except Exception as e:
                result=f"Tool error:{str(e)}"
```
**step 3:** we need to change the instruction prompt in the messages.
```
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
```
### Result:
Example 1:
```
Ask me anything:divide 12 by 0

LLM requested tool: calculator
Arguments: {'a': 12, 'b': 0, 'operation': 'divide'}
Tool result: Tool error:Cannot divide by zero

Final answer: Division by zero is undefined—you cannot divide a number by zero in standard arithmetic.
```
Complex Example 2:
```
Ask me anything:print my name first, then convert my name into decimal digits as per 26 English alphabet, like A should be 1,B should be 2 etc. Next, multiple that with 123.

LLM requested tool: get_user_name
Arguments: {'{}': {}}
Tool result: Tool error:get_user_name() got an unexpected keyword argument '{}'

LLM requested tool: get_user_name
Arguments: {}
Tool result: Sumit

LLM requested tool: calculator
Arguments: {'a': 192113920, 'b': 123, 'operation': 'multiply'}
Tool result: 23630012160

Final answer: Your name: **Sumit**

Converted to digits (A=1, B=2, …, Z=26) and concatenated: **192113920**

Multiplying this number by 123:

**192,113,920 × 123 = 23,630,012,160**
```
That's actually a **very good Agent example.** <br>

It demonstrates that an Agent doesn't necessarily use a tool for every single step.<br>

It uses a tool **when the tool is capable of performing that step.** <br>
#### One more important lesson from this experiment
Your system prompt is **guidance**, not a hard security mechanism.<br>
Even if you write:
```
MUST use calculator
```
the LLM can still make mistakes.<br>
For example, it could decide to calculate:
```
1251 × 789 = ...
```
by itself.
> If you eventually need guaranteed tool usage, the `application code`—not just the prompt—must enforce that policy.

**But don't implement that yet. For your current learning stage, your prompt-based approach is exactly the right experiment.**

## Agent State
Here, `messages` is working as our Agent `state`. But, for a very complex agent, this is not enough.<br>
State enables multiple Agent components to share information within an Agent.<br>
**Think about it like a Java application**
Imagine:
```
class AgentState {
    List<Message> messages;
    int step;
    String status;
    List<ToolResult> toolResults;
    String currentTask;
}
```
You wouldn't want to pass 10 unrelated variables around your application:
```
messages
step
status
toolResults
currentTask
...
```
Instead, you group them into one meaningful object:
```
AgentState
```
Python's dictionary:
```
state = {
    "messages": messages,
    "step": 0,
    "tool_results": [],
    "status": "running"
}
```
is basically our beginner-friendly version of that idea.
**Explicit state gives us one place to manage Agent information**
Without state:
```
messages
step
tool_results
status
current_task
retry_count
...
```
These can become scattered throughout the program.<br>
With state:
```
                Agent State
                    │
       ┌────────────┼─────────────┐
       │            │             │
   messages       step       tool_results
       │                          │
    history                  executions
```
Everything related to the Agent's execution is grouped together.<br>
**It becomes especially useful for multi-step workflows**
Consider:
```
Task
 ↓
Read CSV
 ↓
Clean data
 ↓
Calculate statistics
 ↓
Generate chart
 ↓
Write report
```
At any point, the Agent may need to know:
```
What have I already done?
What is the current task?
What were the results?
Did something fail?
Should I retry?
Is the whole task complete?
```
That's **state**.













