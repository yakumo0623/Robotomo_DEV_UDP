from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json
import re
import time
import threading
from status import get_status, set_status
import socket

class VoskRecognizer:
    def __init__(self, q_in, q_out):
        self.samplerate = 16000
        self.model = Model(lang="ja")
        self.recognizer = KaldiRecognizer(self.model, self.samplerate)
        self.q_in = q_in
        self.q_out = q_out
<<<<<<< HEAD
        self.udpIP = "0.0.0.0"
        self.udpPort = 3333
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udpIP, self.udpPort))
=======
>>>>>>> cdd3dcca7f4b302a7cab16bc34b68b67f4a0b503
        self.t = threading.Thread(target=self.recognize)
        self.t.start()

    def __del__(self):
        self.t.join()

    def callback(self, indata, frames, time, status):
        if get_status() == "idle":
            self.q_in.put(bytes(indata))

    def edit(self, text):
        text = re.sub(r"^(えーっと|えっとー|えーと|えっと|ん|あー|いー|うー|えー)。*", "", text)
        text = re.sub(r" ", "", text)
        return text

    def recognize(self):
        while True:
            start_time = time.time()
            data, addr = self.sock.recvfrom(1024)
            if get_status() == "busy":
                continue
            if self.recognizer.AcceptWaveform(data):
                set_status("busy")
                text = json.loads(self.recognizer.Result()).get('text', '')
                text = self.edit(text)
                if text:
                    print(f'音声認識： {text}({f"{time.time() - start_time:.1f}"} 秒)')
                    self.q_out.put(text)
                else:
                    set_status("idle")
