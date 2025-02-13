from asyncio import Server
import time
import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
import os
import threading
import subprocess
import webbrowser
from streamlit_js_eval import streamlit_js_eval


# Configure Gemini API
GEMINI_API_KEY = "your_api_key"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Speech Recognizer
recognizer = sr.Recognizer()
stop_speaking = threading.Event()
wake_word_detected = False

def speak(text):
    stop_speaking.clear()
    subprocess.run(["say", text] if os.name == "posix" else 
                   ["powershell", "Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak('{}')".format(text)], shell=True)

def get_gemini_response(query):
    prompt = f"You are an AI assistant. Answer concisely in 3 lines max. The question is: {query}"
    model = genai.GenerativeModel("gemini-2.0-flash-001")
    response = model.generate_content(prompt)
    return response.text if response else "I couldn't understand that."

def open_application(app_name):
    app_paths = {
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
    }
    if app_name in app_paths:
        os.startfile(app_paths[app_name])
        return f"Opening {app_name}"
    return "Application not found."

# Function to search the web
def search_google(query):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    speak(f"Searching Google for {query}")


# Function to process spoken commands after wake word detection
def process_command():
    global wake_word_detected
    wake_word_detected = False  # Reset after activation
    st.write("🔊 Listening...")
    speak("I'm listening.")
    st.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdDl4YWxzYWc1Y2c0azBvcjF1cG0yZjdlbXdnb3hoa3EwYTdzejFlcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/pViWHLiQBA1q0/giphy.gif", use_container_width =True)
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            command = recognizer.recognize_google(audio).lower()
            st.write(f"🎙️ You said: {command}")

            if "open" in command:
                app_name = command.replace("open", "").strip()
                response = open_application(app_name)
        # Search Google
            elif "search for" in command:
                search_query = command.replace("search for", "").strip()
                search_google(search_query)
            else:
                response = get_gemini_response(command)
            st.write("🤖 Tars: ", response)
            speak(response)
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand. Try again.")
            speak("Sorry, I couldn't understand. Try again.")
        except sr.RequestError:
            st.error("Could not request results. Check your internet connection.")
            speak("Could not request results. Check your internet connection.")

    time.sleep(1)  # Wait for the speaking to finish
    # streamlit_js_eval(js_expressions="parent.window.location.reload()")


# Wake word listener running in a separate thread
def wake_word_listener():
    global wake_word_detected
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=None)  # Keep listening
                command = recognizer.recognize_google(audio).lower()
                if "hey tars" in command:
                    stop_speaking.set()
                    speak("Yes, how can I assist you?")
                    process_command()  # Call command processor immediately
            except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
                continue  # Keep listening

wake_thread = threading.Thread(target=wake_word_listener, daemon=True)
wake_thread.start()

# Streamlit UI
st.title("🔊 Tars - Voice Assistant")

# Manual voice input
if st.button("🎙️ Speak Command"):
    process_command()

st.write("---")

text_input = st.text_input("Type a command:")
if st.button("Send Command") and text_input:
    response = get_gemini_response(text_input)
    st.write("🤖 Tars: ", response)
    speak(response)
