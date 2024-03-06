import cv2
import os

def extract_specific_frames_from_video(video_path, base_frames_dir, video_name):
    # Create a specific directory for the video inside the activity's frames directory
    video_frames_dir = os.path.join(base_frames_dir, video_name)
    os.makedirs(video_frames_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate frame positions: first frame, 25%, 50%, and 75% through the video
    frame_positions = [0, total_frames // 4, total_frames // 2, 3 * total_frames // 4]
    extracted_frames = []

    for pos in frame_positions:
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret, frame = cap.read()
        if ret:
            frame_path = os.path.join(video_frames_dir, f'{video_name}_frame_at_{pos}_of_{total_frames}.jpg')
            cv2.imwrite(frame_path, frame)
            extracted_frames.append(frame_path)
            print(f'Saved {frame_path}')
        else:
            print(f"Failed to extract frame at position {pos} from {video_path}")
    
    cap.release()
    
    return extracted_frames

def process_videos_in_folders(folders):
    for folder in folders:
        print(f"Processing folder: {folder}")
        folder_path = os.path.join('./', folder)  # Assuming folders are in the current directory
        base_frames_dir = os.path.join('./processed_frames', folder)  # Save frames in separate subdirectories for each folder
        
        for filename in os.listdir(folder_path):
            if filename.endswith('.mp4'):
                video_path = os.path.join(folder_path, filename)
                video_name = os.path.splitext(filename)[0]
                print(f"Processing video: {filename}")
                
                # Extract specific frames into their own folder
                extracted_frames = extract_specific_frames_from_video(video_path, base_frames_dir, video_name)
                
                # Now, you can process extracted frames using process_image function
                # for frame_path in extracted_frames:
                #     process_image(frame_path)

folders = ['crawl', 'climb', 'slide', 'hiding', 'walking']
process_videos_in_folders(folders)
