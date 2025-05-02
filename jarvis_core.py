import speech_recognition as sr
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def ouvir_comando():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Ouvindo...")
        audio = recognizer.listen(source)
        try:
            comando = recognizer.recognize_google(audio, language='pt-BR')
            print(f"🗣️ Você disse: {comando}")
            return comando.lower()
        except sr.UnknownValueError:
            print("😕 Não entendi o que você disse.")
        except sr.RequestError:
            print("❌ Erro ao se conectar com o serviço de voz.")
    return ""

def responder_comando(comando):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": comando}]
        )
        return resposta.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"

def main():
    print("🧠 Jarvis iniciado. Diga algo!")
    while True:
        comando = ouvir_comando()
        if comando:
            resposta = responder_comando(comando)
            print(f"🤖 Jarvis: {resposta}")

if __name__ == "__main__":
    main()