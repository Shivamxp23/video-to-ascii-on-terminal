import cv2
from ascii_magic import AsciiArt
import os

video_number = int(input("Enter the video folder number: "))

os.mkdir(rf"C:\Users\soni8\OneDrive\Desktop\everything\University 2.0\Project(s)\Run video on terminal\video {video_number}")
os.mkdir(rf"C:\Users\soni8\OneDrive\Desktop\everything\University 2.0\Project(s)\Run video on terminal\video {video_number}\frames")

# Use an f-string for proper substitution
os.chdir(f"C:\\Users\\soni8\\OneDrive\\Desktop\\everything\\University 2.0\\Project(s)\\Run video on terminal\\video {video_number}")

print(f"The video {video_number} folder has been created. Please place the video file in this folder and press Enter.")
input()

video_name = str(input("Enter the name of the video file (without extension): "))

vidcap = cv2.VideoCapture(f"{video_name}.mp4")
success, image = vidcap.read()
count = 0

# Use an f-string here as well
os.chdir(f"C:\\Users\\soni8\\OneDrive\\Desktop\\everything\\University 2.0\\Project(s)\\Run video on terminal\\video {video_number}\\frames")

while success:
    if image is not None:  # Check if the frame is valid
        cv2.imwrite(f"frame{count}.jpg", image)  # Save frame as JPEG file
        count += 1
    success, image = vidcap.read()  # Read the next frame

    if cv2.waitKey(10) == 27:  # Exit if Escape is hit
        break

print("All frames have been extracted successfully. Run the next script to convert them to ASCII video.")