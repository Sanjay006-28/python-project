# Import necessary libraries
import speech_recognition as sr  # For converting speech to text
import webbrowser                # To open web URLs
import pyttsx3                   # For offline text-to-speech (not used here, kept as fallback)
import musicLibrary              # Your own dictionary of songs (should be defined separately)
import requests                  # For making API requests
from gtts import gTTS            # Google Text-to-Speech (online TTS)
import pygame                    # For playing MP3 audio
import os                        # For file handling (temp audio files)

# Initialize the speech recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Your NewsAPI key
newsapi = "7106eb1649b64609bfddfc2e3ad6c5b0"

# Fallback speech engine using pyttsx3 (offline, not used)
def speak_old(text):
    print("Speaking:", text)
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()

# Main speak function using gTTS + pygame
def speak(text):
    tts = gTTS(text)                    # Convert text to speech using Google TTS
    tts.save('temp.mp3')                # Save the speech as MP3
    pygame.mixer.init()                 # Initialize Pygame mixer
    pygame.mixer.music.load('temp.mp3') # Load the MP3 file
    pygame.mixer.music.play()           # Play the audio
    while pygame.mixer.music.get_busy():# Wait until the playback finishes
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()         # Unload the MP3
    os.remove("temp.mp3")               # Delete the temporary file

# Function to process AI responses using Groq API
def aiProcess(command):
    url = "https://api.groq.com/openai/v1/chat/completions"  # Groq LLM endpoint
    headers = {
        "Authorization": f"Bearer gsk_JBFITG7d3c6glO0QKUGfWGdyb3FYJtLKTSwdYzamvA21X16MZJ6",  # Your Groq API key
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",       # Groq uses LLaMA 3 model
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": command}
        ]
    }
    response = requests.post(url, headers=headers, json=data)  # Send POST request
    if response.status_code == 200:
        result = response.json()["choices"][0]["message"]["content"]
        print("🧠 Jarvis says:", result)  # Print AI response
        return result
    else:
        print("Error from Groq:", response.text)
        return "Sorry, I couldn't get a response."

# Function to process all commands spoken by user
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkdin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found.")
    elif "news" in c.lower():
        # Fetch and speak 5 latest news headlines from India
        r = requests.get(f"https://newsapi.org/v2/everything?q=india&sortBy=publishedAt&language=en&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for i, article in enumerate(articles[:5], start=1):
                print(f"News {i}: {article['title']}")  # Print news
                speak(article['title'])                # Speak news
        else:
            print("Failed to fetch news.")
            speak("Sorry, I couldn't fetch the news.")
    else:
        # If none of the above, use AI to respond
        output = aiProcess(c)
        speak(output)

# Entry point of the program
if __name__ == "__main__":  
    speak("Initializing Jarvis....")  # Start-up voice
    while True:
        r = sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)  # Listen for wake word
            word = r.recognize_google(audio)  # Convert audio to text
            if word.lower() == "jarvis":
                print("wake word activated")
                speak("Ya")
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)  # Listen for command
                    command = r.recognize_google(audio)
                    print("You said:", command)
                    if "stop" in command.lower():
                        speak("Okay, shutting down.")  # Shutdown voice
                        break  # Exit loop and program
                    processCommand(command)  # Process the given command
        except Exception as e:
            print("Error; {0}".format(e))  # Catch errors from microphone or recognition
