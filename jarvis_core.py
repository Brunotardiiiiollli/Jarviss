
import os, json, queue, pyaudio, openai, threading
from dotenv import load_dotenv
from twilio.rest import Client
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.auth.exceptions

class JarvisAssistant:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.AUDIO_RATE = 16000
        self.WAKE_WORD = os.getenv("WAKE_WORD","jarvis").lower()
        self.audio_q = queue.Queue()
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.running = False
        # External services
        tw_sid = os.getenv("TWILIO_ACCOUNT_SID")
        tw_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.twilio_from = os.getenv("TWILIO_WHATSAPP_FROM","whatsapp:+14155238886")
        self.twilio_client = Client(tw_sid, tw_token) if tw_sid else None
        try: self.gcal = self._google_service()
        except Exception: self.gcal=None

    def _google_service(self):
        SCOPES=['https://www.googleapis.com/auth/calendar.events']
        if not os.path.exists('credentials.json'): return None
        from google.oauth2.credentials import Credentials
        creds=None
        if os.path.exists('token.json'):
            creds=Credentials.from_authorized_user_file('token.json',SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow=InstalledAppFlow.from_client_secrets_file('credentials.json',SCOPES)
                creds=flow.run_local_server(port=0)
            with open('token.json','w') as tk: tk.write(creds.to_json())
        return build('calendar','v3',credentials=creds)

    # --- Runnable functions ---
    def send_message(self,to,body):
        if not self.twilio_client:
            return "Twilio não configurado."
        self.twilio_client.messages.create(
            from_=self.twilio_from,
            to=f'whatsapp:{to}' if not to.startswith("whatsapp:") else to,
            body=body
        )
        return "Mensagem enviada!"

    def schedule_event(self,title,date,time):
        if not self.gcal:
            return "Google Agenda não configurado."
        event={
            "summary":title,
            "start":{"dateTime":f"{date}T{time}:00",
                     "timeZone":"America/Sao_Paulo"},
            "end":{"dateTime":f"{date}T{time}:00",
                   "timeZone":"America/Sao_Paulo"}
        }
        self.gcal.events().insert(calendarId='primary',body=event).execute()
        return "Evento criado."

    def _process_text(self,text):
        functions=[
            {"name":"send_message","description":"Envia mensagem", "parameters":{"type":"object","properties":{"to":{"type":"string"},"body":{"type":"string"}},"required":["to","body"]}},
            {"name":"schedule_event","description":"Agenda compromisso","parameters":{"type":"object","properties":{"title":{"type":"string"},"date":{"type":"string"},"time":{"type":"string"}},"required":["title","date","time"]}}
        ]
        resp=openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":text}],
            functions=functions,
            temperature=0
        )
        choice=resp.choices[0]
        if choice.finish_reason=="function_call":
            fn=choice.message.function_call.name
            args=json.loads(choice.message.function_call.arguments)
            return getattr(self,fn)(**args)
        return choice.message.content

    def _speech(self,msg):
        try:
            speech=openai.audio.speech.create(
                model="tts-1",
                input=msg,
                voice="alloy",
                format="wav"
            )
            with open("response.wav","wb") as f: f.write(speech.audio)
            if os.name=="nt":
                os.startfile("response.wav")
            elif sys.platform=="darwin":
                os.system("afplay response.wav")
            else:
                os.system("aplay response.wav")
        except Exception as e:
            print("Erro TTS:",e)

    def _transcribe_chunk(self,chunk):
        try:
            tr=openai.audio.transcriptions.create_stream(
                model="whisper-large-v3",
                audio=chunk,
                sample_rate_hertz=self.AUDIO_RATE,
                language="pt"
            )
            return tr.text.lower().strip()
        except Exception as e:
            print("STT erro:",e)
            return ""

    def _listen_loop(self,callback_ui):
        while self.running:
            chunk=self.audio_q.get()
            if not chunk: continue
            txt=self._transcribe_chunk(chunk)
            if not txt: continue
            callback_ui(f"Você: {txt}")
            if self.WAKE_WORD in txt:
                prompt=txt.split(self.WAKE_WORD,1)[1].strip()
                if not prompt: continue
                result=self._process_text(prompt)
                callback_ui(f"Jarvis: {result}")
                self._speech(result)

    def start(self,callback_ui=lambda x: print(x)):
        if self.running: return
        self.running=True
        self.stream=self.pa.open(format=pyaudio.paInt16,channels=1,rate=self.AUDIO_RATE,
                                 input=True,frames_per_buffer=1024,
                                 stream_callback=lambda in_data,*_: (self.audio_q.put(in_data),None)[1])
        threading.Thread(target=self._listen_loop,args=(callback_ui,),daemon=True).start()

    def stop(self):
        if not self.running: return
        self.running=False
        if self.stream: self.stream.stop_stream(); self.stream.close()
        self.pa.terminate()
