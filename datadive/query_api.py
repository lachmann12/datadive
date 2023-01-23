import openai
import json
import time

def generate_text(prompt, max_token=200, temperature=0.5):
    with open("secrets/key.json") as file:
        openai.api_key = json.loads(file.read())["key"]
    st = time.time()
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_token,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=[";"]
    )
    print("Elapsed time:", time.time()-st)
    return response["choices"][0]["text"]

generate_text("write a funny joke about germans")

