import os
from contextlib import contextmanager
import sys

# Assuming llava related imports are available and correctly set up
from llava.model.builder import load_pretrained_model
from llava.mm_utils import get_model_name_from_path
from llava.eval.run_llava import eval_model

@contextmanager
def redirect_stdout_to_file(file_path):
    original_stdout = sys.stdout  # Save the original stdout
    with open(file_path, 'w') as file:
        sys.stdout = file  # Redirect stdout to the file
        yield
        sys.stdout = original_stdout  # Reset stdout back to original

def process_image(image_path):
    model_path = "liuhaotian/llava-v1.5-7b"

    base_dir = os.path.dirname(image_path)
    annotation_dir = os.path.join(base_dir, "annotations")
    os.makedirs(annotation_dir, exist_ok=True)

    # Prepare output file name and path
    image_file_name = os.path.basename(image_path)
    output_file_name = f"{os.path.splitext(image_file_name)[0]}_annotation.txt"
    output_file_path = os.path.join(annotation_dir, output_file_name)

    prompt = """For the provided image, describe the scene you see and spare no detail:"""

    # Configure arguments for the model evaluation
    args = type('Args', (), {
        "model_path": model_path,
        "model_base": None,
        "model_name": get_model_name_from_path(model_path),
        "query": prompt,
        "conv_mode": None,
        "image_file": image_path,
        "sep": ",",
        "temperature": 0,
        "top_p": None,
        "num_beams": 1,
        "max_new_tokens": 512
    })()

    # Process the image and redirect stdout to a file
    with redirect_stdout_to_file(output_file_path):
        eval_model(args)


# Example usage:
# process_image('/path/to/your/image.jpg')
