import speech_recognition as sr #module for performing speech recognition
import time as t
import webbrowser 
import playsound #module for playing sound files in python
import os #module for performing tasks on computer
import random
import wikipedia
from gtts import gTTS #google text-to-speech for generating voice by reading strings 
import requests, json #modules for requesting data from web

r = sr.Recognizer()

#fucntion to check for multiple words in command
def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

#record command function
def recordAudio(ask = ""):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source)
        r.adjust_for_ambient_noise(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
            print(voice_data)
            return voice_data
        except sr.UnknownValueError:
            speak('Sorry, I did not get that.')
        except sr.RequestError:
            speak('Sorry, my services are currently down.')

#speak function
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 1000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)
        

def respond(voice_data):
    if 'what is your name' in voice_data:
        speak('Hello, I m Nicole. Your personal voice assistant.')

    #greeting
    if there_exists(['hi', 'hey', 'hello']):
        speak('hi, how are you doing?')

    if 'how are you' in voice_data:
        speak('Hi! I m doing well, how are you today?')
        
    #asking time
    if 'what time is it' in voice_data:
        time = t.strftime('%X')
        arr = time.split(':')
        time = arr[0:2]
        time = ":".join(time)
        speak(f"right now the time is {time}")

    #search for things on google
    if there_exists(["search for"]) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term}')

    #opening google
    if 'open Google' in voice_data:
        webbrowser.open('https://google.com')
        speak('I have opened Google Chrome for you.')
    
    #asking questions using wikipedia api
    if 'tell me more about' in voice_data:
        arr1 = voice_data.split()
        arr2 = arr1[4:]
        info_term = " ".join(arr2)
        result = wikipedia.summary(info_term, sentences = 2)
        speak(result)

    #asking for the weather
    if 'weather in' in voice_data:
        arr1 = voice_data.split()
        arr2 = arr1[2:]
        city = " ".join(arr2)
        api_key = 'MY API KEY'
        #print(city)
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(weather_url)
        if response.status_code == 200:
            data = response.json()
            #print(data)
            main = data['main']
            temp = main['temp']
            desc = data['weather']
            speak(f"It is {temp} degree celcius in {city} right now and the weather report is {desc[0]['description']}")
        else:
            speak("Sorry, error connecting to weather API")


#main function
if __name__ == '__main__':
    speak('Hi, I am Nicole. How can I help you?')
    voice_data = recordAudio()
    respond(voice_data)

