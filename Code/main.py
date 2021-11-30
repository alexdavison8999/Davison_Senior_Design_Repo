from vosk import Model, KaldiRecognizer
import os
import pyaudio
import json
import pyttsx3
import time
import requests
import wifi
from bs4 import BeautifulSoup

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices') #fetching different voices from the system
engine.setProperty('voice', voices[1].id) #setting voice properties
engine.setProperty('rate', 190) #sets speed of speech

whatis = "What is"
warningString = "Warning"
seString = 'side effects'
iTakeString = 'take'

def userSelection(soup, filterString):
    for data in soup.find_all('h2'):
        if filterString in data.text:
            for dat in data.find_all_next(['p', 'h2']):
                if dat.name == 'h2':
                    break
                print(dat.text)
                speak(dat.text)

def readSite(url, drugname):
    resp = requests.get(url)
    infoCount = 0

    if resp.status_code == 200:
        print("Successfully opened the web page")
        # print("The news are as follow :-\n")

        soup = BeautifulSoup(resp.text, 'lxml')

        for data in soup.find_all('h2'):
            # print(data.text)
            if whatis in data.text:
                for dat in data.find_all_next(['p', 'h2']):
                    if infoCount > 0:
                        break
                    if dat.name == 'h2':
                        break
                    print(dat.text)
                    speak(dat.text)
                    infoCount = infoCount + 1

                print('Select an option to learn more information about', drugname)
                speak(('Select an option to learn more information about', drugname))
                print('Warnings')
                speak('warnings')
                print('How should I take', drugname)
                speak(('How should I take', drugname))
                print('Side Effects')
                speak('side effects')
                print('None')
                speak(('or none, if you want to stop learning about', drugname))

                while True:
                    specify = secondCommand()
                    if specify:
                        if 'i take' in specify:
                            print(specify)
                            userSelection(soup, iTakeString)
                        elif 'warnings' in specify:
                            print(specify)
                            userSelection(soup, warningString)
                        elif 'side effects' in specify:
                            print(specify)
                            userSelection(soup, seString)
                        elif 'none' in specify:
                            print(specify)
                            speak('alright, let me know if you need anything else')
                            return
    else:
        print('couldnt open')

def metformin():
    url = 'https://www.drugs.com/metformin.html'
    selection = readSite(url, 'Metformin')

def lisinopril():
    url = 'https://www.drugs.com/lisinopril.html'
    selection = readSite(url, 'Lisinopril')

def amlodipine():
    url = 'https://www.drugs.com/amlodipine.html'
    selection = readSite(url, 'Amlodipine')

def albuterol():
    url = 'https://www.drugs.com/albuterol.html'
    selection = readSite(url, 'Albuterol')

def speak(text):
    time.sleep(.5)
    engine.say(text)
    engine.runAndWait()

# Speech Recognition

model = Model("model")
rec = KaldiRecognizer(model, 16000)

# Opens microphone for listening.
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

def command():
    data = stream.read(4000, exception_on_overflow = False)
    #if len(data) == 0:
        #break
    if rec.AcceptWaveform(data):
        # result is a string
        result = rec.Result()
        # convert it to a json/dictionary
        result = json.loads(result)

        text = result['text']
        print(text)

        if text == 'can you tell me about my medicine' or text == 'why am i taking these pills':
            speak("Sure. What medicine would you like more information on?")
            while True:
                specificMedicine = secondCommand()
                if specificMedicine:
                    break
            if specificMedicine == "metformin":
                metformin()
            elif specificMedicine == "lisinopril":
                lisinopril()
            elif specificMedicine == "amlodipine":
                amlodipine()
            elif specificMedicine == "albuterol":
                albuterol()
        if text == "metformin":
            metformin()


def secondCommand():
    data = stream.read(4000, exception_on_overflow = False)
    if rec.AcceptWaveform(data):
        result = rec.Result()
        result = json.loads(result)

        text = result['text']
        return(text)

#wifi.connectingToExistingWifi()

while True:
    command()


#try metformin, lisinopril, amlodipine, albuterol,

#not working Atorvastatin, Levothyroxine, Metoprolol, Omeprazole, Losartan, Simvastatin
