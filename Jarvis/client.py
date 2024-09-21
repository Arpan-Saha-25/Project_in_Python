# pip install openai
from openai import OpenAI

client = OpenAI(api_key="")     # Add your api key


completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful virtual assistant named \"Jarvis\"."},
        {
            "role": "user",
            "content": "What is programming?"
        }
    ]
)

print(completion.choices[0].message.content)

