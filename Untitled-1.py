import speech_recognition as sr
import webbrowser
import time
import sys
import playsound
import os
import random
import pyttsx3
import pywhatkit
import wikipedia
from gtts import gTTS
from time import ctime
import tkinter as tk



class VoiceAssistant:
    def __init__(self):
        self.user_name = "User"
        self.voice_engine = pyttsx3.init()
        self.voice_rate = 150  # Adjust as needed
        self.context = None 

    def sebi_speak(self, text):
        self.voice_engine.setProperty('rate', self.voice_rate)
        self.voice_engine.say(text)
        self.voice_engine.runAndWait()

    def record_audio(self, prompt):
        with sr.Microphone() as source:
            if prompt:
                self.sebi_speak(prompt)

            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            voice_data = ''
            try:
                voice_data = r.recognize_google(audio, language="ro-RO")
                # print(voice_data)
            except sr.UnknownValueError:
                self.sebi_speak('Sorry, I did not get that')
            except sr.RequestError:
                self.sebi_speak('Sorry, the system is down')
            return voice_data

    def respond(self, voice_data):
        if 'Greetings' in voice_data:
            self.user_name = input("Enter your name here: ")
            self.sebi_speak('Nice to meet you, ' + self.user_name)
        elif 'What is your name' in voice_data:
        
            self.sebi_speak('My name is ' + assistant.user_name + "'s Assistant")
        elif 'What time is it' in voice_data:
            self.sebi_speak(ctime())
        elif 'search' in voice_data:
            search = self.record_audio('What do you want to search for?')
            url = 'https://google.com/search?q=' + search
            webbrowser.get().open(url)
            self.sebi_speak('Here is what I found for ' + search)
        elif 'find location' in voice_data:
            location = self.record_audio('What is the location?')
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.get().open(url)
            self.sebi_speak('Here is the location of ' + location) 
        elif 'Play' in voice_data:
            song = voice_data.replace('Play', '')
            self.sebi_speak('Playing ' + song)
            pywhatkit.playonyt(song)
        elif 'Who is' in voice_data:
            person = voice_data.replace('Who is', '')
            info = wikipedia.summary(person, 1)
            self.sebi_speak(info)
        elif 'Exit' in voice_data:
            sys.exit()

def on_button_click(entry, assistant):
    user_input = entry.get()
    assistant.respond(user_input)

def personalize_assistant(assistant):
    assistant.user_name = input("Enter your preferred name: ")
    assistant.voice_rate = int(input("Enter your preferred voice rate (e.g., 150): "))

if __name__ == "__main__":
    assistant = VoiceAssistant()

    # Personalize the assistant
    personalize_assistant(assistant)

    # Create the main application window
    app = tk.Tk()
    app.title("Voice Assistant")

    # Create a text entry widget
    entry = tk.Entry(app, width=50)
    entry.grid(row=0, column=0, padx=10, pady=10)

    # Create a button to trigger the assistant's response
    button = tk.Button(app, text="Ask", command=lambda: on_button_click(entry, assistant))
    button.grid(row=0, column=1, padx=10, pady=10)

    # Start the Tkinter event loop
    app.mainloop()