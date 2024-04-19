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
    

extract_specific_frames_from_video('./cur_vid.mp4', './frames', 'cur_vid')
    
