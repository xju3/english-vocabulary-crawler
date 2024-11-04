import requests

from common.logger import logger


def ollama_compose_prose(words):
    ollama_url = "http://localhost:3000/ollama/api/generate"
    prompt = f"Generate a prose with fewer than 800 characters, incorporating the words: {",".join(words)}."
    logger.debug(prompt)

    OLLAMA_API_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImM4MWRlNDM3LTcwYWMtNGQ5YS1iOTMxLTIwOWRjYjYzODY5OSJ9.tRCG3Nq5mnV00S55uXaOffLeAFqZ_I3KhS7suyav3m0'
    headers = {
        "Authorization": f"Bearer {OLLAMA_API_TOKEN}",  # Add the token here
        "Content-Type": "application/json"
    }
    # Define the prompt or input for the model
    data = {
        "model": "llama3.2:latest",
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
