# Resize the Window - Non Pep8 Compliant, mandated by Kivy
from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '200')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty

import speech_recognition as sr
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import pyttsx

r = sr.Recognizer()
m = sr.Microphone()
t = pyttsx.init()
t.setProperty('rate', 90)
#t.setProperty('voice', t.getProperty('voices')[1].id)

english_bot = ChatBot("Rao")

#Custom conversation list
conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome.",
    "do you have boyfriend",
    "yes",
    "what is gold plan?",
    "lets explain about the gold plan.. are you clear about this?",
    "quit",
    "bye bye",
    "search for power tools",
    "power tools"
]

#set the type of trainer to chatbot
english_bot.set_trainer(ListTrainer)
#set the list for train
english_bot.train(conversation)


# Root Widget
class Root(BoxLayout):
    pass


class RecordButton(Button):
    # String Property to Hold output for publishing by Textinput
    output = StringProperty('')
    inputarea = StringProperty('')
    
    def record(self):
        # GUI Blocking Audio Capture
        #while True: 
        with m as source:
            audio = r.listen(source)
        
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)
            self.inputarea = "Your request \"{}\"".format(value)
            respstr = english_bot.get_response(value)
            t.say(respstr)
            t.runAndWait()
            self.output = "Reply by me \"{}\"".format(respstr)
            if value=='quit':
                return
            
        
        except sr.UnknownValueError:
            self.output = ("Oops! I failed to catch you :(")
        
        except sr.RequestError as e:
            self.output = ("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))


class SpeechChatBotApp(App):
    
    def build(self):
        # Calibrate the Microphone to Silent Levels
        print("A moment of silence, please...")
        with m as source:
            r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(r.energy_threshold))
        # Create a root widget object and return as root
        return Root()


# When Executed from the command line (not imported as module), create a new SpeechApp
if __name__ == '__main__':
    SpeechChatBotApp().run()
