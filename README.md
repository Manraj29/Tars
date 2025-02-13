# 🗣️ Tars - Your Voice-Activated AI Assistant  

Tars is a **voice-activated AI assistant** that listens for the wake word **"Hey Tars"**, responds to queries, opens applications, and searches the web. It uses **Google Gemini API** for AI responses and supports **real-time interruption** while speaking.

## 🚀 Features  
✅ **Wake Word Detection** → Always listening for "Hey Weekend"  
✅ **AI-Powered Answers** → Uses **Google Gemini API** (Short & Concise)  
✅ **Open Applications** → Chrome, Notepad, Calculator, Spotify (Customizable)  
✅ **Search the Web** → Instantly Google search queries  
✅ **Error Handling** → Automatically returns to wake-word listening  

## 📌 Installation  
1. **Clone the Repository**
     ```sh git clone https://github.com/Manraj29/tars.git```
2. **Install Dependencies**
     ```pip install -r requirements.txt```
3. **Set Up Google Gemini API Key**
     ```GEMINI_API_KEY = "your_api_key_here"```
4. **Run the python script**
     ```python tars.py```,
**if streamlit** ```streamlit run tarslit.py```

## 🛠️ Usage 
### * for cmd app
Run the script, 
Then, say "Hey Tars" and:
- "Open Chrome" → Opens Google Chrome
- "Search for Python tutorials" → Opens Google search
- "Who is Elon Musk?" → Gets AI-generated response

### * for streamlit app
Run the streamlit app,
Then Interact with Tars through:
1. Voice Commands: Say "Hey Tars" to activate, then:
 - "Open Notepad"
 - "Search for the latest tech news"
 - "What is the weather like today?"
 - "Tell me a joke"
2. Text Commands: Type directly into the text box and click Send Command.

## 📜 Requirements
1. Python 3.7+
2. speechrecognition (for voice commands)
3. google-generativeai (for AI responses)
4. pyttsx3 (for text-to-speech)
5. pyaudio (for microphone input)
6. webbrowser (for Google search)
