import os
import time

import modal

from modal import Image, Stub

bot_image = modal.Image.debian_slim().pip_install("openai")
bot_image = bot_image.pip_install("numpy")
bot_image = bot_image.pip_install("pandas")
bot_image = bot_image.pip_install("youtube_transcript_api")
bot_image = bot_image.pip_install("flask")
bot_image = bot_image.pip_install("flask_cors")

stub = modal.Stub("GPT wins 😔", image=bot_image)

@stub.function(secret=modal.Secret.from_name("my-openai-secret"))
def complete_text(prompt):
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a scene graph generator. You like taking in textual representations of an image and translating them into scene graphs."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content

@stub.local_entrypoint()
def main():

    scene_graph = {
    "situation": {
            "rel_pairs": [    
                ["cat", "dog"],
                ["cat", "tree"],
                ["dog", "ball"],
                ["ball", "tree"],
                ["cat", "ball"]
            ],
            "rel_labels": [
                "near", 
                "under", 
                "chasing", 
                "under",
                "looking"
            ],
            "actions": [
                "cat climbing the tree", 
                "dog chasing the ball", 
                "ball rolling under the tree"
            ]
        }
}
    
    scene_graph_2 = {
    "situation": {
        "rel_pairs": [
            ["jellyfish", "water"],
            ["jellyfish", "spots"],
            ["water", "jellyfish"]
        ],
        "rel_labels": ["floating in", "filled with", "decorated with", "surrounding"],
        "actions": ["jellyfish floating in the water", "jellyfish filled with spots"]
    }
}
    
    requests_dir = 'requests_2'
    if not os.path.exists(requests_dir):
        os.makedirs(requests_dir)

    annotations_dir = 'annotations_2'
    annotation_files = [f for f in os.listdir(annotations_dir) if f.endswith('.txt')]

    for file_name in annotation_files:
        file_path = os.path.join(annotations_dir, file_name)
        with open(file_path, 'r') as file:
            annotation_text = file.read()

        question = f"""
        For the provided textual description of an image, generate a scene graph in JSON format that includes the following:\n 1. Relationship Pairs \n2. Relationships\n 3. Actions
        \n
        Here is the textual description I want you to use as context for scene graph generation:
        \n
        {annotation_text}
        \n
        Here is an example of a scene graph, I want you to generate output in the same format as this scene graph: 
        {scene_graph}
        \n
        Here is another great example of a scene graph, again generate something similar in formatting to this:
        {scene_graph_2}
        \n
        Scene Graph:
        """ 

        # Define the path for the new request file
        request_file_path = os.path.join(requests_dir, f"request_{file_name}")
        # Write the request to a new file
        with open(request_file_path, 'w') as request_file:
            request_file.write(complete_text.remote(question))

        # Optionally, you can still print a message indicating the request has been saved
        print(f"Request saved to {request_file_path}")