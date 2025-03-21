from ascii_magic import AsciiArt
import pickle
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor

def convert_frame_to_ascii(frame_path, frame_num):
    """Converts a single frame to ASCII art."""
    try:
        my_art = AsciiArt.from_image(os.path.join(frame_path, f"frame{frame_num}.jpg"))
        return my_art.to_ascii(columns=120)  # Adjust columns as needed
    except Exception as e:
        print(f"Error processing frame {frame_num}: {e}")
        return None

def create_ascii_frames_pickle(frame_path, pickle_path):
    """Creates a pickle file containing ASCII art frames."""
    ascii_frames = []
    frame_files = sorted([f for f in os.listdir(frame_path) if f.endswith(".jpg")], key=lambda x: int(x[5:-4])) #sort by frame number

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda frame_file: convert_frame_to_ascii(frame_path, int(frame_file[5:-4])), frame_files))

    ascii_frames = [result for result in results if result is not None]

    with open(pickle_path, 'wb') as f:
        pickle.dump(ascii_frames, f)
    print(f"ASCII frames pickled to {pickle_path}")

def play_ascii_video(pickle_path):
    """Plays the ASCII video from the pickle file."""
    try:
        with open(pickle_path, 'rb') as f:
            ascii_frames = pickle.load(f)

        for frame in ascii_frames:
            os.system('cls')
            print(frame)
            time.sleep(0.05)  # Adjust delay as needed
    except FileNotFoundError:
        print(f"Pickle file not found: {pickle_path}")
    except Exception as e:
        print(f"Error playing video: {e}")

# Clear the terminal
os.system('cls')

# Change this number depending on the video you want to play
video_number = int(input("Enter the video number: "))

# Path to the folder containing the frames for respective video
frame_path = rf"C:\Users\soni8\OneDrive\Desktop\everything\University 2.0\Project(s)\Run video on terminal\video {video_number}\frames"

# Path to store the pickled ASCII frames
pickle_path = rf"C:\Users\soni8\OneDrive\Desktop\everything\University 2.0\Project(s)\Run video on terminal\video {video_number}\ascii_frames.pkl"

if not os.path.exists(pickle_path):
    print("Creating ASCII frames pickle...")
    create_ascii_frames_pickle(frame_path, pickle_path)

print("Playing ASCII video...")
play_ascii_video(pickle_path)

os.system('cls')