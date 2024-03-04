from llava.model.builder import load_pretrained_model
from llava.mm_utils import get_model_name_from_path
from llava.eval.run_llava import eval_model
import cv2
import os
from contextlib import contextmanager
import sys

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
        
        image_file_name = os.path.basename(image_path)
        output_file_name = f"{os.path.splitext(image_file_name)[0]}_annotation.txt"
        output_file_path = os.path.join(annotation_dir, output_file_name)

        prompt = """For the provided image, describe the scene you see and spare no detail:"""
        
        
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
    
        with redirect_stdout_to_file(output_file_path):
            eval_model(args)


def process_images_in_folder(folder_path):

    allowed_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    
    # List all files in the directory
    for filename in os.listdir(folder_path):
        # Check if the file is an image
        if os.path.splitext(filename)[1].lower() in allowed_extensions:
            # Construct full image path
            image_path = os.path.join(folder_path, filename)
            # Process the image
            process_image(image_path)


video_path = './zibaroon2.mp4'

frames_dir = './cur_video/frames'
os.makedirs(frames_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)

frame_count = 0
while True:

    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame_path = os.path.join(frames_dir, f'frame_{frame_count:04d}.jpg')
    cv2.imwrite(frame_path, frame)
    print(f'Saved {frame_path}')
    
    frame_count += 1

cap.release()

print('Finished saving frames.')

process_images_in_folder('./cur_video/frames')

