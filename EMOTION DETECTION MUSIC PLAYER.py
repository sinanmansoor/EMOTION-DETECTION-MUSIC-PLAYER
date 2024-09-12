import cv2
from deepface import DeepFace
import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Function to play music based on detected emotion
def play_music(emotion):
    music_dir = f"music/{emotion}"
    
    if not os.path.exists(music_dir):
        print(f"No folder found for emotion: {emotion}")
        return
    
    songs = os.listdir(music_dir)
    if songs:
        song = random.choice(songs)
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(music_dir, song))
        pygame.mixer.music.play()

# Function to start emotion detection
def start_detection():
    global cap, root

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        
        if not ret:
            break
        
        try:
            # Detect emotion using DeepFace
            emotions = DeepFace.analyze(frame, actions=['emotion'])
            emotion = emotions[0]['dominant_emotion']
            
            # Display detected emotion in a message box
            if emotion != previous_emotion:
                previous_emotion.set(emotion)
                messagebox.showinfo("Detected Emotion", f"Emotion detected: {emotion}\nClick OK to play corresponding music.")
                
                # Play the music based on the detected emotion
                play_music(emotion)
            
            # Display the detected emotion on the GUI
            cv2.putText(frame, emotion, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            
            # Convert frame to Tkinter-compatible image format
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img = ImageTk.PhotoImage(image=img)
            panel.imgtk = img
            panel.config(image=img)
            
        except Exception as e:
            print(f"Error: {e}")
            messagebox.showerror("Error", "Face not detected or other issue.")
            break

        root.update()

    cap.release()

# Set up GUI
root = tk.Tk()
root.title("Emotion Detecting Music Player")

# Create a label to display the video feed
panel = tk.Label(root)
panel.pack()

# Variable to store the previously detected emotion
previous_emotion = tk.StringVar()
previous_emotion.set("")

# Start emotion detection automatically
start_detection()

root.mainloop()
