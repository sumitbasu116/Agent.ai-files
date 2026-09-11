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
### Why do we need to add it?
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




