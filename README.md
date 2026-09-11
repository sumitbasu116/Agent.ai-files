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
