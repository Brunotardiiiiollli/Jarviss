import openai
import pyttsx3
import speech_recognition as sr

# Chave da OpenAI embutida diretamente no código
openai.api_key = "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"

engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("🎙️ Ouvindo...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio, language="pt-BR")
        except sr.UnknownValueError:
            return "Não entendi o que você disse."
        except sr.RequestError:
            return "Erro ao acessar o serviço de reconhecimento."

def ask_openai(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Jarvis: Erro ao gerar resposta: {e}"

def main():
    print("🤖 Jarvis iniciado. Diga algo!")
    while True:
        question = listen()
        print(f"🗣️ Você disse: {question}")
        answer = ask_openai(question)
        print(f"🤖 {answer}")
        speak(answer)

if __name__ == "__main__":
    main()
