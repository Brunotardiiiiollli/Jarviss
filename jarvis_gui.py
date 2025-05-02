
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from jarvis_core import JarvisAssistant
import threading, sys

class JarvisApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jarvis Assistant")
        self.geometry("600x400")
        self.assistant = JarvisAssistant()

        self.text_area = ScrolledText(self, state='disabled', wrap='word')
        self.text_area.pack(expand=True, fill='both', padx=10, pady=10)

        self.btn_frame = tk.Frame(self)
        self.btn_frame.pack(pady=5)
        self.start_btn = tk.Button(self.btn_frame, text="Iniciar Jarvis", command=self.start)
        self.start_btn.pack(side='left', padx=5)
        self.stop_btn = tk.Button(self.btn_frame, text="Parar", command=self.stop, state='disabled')
        self.stop_btn.pack(side='left', padx=5)

    def log(self, message):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.configure(state='disabled')
        self.text_area.yview(tk.END)

    def start(self):
        self.start_btn.config(state='disabled'); self.stop_btn.config(state='normal')
        threading.Thread(target=self.assistant.start, args=(self.log,), daemon=True).start()
        self.log("Jarvis iniciado. Diga '" + self.assistant.WAKE_WORD + "'...")

    def stop(self):
        self.assistant.stop()
        self.log("Jarvis parado.")
        self.start_btn.config(state='normal'); self.stop_btn.config(state='disabled')

if __name__ == "__main__":
    app = JarvisApp()
    app.mainloop()
