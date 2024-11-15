import requests
import os

from common.logger import logger


def ollama_compose_prose(words):
    ollama_url = f"{os.getenv('OLLAMA_HOST')}/ollama/api/generate"
    prompt = f"Generate a easy prose with fewer than 800 characters, incorporating these words: {",".join(words)}."
    logger.debug(prompt)
    headers = {
        "Authorization": f"Bearer {os.getenv('OLLAMA_KEY')}",  # Add the token here
        "Content-Type": "application/json"
    }
    # Define the prompt or input for the model
    data = {
        "model": os.getenv("OLLAMA_MODEL"),
        "prompt": prompt,
        "format": "json",
        "stream": False
    }

    # Send the request to the Ollama server
    try:
        response = requests.post(ollama_url, headers=headers, json=data, timeout=120)
        # Check for a successful response
        if response.status_code == 200:
            response = response.json()
            logger.debug(response)
            if 'response' in response:
                prose = response['response']
                sentences = prose.split(":")
                if len(sentences) > 0:
                    sentence = sentences[0]
                    prose = sentence.strip().replace("\t", "").replace("\n", "").replace("{", "").replace("}",
                                                                                                          "").replace(
                        "\"", "").replace("\\\\", "")
                    return prose
        else:
            print("Error:", response.status_code, response.text)

    except Exception as e:
        print("An error occurred:", e)
