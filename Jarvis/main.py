import speech_recognition as sr
import webbrowser 
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init()     # Object Creation
newsapiKey = "xxxxxxx"

# Speaks the provided text 
def speak(text):
    engine.say(text)
    engine.runAndWait()     # ensures speech command is executed first before executing further lines

# To handle the others commands by OpenAI
def aiProcess(command):
    client = OpenAI(api_key="xxxxx-xxxx")

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful virtual assistant named \"Jarvis\"."},
            {
                "role": "user",
                "content": command  
            }
        ]
    )

    return print(completion.choices[0].message.content)

# For processing command for the Jarvis ; c is the command(str)
def processCommand(c):   

    # opening websites
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://in.linkedin.com/")

    # opening music
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    # opening news
    elif "news" in c.lower():
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapiKey}")

        if response.status_code == 200:  # Check if the request was successful
            news_data = response.json()  # Parse the JSON response
        
            # Loop through the articles and print the title and description
            for article in news_data.get('articles', []):
                title = article.get('title')
                speak(title)
        else:
            print(f"Failed to fetch news. Status code: {response.status_code}")
    else:
        # Let openAI handle the request
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak(" Initialising Jarvis...")

    while True :
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone 
        r = sr.Recognizer()

        # recognize speech using Google
        print("Recognising...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout = 2, phrase_time_limit=1)
            word = r.recognize_google(audio)

            if(word.lower() == "jarvis"):
                # Reply from Jarvis
                speak(" Yes")
                
                # listen for command
                with sr.Microphone() as source:
                    print("Jarvis is active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except sr.UnknownValueError:
            print("Google could not understand audio.")
        except Exception as e:
            print(f"Google error: {e}")
        


