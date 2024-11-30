import time

import requests
import os

from common.logger import logger


def ollama_compose_prose(words, repeat=5):
    ollama_url = f"{os.getenv('LLM_HOST')}/api/generate"
    prompt = f"Generate a easy prose with fewer than 800 characters, incorporating these words: { ','.join(words)}."
    logger.debug(prompt)
    headers = {
        # "Authorization": f"Bearer {os.getenv('OLLAMA_KEY')}",  # Add the token here
        "Content-Type": "application/json"
    }
    # Define the prompt or input for the model
    data = {
        "model": os.getenv("LLM_MODEL"), 
        "prompt": prompt,
        "format": "json",
        "stream": False
    }

    # Send the request to the Ollama server
    try:
        response = requests.post(ollama_url, headers=headers, json=data, timeout=1200, stream=False)
        # Check for a successful response
        if response.status_code == 200:
            data = response.json()
            if 'response' in data:
                article = data['response']
                article = article.replace("{", "").replace("}", "").replace(":", "").replace("\n", "")
                if len(article) < 100 and repeat > 0:
                    print(f'article: {len(article)}')
                    time.sleep(10)
                    repeat -= 1
                    ollama_compose_prose(words, repeat)
                return article
        else:
            print("Error:", response.status_code, response.text)
            return -1
    except Exception as e:
        print("An error occurred:", e)
        return -1

if __name__ == '__main__':
    w = ['improvise','ad-lib','extemporize','play by','spot','freestyle']
    prose = ollama_compose_prose(w)
    print(prose)
