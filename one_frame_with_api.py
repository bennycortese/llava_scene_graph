from openai import OpenAI

def llama_pipeline(prompt: str, max_new_token: int=300):
    client_8000 = OpenAI(base_url="http://krusty.cise.ufl.edu:8000/v1/", api_key="ecoleonly")
    response_8000 = client_8000.chat.completions.create(
        model="llama2",
        messages=[
            {
                "content": prompt,
                "role": "user"
            },
            
        ],
        max_tokens=max_new_token,
    )
    return response_8000.choices[0].message.content


def llava_pipeline(image: str, prompt: str, max_new_token: int=300):
    client_8001 = OpenAI(base_url="http://krusty.cise.ufl.edu:8001/v1/", api_key="ecoleonly")
    response_8001 = client_8001.chat.completions.create(
        model="llava",
        messages=[
            
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image,
                            "detail": "high"
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        max_tokens=max_new_token,
    )
    return response_8001.choices[0].message.content

def process_image(image_path):
    prompt = """For the provided image, describe the scene you see and spare no detail:"""
    output = llava_pipeline(image = image_path, prompt = prompt, max_new_token = 600)
    print('>>>>>>>>>>>>>>>>>>>>>>>> image describtion >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print(output)
    print('<<<<<<<<<<<<<<<<<<<<< image describtion ended <<<<<<<<<<<<<<<<<<<<<<<<<<<')
    return output

def get_scene_graph(prompt):
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

    question = f"""
        For the provided textual description of an image, generate a scene graph in JSON format that includes the following:\n 1. Relationship Pairs \n2. Relationships\n 3. Actions
        \n
        Here is the textual description I want you to use as context for scene graph generation:
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
    # question = f'''
    #     For the provided textual description of an image, generate a scene graph in JSON format that includes the following:\n 1. Relationship Pairs \n2. Relationships\n 3. Actions
    #     Here are some textual descriptions and corresponding scene graph I want you to learn for generation:

    #     Prompt: In this enchanting scene, a large, robust tree with a wide trunk and sprawling branches sits at the center, its leaves forming a lush canopy in varying shades of green. Sunlight filters through the foliage, casting a soft, warm glow and creating a tapestry of light and shadow on the ground. The tree's bark is textured, rich in browns and grooves, and its roots stretch into the earth, where a gentle blanket of grass surrounds it. Clinging to a lower branch, a plump grey and white cat with a bushy tail peers down curiously, its posture tense as if poised for action.
    #     Below, a golden retriever with a lustrous coat is mid-stride, its focus directed toward a vibrant red ball that appears to be in motion, rolling across a small, grassy mound at the base of the tree. The dog's tongue lolls slightly, capturing the essence of play and joyful exertion. Surrounding the central action are more muted trees, fading into a soft-focus background that suggests a tranquil, secluded grove. The overall atmosphere of the image is one of idyllic peace and playful anticipation, evoking a sense of simple joys and the beauty of a leisurely day spent in nature.
    #     Scene Graph: {scene_graph}

    #     Prompt: In the image, a translucent jellyfish is captured against a deep blue backdrop, evoking the depths of the ocean. The jellyfish's bell, semi-spherical and gelatinous, is dotted with a constellation of white spots that stand out in stark contrast to the creature's clear flesh. From beneath the bell, a bouquet of delicate, frilly tendrils hangs and drifts. These tentacles, likely laden with stinging cells known as nematocysts, dangle in an array of fine, branched structures that suggest a soft, almost feather-like appearance.
    #     The lighting accentuates the jellyfish's ghostly translucence and the ethereal quality of its floating motion. The simplicity of the composition, with the singular focus on the jellyfish, draws attention to the animal's alien beauty and the quiet grace with which it moves. The watermark "iStock by Getty Images," indicates the source of the image, suggesting that this still was likely sourced from a stock photography collection.
    #     Scene Graph: {scene_graph_2}

    #     Prompt: {prompt}
    #     Scene Graph: 
    
    # '''

    client_8000 = OpenAI(base_url="http://krusty.cise.ufl.edu:8000/v1/", api_key="ecoleonly")
    output = client_8000.chat.completions.create(
        model="llama2",
        messages=[
            {"role": "system", "content": "You are a scene graph generator. You like taking in textual representations of an image and translating them into scene graphs."},
            {"role": "user", "content": question},
            
        ],
    )
    output = output.choices[0].message.content
    # return response_8000.choices[0].message.content
    print('>>>>>>>>>>>>>>>>>>>>>>>> scene graph >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    output = output.split('{', 1)[1]
    output = output.rsplit('}', 1)[0]
    output = '{' + output + '}'
    print(output)
    print('<<<<<<<<<<<<<<<<<<<<< scene graph ended <<<<<<<<<<<<<<<<<<<<<<<<<<<')
    return output

     

# Example usage:888
# process_image('./keyframe2.jpeg')
