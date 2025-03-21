import cv2
import os
import time
import pickle
from concurrent.futures import ThreadPoolExecutor
import sys
import platform
import ctypes
from tqdm import tqdm
import msvcrt

def rgb_to_ansi(r, g, b):
    """Converts RGB to closest ANSI color code."""
    if r == g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return 232 + (r - 8) * 24 / 240
    r_6 = int(r * 5 / 255)
    g_6 = int(g * 5 / 255)
    b_6 = int(b * 5 / 255)
    return 16 + 36 * r_6 + 6 * g_6 + b_6

ansi_colors = {}

def ascii_theater_convert(image_path, columns, rows, char_set):
    """Converts an image to colored ASCII art with character as background and foreground."""
    img = cv2.imread(image_path)
    img = cv2.resize(img, (columns, rows), interpolation=cv2.INTER_FAST_LINEAR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pixels = img.reshape(-1, 3).tolist()

    def get_char(pixel):
        """Maps pixel brightness and color to an ASCII character."""
        r, g, b = pixel
        if (r,g,b) not in ansi_colors:
            ansi_colors[(r, g, b)] = rgb_to_ansi(r, g, b)

        ansi_color = ansi_colors[(r, g, b)]
        brightness = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
        char_index = int(brightness / 255 * (len(char_set) - 1))
        return f"\x1b[48;5;{int(ansi_color)}m\x1b[38;5;{int(ansi_color)}m{char_set[char_index]}"

    ascii_art = ''
    for pixel in pixels:
        ascii_art += get_char(pixel)
    for i in range(rows):
        ascii_art += '\x1b[0m\n'
    ascii_art += '\x1b[0m'
    return ascii_art

def create_ascii_frames_pickle_theater(frame_path, pickle_path, columns, rows, char_set):
    """Creates a pickle file containing colored ASCII art frames with progress bar."""
    ascii_frames = []
    frame_files = sorted([f for f in os.listdir(frame_path) if f.endswith(".jpg")], key=lambda x: int(x[5:-4]))
    total_frames = len(frame_files)

    with tqdm(total=total_frames, desc="Processing frames") as pbar:
        with ThreadPoolExecutor() as executor:
            results = []
            for frame_file in frame_files:
                results.append(executor.submit(ascii_theater_convert, os.path.join(frame_path, frame_file), columns, rows, char_set))
            for future in results:
                ascii_frames.append(future.result())
                pbar.update(1)

    with open(pickle_path, 'wb') as f:
        pickle.dump(ascii_frames, f)
    print(f"ASCII frames pickled to {pickle_path}")

def play_ascii_video_theater(pickle_path):
    """Plays the colored ASCII video from the pickle file."""
    try:
        with open(pickle_path, 'rb') as f:
            ascii_frames = pickle.load(f)

        frame_rate = 20
        frame_delay = 1 / frame_rate
        last_frame_time = time.perf_counter()

        for frame in ascii_frames:
            current_time = time.perf_counter()
            elapsed_time = current_time - last_frame_time

            if elapsed_time >= frame_delay:
                clear_screen()
                print(frame, end='')
                last_frame_time = current_time
            else:
                time.sleep(frame_delay - elapsed_time)

    except FileNotFoundError:
        print(f"Pickle file not found: {pickle_path}")
    except Exception as e:
        print(f"Error playing video: {e}")

def get_optimal_dimensions(frame_path, target_width=200):
    """Calculates optimal columns and rows based on the first frame's aspect ratio."""
    first_frame_path = os.path.join(frame_path, sorted(os.listdir(frame_path))[0])
    img = cv2.imread(first_frame_path)
    height, width, _ = img.shape
    aspect_ratio = width / height
    columns = target_width
    rows = int(target_width / aspect_ratio * 0.45)
    return columns, rows

def clear_screen():
    """Clears the terminal screen."""
    if platform.system() == 'Windows':
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleCursorPosition(kernel32.GetStdHandle(-11), 0)
        print("\x1b[2J", end="")
    else:
        print("\x1b[H\x1b[J", end="")

video_number = int(input("Enter the video number: "))
frame_path = rf"C:\Users\soni8\OneDrive\Desktop\everything\University 2.0\Project(s)\Run video on terminal\video {video_number}\frames"
pickle_path = rf"C:\Users\soni8\OneDrive\Desktop\everything\University 2.0\Project(s)\Run video on terminal\video {video_number}\ascii_frames_theater_color.pkl"
char_set = "██▓▒░ "

columns, rows = get_optimal_dimensions(frame_path)

if not os.path.exists(pickle_path):
    print("Creating colored ASCII frames pickle...")
    create_ascii_frames_pickle_theater(frame_path, pickle_path, columns, rows, char_set)

print("Press SPACE to play the video...")

while True:
    if platform.system() == 'Windows':
        if msvcrt.kbhit():
            if msvcrt.getch() == b' ':
                break
    else:
        import select
        i, o, e = select.select([sys.stdin], [], [], 0.001)
        if i:
            if sys.stdin.read(1) == ' ':
                break

print("Playing colored ASCII video...")
play_ascii_video_theater(pickle_path)

os.system('cls')