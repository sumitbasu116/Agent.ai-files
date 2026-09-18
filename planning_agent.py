import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

user_question = input("What do you want me to do? ")

planner_prompt = f"""
You are a planning assistant.

Create a simple step-by-step plan for the user's request.

Rules:
1. Break the request into logical steps.
2. Do not execute the steps.
3. Each step should describe one action.
4. Keep the plan simple and ordered.
5. Return ONLY a JSON array.

User request:
{user_question}
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": planner_prompt
        }
    ],
    temperature=0
)

plan_text = response.choices[0].message.content

print("\n===== GENERATED PLAN =====")
print(plan_text)