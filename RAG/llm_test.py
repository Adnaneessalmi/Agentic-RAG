import requests

OLLAMA_HOST = ""

input_text = "What is the capital of Morocco?"

headers = {'Content-Type': 'application/json', 'Connection': 'close'}

response = requests.post(
    f"{OLLAMA_HOST}/v1/completions",
    json={"model": "gemma2:2b", "prompt": input_text},
    headers=headers,
    verify=False 
)

if response.status_code == 200:
    completion_text = response.json()['choices'][0]['text']
    print(completion_text)
else:
    print(f"Error: {response.status_code}, {response.text}")
