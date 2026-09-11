# Agent.ai-files
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

  
