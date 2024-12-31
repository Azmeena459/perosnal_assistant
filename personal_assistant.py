import os
import time
import subprocess
import json
import wolframalpha
import requests
import webbrowser
import wikipedia
import datetime
import speech_recognition as sr
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[0].id)

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to wish the user based on the time of day
def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak("Hello, Good Morning")
        print("Hello, Good Morning")
    elif hour >= 12 and hour <= 18:
        speak("Hello, Good Afternoon")
        print("Hello, Good Afternoon")
    else:
        speak("It's already late, better go to sleep")
        print("It's already late, better go to sleep")

# Function to take voice command
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I AM LISTENING")
        audio = r.listen(source)
        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said: {statement}\n")
            return statement
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return "None"
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return "None"
        except Exception as e:
            print(f"An error occurred: {e}")
            return "None"

# Main program logic
if __name__ == '__main__':
    speak("LOADING YOUR PERSONAL A.I ASSISTANT")
    wishMe()

    while True:
        speak("How can I help you?")
        statement = takeCommand().lower()

        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak("Your personal AI assistant is shutting down, Goodbye!")
            print("Your personal AI assistant is shutting down, Goodbye!")
            break

        if 'wikipedia' in statement:
            speak("Searching Wikipedia...")
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia...")
            print(results)
            speak(results)

        elif "open youtube" in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("YouTube is open for you")
            time.sleep(5)

        elif "open google" in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google search is open for you")
            time.sleep(5)

        elif "open gmail" in statement:
            webbrowser.open_new_tab("https://www.gmail.com")
            speak("Your Gmail is open for you")
            time.sleep(5)

        elif "weather" in statement:
            api_key = "8ef61edcf1c576d65d836254e11ea420"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("What's the city name?")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(f"The temperature in kelvin units is {current_temperature}. "
                      f"Humidity in percentage is {current_humidity}. "
                      f"Weather description: {weather_description}.")
                print(f"The temperature in kelvin units is {current_temperature}. "
                      f"Humidity in percentage is {current_humidity}. "
                      f"Weather description: {weather_description}.")
            else:
                speak("City not found")
                print("City not found")

        elif "time" in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif "who are you" in statement or "what can you do" in statement:
            speak("I am version 1.0, your personal assistant. I can perform tasks like "
                  "opening YouTube, Google Chrome, Gmail, and Stack Overflow, predicting time, "
                  "taking photos, searching Wikipedia, predicting weather in different cities, "
                  "getting top news headlines, and answering computational or geographical questions.")

        elif "who made you" in statement or "who created you" in statement:
            speak("I was built by Azmeena")
            print("I was built by Azmeena")

        elif "open stack overflow" in statement:
            webbrowser.open_new_tab("https://stackoverflow.com/login")
            time.sleep(5)

        elif "news" in statement:
            webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak("Here are some headlines for you from Times of India - happy reading!")
            time.sleep(7)

        elif "search" in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif "ask" in statement:
            speak("I can answer computational and geographical questions. What do you want to ask?")
            question = takeCommand()
            app_id = "R2K75H-7ELALHR35X"
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)

        elif "log off" in statement or "sign out" in statement or "shutdown" in statement:
            speak("OK, Your PC will shut down in 10 seconds. Make sure you save and exit all applications.")
            subprocess.call(['shutdown', "/s"])
            time.sleep(5)
