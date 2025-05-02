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
        print("Ouvindo...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio, language="pt-BR")
        except sr.UnknownValueError:
            return "Não entendi o que você disse."
        except sr.RequestError:
            return "Erro ao acessar o serviço de reconhecimento."

def gerar_resposta(prompt):
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente útil."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Erro ao gerar resposta:", e)
        return "Jarvis: Erro ao gerar resposta."

while True:
    comando = listen()
    print("Você disse:", comando)
    resposta = gerar_resposta(comando)
    print("Jarvis:", resposta)
    speak(resposta)

