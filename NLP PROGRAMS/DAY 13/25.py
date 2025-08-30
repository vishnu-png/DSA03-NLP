# pip install openai
# You need an OpenAI API key set as environment variable: export OPENAI_API_KEY="your_key"

from openai import OpenAI
client = OpenAI()

prompt = "Write a short bedtime story about a robot and a cat."

response = client.completions.create(
    model="text-davinci-003",  # GPT-3
    prompt=prompt,
    max_tokens=100
)

print(response.choices[0].text.strip())
