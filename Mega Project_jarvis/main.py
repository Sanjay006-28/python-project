import speech_recognition as sr  # speech_recognition is said as sr
import webbrowser 
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "7106eb1649b64609bfddfc2e3ad6c5b0"

def speak_old(text):
        print("Speaking:", text)
        engine = pyttsx3.init('sapi5')
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 
        
def aiProcess(command):
    client = OpenAI(api_key="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",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

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
        r = requests.get(f"https://newsapi.org/v2/everything?q=india&sortBy=publishedAt&language=en&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for i, article in enumerate(articles[:5], start=1):
                print(f"News {i}: {article['title']}")
                speak(article['title'])
        else:
            print("Failed to fetch news.")
            speak("Sorry, I couldn't fetch the news.")
    else:
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":  
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()

        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if word.lower() == "jarvis":
                print("work word activate")
                speak("Ya")
                # listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print("You said:", command)
                    if "stop listening" in command.lower():
                        speak("Okay, shutting down.")
                        break
                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))
            
# python -m pip install -r requirements.txt

