# WinAssist - A voice assistant for Windows

This is a voice assistant that can perform various tasks such as searching Wikipedia, controlling media, setting the volume, and more. You can interact with the assistant using voice commands or text input.

The assistant uses the following libraries:

- `speech_recognition` for speech recognition
- `pyttsx3` for text-to-speech
- `wikipedia` for searching Wikipedia
- `pyjokes` for telling jokes
- `spotipy` for playing music on Spotify
- `pyautogui` for performing hotkey shortcuts
- `pycaw` for controlling the volume
- `psutil` for closing applications
- `cv2` for capturing images and videos from the webcam

The assistant can be controlled using the following voice commands:

- `wikipedia <search term>`: Search Wikipedia for the given search term
- `play <song name> by <artist name>`: Play the given song on Spotify
- `capture image`: Capture an image from the webcam and save it with a random name
- `record video`: Press Q
- `stop recording`: Stop recording the video
- `joke`: Tell a joke
- `time`: Get the current time
- `exit`: Exit the assistant
- `open <application name>`: Open the given application
- `browse <website>`: Open the given website in the default web browser
- `play pause`: Toggle play/pause
- `next track`: Go to the next track
- `previous track`: Go to the previous track
- `set volume to <percentage>`: Set the volume to the given percentage
- `increase volume`: Increase the volume
- `decrease volume`: Decrease the volume
- `mute`: Mute the volume
- `unmute`: Unmute the volume
- `close all windows`: Close all windows
- `window switch right`: Switch to the next window
- `window switch left`: Switch to the previous window
- `desktop switch right`: Switch to the next desktop
- `desktop switch left`: Switch to the previous desktop
- `minimise all windows`: Minimise all windows

The assistant can also be controlled using text input. Simply type a command and press enter to execute it.

The GUI has a text input field, a button to start the assistant, and a button to toggle between voice and text mode. The assistant will speak its responses in voice mode, and display them in the text input field in text mode.

The assistant also integrates with the Gemini Generative AI to generate content based on user commands. The following command is used to interact with the Gemini API:

- `<just say the question or query>`: Generates content using the Gemini Generative AI

Ensure you have configured the Gemini API with the necessary API key before using this command.


## Steps to Procure Gemini and Spotify APIs

### Gemini API
1. **Visit the Gemini AI website**: Go to the official Gemini AI website and sign up or log in to your account.
2. **Access API keys**: Navigate to the developer's section or API keys section on the website.
3. **Create a new API key**: Follow the instructions to generate a new API key for your application.
4. **Configure API key**: Once you have the API key, you can configure it in your application by setting it as an environment variable or directly in your code.

### Spotify API
1. **Visit the Spotify Developer Dashboard**: Go to https://developer.spotify.com and log in with your Spotify account.
2. **Create a new application**: Click on your profile and select "Dashboard." Then, click "Create an App" to register a new application.
3. **Get Client ID and Secret**: After creating the app, you'll be provided with a Client ID and Client Secret. These are needed for authentication.
4. **Set Redirect URI**: In your app settings, set a Redirect URI. This is necessary for the OAuth flow. It should match the URI configured in your application code.
5. **Configure API keys in your code**: Use the Client ID, Client Secret, and Redirect URI to authenticate requests in your application.

Ensure you follow each platform's documentation for any additional requirements or changes in the API procurement process.



