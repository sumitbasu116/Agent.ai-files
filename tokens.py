import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

model="openai/gpt-oss-20b"

role = "user"

promt1 = "Hi!"
promt2 = "Explain time travel in details but under 100 words"
promt3 = "write a 1000 words essay in machine learning"

promts = [promt1,promt2,promt3]

for promt in promts:
    message={
        "role":role,
        "content":promt
    }
    messages=[message]
    response = client.chat.completions.create(model=model,messages=messages,
                                         max_tokens=500)
    usage=response.usage
    print(f"Prompt: {promt}--> your tokens:{usage.prompt_tokens} completion_tokens:{usage.completion_tokens} total tokens: {usage.total_tokens} Finish Reason: {response.choices[0].finish_reason}")

    
