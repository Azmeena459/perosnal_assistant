from flask import Flask, render_template, jsonify
import datetime
import wikipedia
import webbrowser
import requests
import pyttsx3
import speech_recognition as sr
import wolframalpha

app = Flask(__name__)

import pyttsx3

engine = pyttsx3.init()  # Initialize engine once globally

def speak(message):
    engine.say(message)
    engine.runAndWait()

# Initialize pyttsx3 (Text-to-Speech engine)
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[0].id)

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wish')
def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        message = "Good Morning!"
    elif hour >= 12 and hour <= 18:
        message = "Good Afternoon!"
    else:
        message = "Good Evening!"
    return jsonify(message=message)

@app.route('/search_wikipedia/<query>')
def search_wikipedia(query):
    results = wikipedia.summary(query, sentences=3)
    return jsonify(results=results)

@app.route('/weather/<city_name>')
def get_weather(city_name):
    api_key = "8ef61edcf1c576d65d836254e11ea420"
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        return jsonify(description=weather_description, temp=current_temperature, humidity=current_humidity)
    else:
        return jsonify(description="City not found", temp=None, humidity=None)

@app.route('/say/<message>')
def say_message(message):
    speak(message)
    return jsonify(message=message)

@app.route('/ask/<question>')
def ask_question(question):
    app_id = "R2K75H-7ELALHR35X"
    client = wolframalpha.Client(app_id)
    try:
        res = client.query(question, timeout=30)
        answer = next(res.results).text
        return jsonify(answer=answer)
    except StopIteration:
        return jsonify(answer="I could not find an answer.")

if __name__ == "__main__":
    app.run(debug=True)
