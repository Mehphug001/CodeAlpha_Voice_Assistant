import speech_recognition as sr
import pyttsx3
import requests
from datetime import datetime

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Captures audio input and converts it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand you.")
        except sr.RequestError:
            speak("There seems to be an issue with the speech recognition service.")
        except sr.WaitTimeoutError:
            speak("You didn't say anything.")
    return ""

def get_country_capital(country):
    """Returns the capital of the given country."""
    capitals = {
        "india": "New Delhi",
        "united states": "Washington, D.C.",
        "france": "Paris",
        "germany": "Berlin",
        "italy": "Rome",
        "japan": "Tokyo",
        "china": "Beijing",
        "russia": "Moscow",
        "brazil": "Brasília",
        "canada": "Ottawa"
        # Add more countries and their capitals here
    }
    return capitals.get(country.lower(), "Sorry, I don't know the capital of that country.")

def get_weather(city):
    """Returns the current weather for the given city."""
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(complete_url)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]['description']
        temperature = main['temp']
        return f"The current weather in {city} is {weather} with a temperature of {temperature}°C."
    else:
        return "Sorry, I couldn't get the weather for that city."

def respond(command):
    """Processes the command and provides appropriate responses."""
    if "wikipedia" in command:
        speak("Searching Wikipedia...")
        query = command.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(result)
    elif "your name" in command:
        speak("I am your friendly voice assistant and my name is Nasim")
    elif "time" in command:
        now = datetime.now().strftime("%H:%M")
        speak(f"The time is {now}.")
    elif "date" in command:
        today = datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}.")
    elif "capital of" in command:
        country = command.split("capital of")[-1].strip()
        capital = get_country_capital(country)
        speak(f"The capital of {country} is {capital}.")
    elif "weather" in command:
        city = command.split("weather in")[-1].strip()
        weather = get_weather(city)
        speak(weather)
    elif "help" in command:
        speak("I can help you with the following commands: ")
        speak("1. Ask for the time.")
        speak("2. Ask for today's date.")
        speak("3. Ask for the capital of a country.")
        speak("4. Ask for the weather in a city.")
        speak("5. Ask about my name.")
        speak("6. Search something on Wikipedia.")
        speak("7. Say 'exit' or 'stop' to end this conversation.")
    else:
        speak("I am not sure how to respond to that.")

def main():
    """Main function to run the voice assistant."""
    speak("Hello! I am your voice assistant. How can I help you today?")
    while True:
        command = listen()
        if "exit" in command or "stop" in command:
            speak("Goodbye!")
            break
        respond(command)

if __name__ == "__main__":
    main()
