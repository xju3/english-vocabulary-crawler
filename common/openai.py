

import openai

from common.env import Environment

env = Environment()

# Set up your API key
openai.api_key = env.config.openai_key

def gen_composition(words):
    """generate an article within these words"""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Can you help me with generating a article with these words { ','.join(words)}?"}
    ]

    # Make the API request
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use "gpt-4" if available to you and desired
        messages=messages
    )

    # Extract and print the assistant's response
    return response['choices'][0]['message']['content']