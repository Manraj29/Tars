import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import threading
import os
import webbrowser

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyCWFqIFVj1MpHJ1B9d8UzaMm_hBvHVnZn8"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Initialize Speech Recognizer
recognizer = sr.Recognizer()
stop_speaking = threading.Event()

# Function to convert text to speech (with interrupt support)
def speak(text):
    stop_speaking.clear()
    for sentence in text.split(". "):
        if stop_speaking.is_set():
            break
        engine.say(sentence)
        engine.runAndWait()

# Function to open apps
def open_application(app_name):
    app_paths = {
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "spotify": "C:\\Users\\YourUsername\\AppData\\Roaming\\Spotify\\Spotify.exe",
    }
    if app_name in app_paths:
        os.startfile(app_paths[app_name])
        speak(f"Opening {app_name}")
    else:
        speak(f"Sorry, I couldn't find {app_name} on your system.")

# Function to search the web
def search_google(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    speak(f"Searching Google for {query}")

# Function to process user queries using Gemini API
def get_gemini_response(query):
    prompt = f"You are an AI assistant. Answer concisely in 3 lines max. The question is: {query}"
    model = genai.GenerativeModel("gemini-2.0-flash-001")
    response = model.generate_content(prompt)
    return response.text if response else "I couldn't understand that."

# Function to listen for the wake word
def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source, timeout=10)
                text = recognizer.recognize_google(audio).lower()
                if "hey tars" in text:
                    print("Wake word detected! Listening for command...")
                    stop_speaking.set()
                    speak("Yes, how can I help you?")
                    process_command()
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                print("Could not request results. Check internet connection.")

# Function to process user commands
def process_command():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            print("Listening for command...")
            audio = recognizer.listen(source, timeout=10)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")

            # Open apps
            if "open" in command:
                app_name = command.replace("open", "").strip()
                open_application(app_name)

            # Search Google
            elif "search for" in command:
                search_query = command.replace("search for", "").strip()
                search_google(search_query)

            # Get AI response for general questions
            else:
                ai_response = get_gemini_response(command)
                print(f"AI: {ai_response}")
                speak(ai_response)

        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            speak("Sorry, I didn't catch that, please repeat.")
        except sr.RequestError:
            print("Could not request results. Check internet connection.")

    # Return to wake word listening
    listen_for_wake_word()

# Run the assistant
listen_for_wake_word()
