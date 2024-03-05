import openai
import json
import time
import tqdm
import numpy as np

def generate(prompt, max_token=2000, temperature=0.5, timing=False):
    with open("secrets/key.json") as file:
        openai.api_key = json.loads(file.read())["key"]
    st = time.time()
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_token,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        if timing:
            print("Elapsed time:", time.time()-st)
        return response["choices"][0]["text"]
    except Exception:
        return ""

def generate_gpt(prompt, max_token=8000, temperature=0.5, timing=False):
    with open("secrets/key.json") as file:
        openai.api_key = json.loads(file.read())["key"]
    response = openai.ChatCompletion.create(
        #model="gpt-4-0314",
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a machine that produces JSON files that are machine readable"},
                {"role": "user", "content": "write all responses in JSON format"},
                {"role": "assistant", "content": "understood, I will write all my replies in JSON format"},
                {"role": "user", "content": "I give you a promt and you should just repeat it to me without changing anything."},
                {"role": "assistant", "content": "understood"},
                {"role": "user", "content": prompt}
            ]
        )
    return response

def generate_gpt_2(prompt, max_token=8000, temperature=0.5, timing=False):
    with open("secrets/key.json") as file:
        openai.api_key = json.loads(file.read())["key"]
    response = openai.ChatCompletion.create(
        #model="gpt-4-0314",
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are a brilliant science fiction writer."},
                {"role": "user", "content": "write an outline of an exciting story, including a romance arc, aspects of detective noir like and scify. It should be about humans that are multiplanetary but only in the solar system. Be very specific and write a long text."},
                {"role": "assistant", "content": "\n\nTitle: Starcrossed Detectives\n\nSetting: In the distant future, humans have successfully colonized the entire solar system, with colonies present on all of the nine planets, including Pluto. All the colonies are connected by a network of space stations and interplanetary transport systems.\n\nPlot:\n\nDetective Serena Reyes, the head of security on the biggest space station orbiting the sun, has a new case: a high-profile theft of advanced technology from a research facility on Mars. Her investigation leads her on a dangerous journey across the solar system to track down the culprits.\n\nOn her journey, she meets Ben Henderson, a charming and handsome private investigator. Sparks fly between them, but Serena hesitates to get involved with him as she is still emotionally recovering from a failed relationship on Earth.\n\nTogether, they discover a conspiracy that runs deep in the solar system, involving a rogue group of scientists and business tycoons who aim to monopolize advanced technology for their own gain.\n\nAs they unravel the mystery, the stakes get higher, and they find themselves in life-threatening situations. Along the way, they develop a deep connection and bond that helps keep them going through the hardships.\n\nThe two investigators find themselves shuffling between the different planets, chasing leads, dodging danger, and ultimately putting the pieces together to solve the case.\n\nAs they close in on the culprits, a surprising twist is revealed: the mastermind behind the conspiracy is none other than Serena\u2019s ex-boyfriend, who had been using her to gain access to classified information.\n\nSerena and Ben manage to catch the culprits, but not before a harrowing ordeal that forces them to realize that they need each other's support, comfort, and love to overcome the trauma.\n\nIn the end, Serena and Ben return to the space station victorious, and their romance blossoms. They understand that they are \u201cstarcrossed\u201d lovers, each with their own reasons and histories that have led them to the solar system, but now they are joined on this adventure.\n\nConclusion:\n\nIn \"Starcrossed Detectives,\" the reader is taken on a thrilling ride through the sols system, complete with elements of detective noir, romance, and sci-fi. From high-speed space chases to intense battles with enemy forces, the story is full of action, adventure and intrigue. As Serena and Ben draw closer to the truth, they also grow closer to each other \u2013 and in the end, they realize that they may be Star-crossed lovers, but it is their combined strength and love that will keep them supporting each other through any adventure that comes their way in the sols system."},
                {"role": "user", "content": prompt}
            ]
        )
    return response

def embedding(text, model="text-embedding-ada-002"):
    with open("secrets/key.json") as file:
        openai.api_key = json.loads(file.read())["key"]
    text = text.replace("\n", " ")
    return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

def embedding_vec_old(data, model="text-embedding-ada-002"):
    with open("secrets/key.json") as file:
        openai.api_key = json.loads(file.read())["key"]
    embedding_result = openai.Embedding.create(input = data, model=model)
    return np.array([x["embedding"] for x in embedding_result["data"]])

def chunk_list(lst, chunk_size):
    return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]

def embedding_vec(data, model="text-embedding-ada-002", max_chunk_size=50):
    with open("secrets/key.json") as file:
        openai.api_key = json.loads(file.read())["key"]
    chunk_data = chunk_list(data, max_chunk_size)
    embeddings = []
    for chunk_data in tqdm.tqdm(chunk_data):
        embedding_result = openai.Embedding.create(input=chunk_data, model=model)
        chunk_embeddings = np.array([x["embedding"] for x in embedding_result["data"]])
        embeddings.append(chunk_embeddings)
    return np.concatenate(embeddings, axis=0)

def transcribe(file):
    audio_file= open(file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript