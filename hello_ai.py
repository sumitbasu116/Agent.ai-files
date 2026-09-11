import os
from dotenv import load_dotenv
from groq import Groq
# Load variables from the .env file
load_dotenv()
# Get the API key
my_api_key = os.getenv("GROQ_API_KEY")
# Check if the API key exists
if not my_api_key:
    raise ValueError("GROQ_API_KEY is missing")
# Create the Groq client
client = Groq(api_key=my_api_key)
model = "openai/gpt-oss-20b"

prompt = "What is Agentic AI? Explain it in simple English."
# Send the request to the LLM
response = client.chat.completions.create(
    model=model,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)
# Get the main answer
answer = response.choices[0].message.content
print(answer)