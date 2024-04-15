import os
from openai import OpenAI

# Set up OpenAI client with your API key
os.environ['OPENAI_API_KEY'] = ''

client = OpenAI()


def complete_text(prompt):
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[
            {"role": "system", "content": "Generate a scene graph from simple descriptive pairs."},
            {"role": "user", "content": prompt + """ Again, as a json in the format of a parent node situation with rel_pairs, rel_labels, and actions as the children node of situation. Here's an example to descibe the relationship:
                "situation": {
                "rel_pairs": [    
                    ["entity1", "entity2"],
                    ["", ""],
                    ["", ""],
                    ["", ""],
                    ["", ""]
                ],
                "rel_labels": [
                    "relation between entity 1 and 2", 
                    "", 
                    "", 
                    "",
                    ""
                ],
                "actions": [
                    "An overall action in the scene",
                    "",
                    ""
                ]
            }""" }
        ],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

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
    
    annotations_dir = 'horse_classes'
    if not os.path.exists(annotations_dir):
        print("Annotations directory does not exist.")
        return

    request_dir = 'requests_2'
    if not os.path.exists(request_dir):
        os.makedirs(request_dir)

    for file_name in os.listdir(annotations_dir):
        file_path = os.path.join(annotations_dir, file_name)
        with open(file_path, 'r') as file:
            pairs = file.readlines()

        prompt = ""
        for pair in pairs:
            prompt += "- " + pair.strip() + "\n"
            
        question = f"""
        For the provided relation pairs of an image, create a scene graph in JSON format that includes the following:\n 1. Relationship Pairs \n2. Relationships\n 3. Actions, using just these pairings. You can use the same relationship pairs and leave the others blank. Be sure to format it like the examples.
        \n
        {prompt}
        \n
        Here is an example of a scene graph, I want you to generate output in the same format as this scene graph: 
        {scene_graph}
        \n
        Here is another great example of a scene graph, again generate something similar in formatting to this:
        {scene_graph_2}
        \n
        Scene Graph:
        """ 

        # Scene graph generation
        scene_graph = complete_text(prompt)

        # Write the scene graph to a new file in the request directory
        request_file_path = os.path.join(request_dir, f"request_{file_name}")
        with open(request_file_path, 'w') as request_file:
            request_file.write(scene_graph)
        
        print(f"Request saved to {request_file_path}")

if __name__ == "__main__":
    main()
