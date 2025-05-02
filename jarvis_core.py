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
