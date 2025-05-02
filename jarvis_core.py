import openai
import pyttsx3
import speech_recognition as sr
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("🎤 Ouvindo...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio, language="pt-BR")
        except sr.UnknownValueError:
            return ""

def generate_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente de voz"},
                {"role": "user", "content": user_input}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Jarvis: Erro ao gerar resposta: {e}")
        return "Erro ao gerar resposta."

# Loop principal
print("🤖 Jarvis iniciado. Diga algo!")
while True:
    user_input = listen()
    print(f"Você disse: {user_input}")
    if user_input:
        response = generate_response(user_input)
        print(f"Jarvis: {response}")
        speak(response)


