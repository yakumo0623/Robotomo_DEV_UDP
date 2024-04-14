from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json
import re
import time
import threading
import status
import socket

class VoskRecognizer:
    def __init__(self, q_in, q_out, port):
        self.samplerate = 16000
        self.model = Model(lang="ja")
        self.recognizer = KaldiRecognizer(self.model, self.samplerate)
        self.q_in = q_in
        self.q_out = q_out
        self.udpIP = "0.0.0.0"
        self.rxPort = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udpIP, self.rxPort))
        self.t = threading.Thread(target=self.recognize)
        self.t.start()

    def __del__(self):
        self.t.join()

    def callback(self, indata, frames, time, status):
        if status.get_status() == "idle":
            self.q_in.put(bytes(indata))

    def edit(self, text):
        text = re.sub(r"^(えーっと|えっとー|えーと|えっと|ん|あー|いー|うー|えー)。*", "", text)
        text = re.sub(r" ", "", text)
        return text

    def recognize(self):
        while True:
            start_time = time.time()
            data, addr = self.sock.recvfrom(1024)
            if status.get_status() == "busy":
                continue
            if self.recognizer.AcceptWaveform(data):
                status.set_status("busy")
                text = json.loads(self.recognizer.Result()).get('text', '')
                text = self.edit(text)
                if text:
                    print(f'音声認識： {text}({f"{time.time() - start_time:.1f}"} 秒)')
                    self.q_out.put(text)
                    status.set_ip(addr[0])
                else:
                    status.set_status("idle")
