from PIL import Image
import os
import time
import pickle
from concurrent.futures import ThreadPoolExecutor

def ascii_theater_convert(image_path, columns, rows, char_set):
    """Converts an image to ASCII art in the 'ascii.theater' style."""
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img = img.resize((columns, rows))
    pixels = list(img.getdata())

    def get_char(pixel_value):
        """Maps pixel brightness to an ASCII character."""
        index = int(pixel_value / 255 * (len(char_set) - 1))
        return char_set[index]

    ascii_art = ''
    for i, pixel in enumerate(pixels):
        ascii_art += get_char(pixel)
        if (i + 1) % columns == 0:
            ascii_art += '\n'
    return ascii_art

def create_ascii_frames_pickle_theater(frame_path, pickle_path, columns, rows, char_set):
    """Creates a pickle file containing ASCII art frames in the 'ascii.theater' style."""
    ascii_frames = []
    frame_files = sorted([f for f in os.listdir(frame_path) if f.endswith(".jpg")], key=lambda x: int(x[5:-4]))

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda frame_file: ascii_theater_convert(os.path.join(frame_path, frame_file), columns, rows, char_set), frame_files))

    ascii_frames = [result for result in results if result is not None]

    with open(pickle_path, 'wb') as f:
        pickle.dump(ascii_frames, f)
    print(f"ASCII frames pickled to {pickle_path}")

def play_ascii_video_theater(pickle_path):
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

# Example Usage:
video_number = int(input("Enter the video number: "))
frame_path = rf"C:\Users\soni8\OneDrive\Desktop\everything\University 2.0\Project(s)\Run video on terminal\video {video_number}\frames"
pickle_path = rf"C:\Users\soni8\OneDrive\Desktop\everything\University 2.0\Project(s)\Run video on terminal\video {video_number}\ascii_frames_theater.pkl"
char_set = " .:-=+*#%@"  # Smaller, more granular character set
columns = 200 # increase columns for more detail
rows = 50 # decrease rows for a wider image

if not os.path.exists(pickle_path):
    print("Creating ASCII frames pickle...")
    create_ascii_frames_pickle_theater(frame_path, pickle_path, columns, rows, char_set)

print("Playing ASCII video...")
play_ascii_video_theater(pickle_path)

os.system('cls')