import threading
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pyjokes
import os
import subprocess
from tkinter import *
import keyboard
import requests
import time
import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import psutil
import cv2
import random
import string
import pycaw.pycaw as pycaw
import pyautogui

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

# Function to change voice
def set_voice(voice_id):
    engine.setProperty('voice', voices[voice_id].id)

# Initialize voice to female by default
set_voice(1)

# API credentials (manually input your credentials)
GEMINI_API_KEY = "gemini_api_key"  # Replace with your actual API key

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to update the history box
def update_history_box(user_input, assistant_response):
    history_box.insert(END, f"You: {user_input}\nAssistant: {assistant_response}\n")
    history_box.see(END)

# Greet user
def wishMe():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Hello, Good Morning")
    elif hour < 18:
        speak("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")

# Get audio input
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print('You: ' + text)
            return text.lower()
        except sr.UnknownValueError:
            return "none"

# Call Gemini API
def call_apis(command):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(command)
        gemini_response = response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        gemini_response = None

    return gemini_response

# Open applications
def open_application(app_name):
    directories = [
        r"C:\ProgramData\Microsoft\Windows\Start Menu",
        r"C:\Users\ralph\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"
    ]

    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if app_name.lower() in file.lower() and file.endswith(".lnk"):
                    app_path = os.path.join(root, file)
                    try:
                        subprocess.Popen(app_path, shell=True)
                        speak(f"Opening {app_name}")
                        return
                    except Exception as e:
                        speak(f"Could not open {app_name}: {e}")
                        return

    speak(f"Could not find an application named {app_name} in the Start Menu directories.")

# Play Spotify songs
SPOTIFY_CLIENT_ID = 'spotify_client_id'  # Replace with your Client ID
SPOTIFY_CLIENT_SECRET = 'spotify_client_secret'  # Replace with your Client Secret
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'  # Replace with your Redirect URI

def get_spotify_oauth_object():
    return SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                        client_secret=SPOTIFY_CLIENT_SECRET,
                        redirect_uri=SPOTIFY_REDIRECT_URI,
                        scope='user-read-playback-state,user-modify-playback-state')

def get_spotify_access_token():
    sp_oauth = get_spotify_oauth_object()
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print(f"Please navigate here: {auth_url}")
        response = input("Enter the URL you were redirected to: ")
        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code, as_dict=False)
    return token_info['access_token']

def get_spotify_track_link(song_name, artist_name, access_token):
    sp = spotipy.Spotify(auth=access_token)
    query = f"track:{song_name} artist:{ artist_name}"
    results = sp.search(q=query, limit=1)
    tracks = results['tracks']['items']
    if len(tracks) > 0:
        track_id = tracks[0]['id']
        spotify_link = f"spotify:track:{track_id}"
        return spotify_link
    else:
        return None

# Function to adjust system volume
def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level, None)  # level is between 0.0 and 1.0

def change_volume(command):
    if 'set volume to' in command:
        try:
            percentage = int(command.split('set volume to')[1].strip().replace('percent', '').replace('%', ''))
            if 0 <= percentage <= 100:
                set_volume(percentage / 100.0)  # Convert percentage to a value between 0.0 and 1.0
                speak(f"Volume set to {percentage} percent.")
                return f"Volume set to {percentage} percent."
            else:
                speak("Please provide a volume percentage between 0 and 100.")
                return "Please provide a volume percentage between 0 and 100."
        except ValueError:
            speak("I couldn't understand the percentage. Please try again.")
            return "I couldn't understand the percentage. Please try again."
    elif 'increase volume' in command:
        set_volume(1.0)  # Max volume
        speak("Volume set to maximum.")
        return "Volume set to maximum."
    elif 'decrease volume' in command:
        set_volume(0.5)  # Medium volume
        speak("Volume set to medium.")
        return "Volume set to medium."
    elif 'mute' in command:
        set_volume(0.0)  # Mute
        speak("Volume muted.")
        return "Volume muted."
    elif 'unmute' in command:
        set_volume(0.5)  # Unmute to medium
        speak("Volume unmuted.")
        return "Volume unmuted."

# Function to control media
def control_media(command):
    devices = pycaw.PyCAW().audio_controllers()
    for device in devices:
        if device.state == pycaw.AudioDeviceState.active:
            player = device.audio_session
            if player:
                volume_control = player.SimpleAudioVolume
                if command == "play/pause":
                    volume_control.Volume = volume_control.Volume
                elif command == "next_track":
                    player.VolumeControl.Volume = 0
                    player.VolumeControl.Volume = 1
                elif command == "previous_track":
                    player.VolumeControl.Volume = 0
                    player.VolumeControl.Volume = 1
                break

# Function to close applications
def close_application(app_name):
    for proc in psutil.process_iter(['name']):
        if app_name.lower() in proc.info['name'].lower():
            proc.terminate()
            speak(f"Closed {app_name}")
            return
    speak(f"Could not find an application named {app_name}.")

# Function to create a new desktop (Windows 10 and above)
def create_new_desktop():
    subprocess.run('powershell.exe New-Desktop', shell=True)
    speak("New desktop created.")

# Function to delete the current desktop
def delete_current_desktop():
    subprocess.run('powershell.exe Remove-Desktop', shell=True)
    speak("Current desktop deleted.")

# Function to generate a random name
def generate_random_name(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Function to capture an image from the webcam and save it with a random name
def capture_image_with_random_name():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        speak("Error opening video capture device")
        return "Error opening video capture device"

    # Read a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        speak("Error capturing frame")
        return "Error capturing frame"

    # Generate a random name for the image
    random_name = generate_random_name()

    # Save the captured frame with the random name
    cv2.imwrite(f'{random_name}.jpg', frame)

    # Display the captured frame
    cv2.imshow('frame', frame)

    # Wait for 2 seconds
    cv2.waitKey(2000)

    # Release the capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

    speak(f"Image captured and saved as {random_name}.jpg")
    return f"Image captured and saved as {random_name}.jpg"

# Function to record a video from the webcam and save it with a random name
def record_video_with_random_name():
    global cap, out, recording
    recording = True

    # Initialize the video capture object
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        speak("Error opening video capture device")
        return "Error opening video capture device"

    # Generate a random name for the video file
    random_name = generate_random_name()

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(f'{random_name}.avi', fourcc, 20.0, (640, 480))

    speak("Recording video. Press Q to stop.")
    while recording:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If frame is read correctly, write the frame into the output file
        if ret:
            out.write(frame)

            # Display the resulting frame
            cv2.imshow('frame', frame)

            # Press Q on keyboard to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                stop_recording()
                break

    return f"Video recorded and saved as {random_name}.avi"

# Function to stop recording
def stop_recording():
    global cap, out, recording
    recording = False

    # Release the capture and write objects
    cap.release()
    out.release()

    # Close all windows
    cv2.destroyAllWindows()

    speak("Recording stopped and video saved.")
    return "Recording stopped and video saved."

# Function to perform hotkey shortcuts
def perform_hotkey(command):
    if 'close all windows' in command:
        pyautogui.hotkey('alt', 'f4')
        speak("All windows closed.")
        return "All windows closed."
    elif 'window switch right' in command:
        pyautogui.hotkey('alt', 'tab')
        speak("Switched to the next window.")
        return "Switched to the next window."
    elif 'window switch left' in command:
        pyautogui.hotkey('alt', 'shift', 'tab')
        speak("Switched to the previous window.")
        return "Switched to the previous window."
    elif 'desktop switch right' in command:
        pyautogui.hotkey('ctrl', 'win', 'right')
        speak("Switched to the next desktop.")
        return "Switched to the next desktop."
    elif 'desktop switch left' in command:
        pyautogui.hotkey('ctrl', 'win', 'left')
        speak("Switched to the previous desktop.")
        return "Switched to the previous desktop."
    elif 'minimise all windows' in command:
        pyautogui.hotkey('win', 'm')
        speak("All windows minimized.")
        return "All windows minimized."
    elif 'play pause' in command:
        pyautogui.hotkey('playpause')
        speak("Play/Pause toggled.")
        return "Play/Pause toggled."
    elif 'next track' in command:
        pyautogui.hotkey('nexttrack')
        speak("Next track.")
        return "Next track."
    elif 'previous track' in command:
        pyautogui.hotkey('prevtrack')
        speak("Previous track.")
        return "Previous track."
    else:
        speak("Command not recognized.")
        return "Command not recognized."

# Process commands
def process_audio(command):
    if 'wikipedia' in command:
        speak("Searching Wikipedia...")
        command = command.replace("wikipedia", "")
        result = wikipedia.summary(command, sentences=2)
        speak(result)
        return result
    elif 'capture image' in command:
        return capture_image_with_random_name()
    elif 'record video' in command:
        return record_video_with_random_name()
    elif 'stop recording' in command:
        return stop_recording()
    elif 'joke' in command:
        joke = pyjokes.get_joke()
        speak(joke)
        return joke
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {current_time}")
        return f"The time is {current_time}"
    elif 'play' in command and 'by' in command:
        song = command.replace("play", "").replace("by", "").strip()
        details = song.split(" ")
        song_name = " ".join(details[:-1])
        artist_name = details[-1]
    
        access_token = get_spotify_access_token()
        spotify_link = get_spotify_track_link(song_name, artist_name, access_token)
    
        if spotify_link:
            webbrowser.open(spotify_link)
            speak(f"Playing {song_name} on Spotify")
            return f"Playing {song_name} on Spotify"
        else:
            speak(f"Could not find {song_name} on Spotify")
            return f"Could not find { song_name} on Spotify"
    elif 'exit' in command:
        speak("Goodbye!")
        exit()
    elif 'open' in command:
        app_name = command.replace("open", "").strip()
        open_application(app_name)
        return f"Opening {app_name}"
    elif 'browse' in command:
        website = command.replace("browse", "").strip()
        if not website.startswith("http://") and not website.startswith("https://"):
            website = f"http://{website}"
        webbrowser.open(website)
        return f"Opening website {website}"
    elif 'play pause' in command or 'next track' in command or 'previous track' in command:
        return perform_hotkey(command)
    elif 'set volume to' in command or 'increase volume' in command or 'decrease volume' in command or 'mute' in command or 'unmute' in command:
        return change_volume(command)
    elif 'close all windows' in command or 'window switch right' in command or 'window switch left' in command or 'desktop switch right' in command or 'desktop switch left' in command or 'minimise all windows' in command:
        return perform_hotkey(command)
    else:
        speak("Command not recognized.")
        return "Command not recognized."

# GUI and main loop
def start_assistant():
    wishMe()
    while True:
        command = get_audio()
        if command != "none":
            response = process_audio(command)
            update_history_box(command, response)

def on_submit():
    user_input = text_input.get()
    if user_input:
        response = process_audio(user_input.lower())
        update_history_box(user_input, response)
        text_input.delete(0, END)

def toggle_voice_mode():
    global voice_mode
    voice_mode = not voice_mode
    if voice_mode:
        speak("Voice mode activated. You can now speak to me.")
    else:
        speak("Text mode activated. You can type your commands.")

# GUI Setup
screen = Tk()
screen.title("Voice Assistant")
screen.geometry("600x600")

history_box = Text(screen, height=20, width=70)
history_box.pack(pady=10)

text_input = Entry(screen, width=50)
text_input.pack(pady=10)
text_input.bind("<Return>", lambda event: on_submit())

start_button = Button(screen, text="Start Voice Assistant", command=start_assistant, width=20, height=2)
start_button.pack(pady=20)

toggle_button = Button(screen, text="Toggle Voice/Text Mode", command=toggle_voice_mode, width=20, height=2)
toggle_button.pack(pady=20)

voice_label = Label(screen, text="Select Voice:")
voice_label.pack(pady=5)

voice_var = IntVar(value=1)
voice_menu = OptionMenu(screen, voice_var, *range(len(voices)), command=set_voice)
voice_menu.pack(pady=5)

keyboard.add_hotkey("F4", start_assistant)

screen.mainloop()