from ascii_magic import AsciiArt
import pickle
import os
import time

# Clear the terminal
os.system('cls')

# Change this number depending on the video you want to play
video_number = int(input("Enter the video number: "))

# Path to the folder containing the frames for respective video
frame_path = rf"C:\Users\soni8\OneDrive\Desktop\everything\University 2.0\Project(s)\Run video on terminal\video {video_number}\frames"

# Path to store the pickled ASCII frames
pickle_path = rf"C:\Users\soni8\OneDrive\Desktop\everything\University 2.0\Project(s)\Run video on terminal\video {video_number}\ascii_frames.pkl"

os.chdir(frame_path)

# Display the frames in sequence
for frame_num in range(0,len(os.listdir(frame_path))):
    os.system('cls')  # Clear the screen
    my_art = AsciiArt.from_image(f"frame{frame_num}.jpg")
    my_art.to_terminal()
    time.sleep(0.05)  # Adjust the delay for smoother playback
os.system('cls')