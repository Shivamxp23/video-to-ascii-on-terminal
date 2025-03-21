from PIL import Image
import os
import time
import pickle
from concurrent.futures import ThreadPoolExecutor
import sys
import platform
import ctypes

def rgb_to_ansi(r, g, b):
    """Converts RGB to closest ANSI color code."""
    if r == g == b:  # Grayscale
        if r < 8:
            return 16  # Black
        if r > 248:
            return 231  # White
        return 232 + (r - 8) * 24 / 240  # Grayscale range
    r_6 = int(r * 5 / 255)
    g_6 = int(g * 5 / 255)
    b_6 = int(b * 5 / 255)
    return 16 + 36 * r_6 + 6 * g_6 + b_6

def ascii_theater_convert(image_path, columns, rows, char_set):
    """Converts an image to colored ASCII art with character as background and foreground."""
    img = Image.open(image_path).resize((columns, rows))
    pixels = list(img.getdata())

    def get_char(pixel):
        """Maps pixel brightness and color to an ASCII character."""
        if isinstance(pixel, tuple):  # Color image
            r, g, b = pixel
            brightness = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
            ansi_color = rgb_to_ansi(r, g, b)
            char_index = int(brightness / 255 * (len(char_set) - 1))
            return f"\x1b[48;5;{int(ansi_color)}m\x1b[38;5;{int(ansi_color)}m{char_set[char_index]}"  # Set background and foreground
        else:  # Grayscale image
            brightness = pixel
            char_index = int(brightness / 255 * (len(char_set) - 1))
            return char_set[char_index]

    ascii_art = ''
    for i, pixel in enumerate(pixels):
        ascii_art += get_char(pixel)
        if (i + 1) % columns == 0:
            ascii_art += '\x1b[0m\n'  # Reset color and add newline
    ascii_art += '\x1b[0m'  # Reset color at the end.
    return ascii_art

def create_ascii_frames_pickle_theater(frame_path, pickle_path, columns, rows, char_set):
    """Creates a pickle file containing colored ASCII art frames."""
    ascii_frames = []
    frame_files = sorted([f for f in os.listdir(frame_path) if f.endswith(".jpg")], key=lambda x: int(x[5:-4]))

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda frame_file: ascii_theater_convert(os.path.join(frame_path, frame_file), columns, rows, char_set), frame_files))

    ascii_frames = [result for result in results if result is not None]

    with open(pickle_path, 'wb') as f:
        pickle.dump(ascii_frames, f)
    print(f"ASCII frames pickled to {pickle_path}")

def play_ascii_video_theater(pickle_path):
    """Plays the colored ASCII video from the pickle file."""
    try:
        with open(pickle_path, 'rb') as f:
            ascii_frames = pickle.load(f)

        for frame in ascii_frames:
            clear_screen()
            print(frame, end='')
            time.sleep(0.05)
    except FileNotFoundError:
        print(f"Pickle file not found: {pickle_path}")
    except Exception as e:
        print(f"Error playing video: {e}")

def get_optimal_dimensions(frame_path, target_width=200):
    """Calculates optimal columns and rows based on the first frame's aspect ratio."""
    first_frame_path = os.path.join(frame_path, sorted(os.listdir(frame_path))[0])
    img = Image.open(first_frame_path)
    width, height = img.size
    aspect_ratio = width / height
    columns = target_width
    rows = int(target_width / aspect_ratio * 0.45)  # 0.45 is a tweak to account for character aspect ratios.
    return columns, rows

def clear_screen():
    """Clears the terminal screen."""
    if platform.system() == 'Windows':
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleCursorPosition(kernel32.GetStdHandle(-11), 0)
        print("\x1b[2J", end="")
    else:
        print("\x1b[H\x1b[J", end="")

# Example Usage:
video_number = int(input("Enter the video number: "))
frame_path = rf"C:\Users\soni8\OneDrive\Desktop\everything\University 2.0\Project(s)\Run video on terminal\video {video_number}\frames"
pickle_path = rf"C:\Users\soni8\OneDrive\Desktop\everything\University 2.0\Project(s)\Run video on terminal\video {video_number}\ascii_frames_theater_color.pkl"
char_set = "██▓▒░ "  # Denser Char set.

columns, rows = get_optimal_dimensions(frame_path)

if not os.path.exists(pickle_path):
    print("Creating colored ASCII frames pickle...")
    create_ascii_frames_pickle_theater(frame_path, pickle_path, columns, rows, char_set)

print("Playing colored ASCII video...")
play_ascii_video_theater(pickle_path)

os.system('cls')