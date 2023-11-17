import tkinter as tk
import pyttsx3
import speech_recognition as sr
from time import ctime
import webbrowser
import sys
import pywhatkit
import wikipedia
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from plyer import notification
from parsedatetime import Calendar

class VoiceAssistant:
    def __init__(self):
        self.user_name = "User"
        self.voice_engine = pyttsx3.init()
        self.voice_rate = 150
        self.context = None

    def sebi_speak(self, text):
        self.voice_engine.setProperty('rate', self.voice_rate)
        self.voice_engine.say(text)
        self.voice_engine.runAndWait()
    
    
    def record_audio(self, prompt=None):
        with sr.Microphone() as source:
            if prompt:
                self.sebi_speak(prompt)

            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            voice_data = ''
            try:
                voice_data = r.recognize_google(audio, language="ro-RO")
            except sr.UnknownValueError:
                self.sebi_speak('Sorry, I did not get that')
            except sr.RequestError:
                self.sebi_speak('Sorry, the system is down')
            return voice_data

    def respond(self, voice_data):
        if 'Set a reminder' in voice_data:
            self.set_reminder()

        if 'greetings' in voice_data:
            self.sebi_speak('Nice to meet you, ' + assistant.user_name)
        elif 'what is your name' in voice_data:
            self.sebi_speak('My name is ' + assistant.user_name + "'s Assistant")
        elif 'what time is it' in voice_data:
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
        elif 'play' in voice_data:
            song = voice_data.replace('Play', '')
            self.sebi_speak('Playing ' + song)
            pywhatkit.playonyt(song)
        elif 'who is' in voice_data:
            person = voice_data.replace('Who is', '')
            info = wikipedia.summary(person, 1)
            self.sebi_speak(info)
        elif 'exit' in voice_data:
            sys.exit()
        elif 'how are you' in voice_data:
            self.sebi_speak('I am doing well, thank you for asking!')
        else:
            self.sebi_speak("I'm not sure how to respond to that. Can you provide more details?")

    def set_reminder(self):
        self.sebi_speak("Sure, please tell me what you want to be reminded about and when.")

        # Get the reminder details from the user
        reminder_details = self.record_audio()
        self.sebi_speak(f"Setting a reminder for {reminder_details}")

        # Parse the reminder time using parsedatetime
        cal = Calendar()
        time_struct, parse_status = cal.parse(reminder_details)

        if parse_status == 0:
            self.sebi_speak("Sorry, I couldn't understand the time. Please try again.")
            return

    # Schedule the reminder notification
    schedule_notification("Reminder", f"Time to {reminder_details}", time_struct)


def set_reminder(self):
        self.sebi_speak("Sure, please tell me what you want to be reminded about and when.")

        # Get the reminder details from the user
        reminder_details = self.record_audio()
        self.sebi_speak(f"Setting a reminder for {reminder_details}")

        # Parse the reminder time using parsedatetime
        cal = Calendar()
        time_struct, parse_status = cal.parse(reminder_details)

        if parse_status == 0:
            self.sebi_speak("Sorry, I couldn't understand the time. Please try again.")
            return

        # Schedule the reminder notification
        self.schedule_notification("Reminder", f"Time to {reminder_details}", time_struct)

def schedule_notification(self, title, message, time_struct):
        notification_time = time.mktime(time_struct)
        notification.schedule(
            title=title,
            message=message,
            timeout=10,  # Notification timeout in seconds
            toast=True,  # Display as toast notification (Windows)
            ticker=message,  # Notification ticker text (Android)
            app_icon=None,  # Icon path for Windows (None uses the default)
            timeout_notify=True,
            toast_timeout=10,
            callback=None,  # Callback function to be called when the notification is clicked
            app_name='Voice Assistant'  # App name for Linux
        )

def on_button_click(entry, mode_var, assistant):
    user_input = entry.get()
    if mode_var.get() == 1:  # Voice mode
        assistant.respond(assistant.record_audio(user_input))
    else:  # Text mode
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

    # Create a radio button for selecting the input mode
    mode_var = tk.IntVar()
    voice_mode_radio = tk.Radiobutton(app, text="Voice Mode", variable=mode_var, value=1)
    text_mode_radio = tk.Radiobutton(app, text="Text Mode", variable=mode_var, value=2)

    voice_mode_radio.grid(row=1, column=0, padx=10, pady=5)
    text_mode_radio.grid(row=1, column=1, padx=10, pady=5)

    # Create a button to trigger the assistant's response
    button = tk.Button(app, text="Ask", command=lambda: on_button_click(entry, mode_var, assistant))
    button.grid(row=2, column=0, columnspan=2, pady=10)

    # Example of setting a reminder
    assistant.set_reminder()
  
    # Start the Tkinter event loop
    app.mainloop()