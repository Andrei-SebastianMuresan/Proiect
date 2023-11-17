
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

r = sr.Recognizer()


def record_audio(ask = False):
    with sr.Microphone() as source:
        if ask:
            sebi_speak(ask)
            
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio, language = "en-EN")
            #print(voice_data)
        except sr.UnknownValueError:
           sebi_speak('Sorry, I did not get that')
        except sr.RequestError:
            sebi_speak('Sorry, the system is down')
        return voice_data
    
def sebi_speak(audio_string):
    tts = gTTS(text = audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)
     
      
def respond(voice_data):
    if 'What is your name' in voice_data:
        name=input("enter your name here:")
        sebi_speak('My name is ' + str(name) + "'s Assistant")
    if 'What time is it' in voice_data:
        sebi_speak(ctime())
    if 'search' in voice_data:
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        sebi_speak('Here is what I found for ' + search)
    if 'find location' in voice_data:
        location = record_audio('What is the location?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        sebi_speak('Here is the location of ' + location) 
    if 'Play' in voice_data:
        song = voice_data.replace('Play', '')
        sebi_speak('playing' + song)
        pywhatkit.playonyt(song)
    if 'Who is' in voice_data:
        person = voice_data.replace('Who is', '')
        info = wikipedia.summary(person, 1)
        sebi_speak(info)
    if 'Exit' in voice_data:
        sys.exit()

''' THIS PART OF THE PROJECT IS WITH AN UI (BUT WE CAN USE THE ASSISTANT ONLY WITH VOICE )

def on_button_click(entry):
    user_input = entry.get()
    respond(user_input)

# main application window
app = tk.Tk()
app.title("Voice Assistant")

# text entry widget
entry = tk.Entry(app, width=50)
entry.grid(row=0, column=0, padx=10, pady=10)

# button to trigger the assistant's response
button = tk.Button(app, text="Ask", command=lambda: on_button_click(entry))
button.grid(row=0, column=1, padx=10, pady=10)

# Start the Tkinter event loop
app.mainloop()
'''

time.sleep(1) 
sebi_speak("Good day my dear friend! How May I help you?")
while 1:
    voice_data = record_audio()
    respond(voice_data)


