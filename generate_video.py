import cv2
import numpy as np

def generate_sample_video(output_path="sample.mp4", duration_sec=300, fps=2, width=1280, height=720):
    """
    Generates a lightweight 5-minute video with 'Made by Python' text.
    Using low FPS (2 fps) keeps the file size small (~2-4 MB) and fast to upload.
    """
    print(f"Generating {duration_sec}s ({duration_sec // 60} min) video at {output_path}...")
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    total_frames = duration_sec * fps
    
    # Pre-render a base frame
    base_frame = np.zeros((height, width, 3), dtype=np.uint8)
    # Dark modern gradient or background (RGB: 18, 18, 24)
    base_frame[:] = (24, 18, 18)
    
    # Static text elements
    title_text = "Made by Python"
    sub_text = "YouTube Automation Dynamic Views Project"
    
    font = cv2.FONT_HERSHEY_DUPLEX
    
    for i in range(total_frames):
        frame = base_frame.copy()
        
        # Draw decorative banner
        cv2.rectangle(frame, (100, 150), (width - 100, 570), (45, 30, 30), -1)
        cv2.rectangle(frame, (100, 150), (width - 100, 570), (0, 180, 255), 3)
        
        # Draw "Made by Python"
        cv2.putText(frame, title_text, (width // 2 - 300, 290), font, 2.2, (255, 255, 255), 4, cv2.LINE_AA)
        
        # Draw subtitle
        cv2.putText(frame, sub_text, (width // 2 - 400, 370), font, 1.1, (200, 200, 200), 2, cv2.LINE_AA)
        
        # Draw elapsed timer
        current_sec = i // fps
        mins = current_sec // 60
        secs = current_sec % 60
        timer_str = f"Duration: {mins:02d}:{secs:02d} / 05:00"
        cv2.putText(frame, timer_str, (width // 2 - 190, 470), font, 1.0, (0, 220, 120), 2, cv2.LINE_AA)
        
        out.write(frame)
        
        if i % (fps * 30) == 0:
            print(f"Progress: {current_sec}/{duration_sec}s ({(i / total_frames) * 100:.1f}%)")
            
    out.release()
    print(f"Video saved successfully: {output_path}")

if __name__ == "__main__":
    generate_sample_video()
