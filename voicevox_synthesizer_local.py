import requests
import json
import pyaudio
import time
import threading
import wave
import io
import status
import socket

class VoiceVoxSynthesizerLocal:
    def __init__(self, q_in, q_out):
        self.host = "192.168.2.107"
        self.port = 50021
        self.speaker = 0
        self.url1 = f"http://{self.host}:{self.port}/audio_query"
        self.url2 = f"http://{self.host}:{self.port}/synthesis"
        self.rate = 24000
        self.chunk = 512
        self.q_in = q_in
        self.q_out = q_out
        self.udpPort = 4444
        self.t1 = threading.Thread(target=self.synthesize)
        self.t2 = threading.Thread(target=self.play)
        self.t1.start()
        self.t2.start()

    def __del__(self):
        self.t1.join()
        self.t2.join()

    def synthesize(self):
        while True:
            text = self.q_in.get()
            start_time = time.time()
            params = (('text', text), ('speaker', self.speaker))
            query = requests.post(self.url1, params=params)
            synthesis = requests.post(self.url2, headers={"Content-Type": "application/json"}, params=params, data=json.dumps(query.json()))
            print(f'音声合成： {text}({f"{time.time() - start_time:.1f}"} 秒)')
            self.q_out.put(synthesis.content)

    def play(self):
        cnt = 0
        while True:
            try:
                voice = self.q_out.get()
                wv = wave.open(io.BytesIO(voice))
                audio = pyaudio.PyAudio()
                stream = audio.open(format=pyaudio.paInt16, channels=1, rate=self.rate, output=True)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((status.get_ip(), self.udpPort))
                data = wv.readframes(self.chunk)
                while data:
                    # stream.write(data)
                    sock.send(data)
                    cnt += 1
                    if cnt == 100:
                        time.sleep(1)
                        cnt = 0
                    data = wv.readframes(self.chunk)
                time.sleep(0.2)
                stream.stop_stream()
                stream.close()
                audio.terminate()
                sock.close()
                if self.q_out.empty():
                    status.set_status("idle")
            except Exception as e:
                print(e)
                status.set_status("idle")
