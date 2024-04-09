import requests
import json
import pyaudio
import time
import threading
import wave
import io
from status import get_status, set_status

class VoiceVoxSynthesizerLocal:
    def __init__(self, q_in, q_out):
<<<<<<< HEAD
        self.host = "192.168.2.109"
=======
        self.host = "192.168.2.114"
>>>>>>> cdd3dcca7f4b302a7cab16bc34b68b67f4a0b503
        self.port = 50021
        self.speaker = 0
        self.url1 = f"http://{self.host}:{self.port}/audio_query"
        self.url2 = f"http://{self.host}:{self.port}/synthesis"
        self.rate = 24000
        self.chunk = 1024
        self.q_in = q_in
        self.q_out = q_out
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
        while True:
            voice = self.q_out.get()
            wv = wave.open(io.BytesIO(voice))
            audio = pyaudio.PyAudio()
            stream = audio.open(format=pyaudio.paInt16, channels=1, rate=self.rate, output=True)
            data = wv.readframes(self.chunk)
            while data:
                stream.write(data)
                data = wv.readframes(self.chunk)
            time.sleep(0.2)
            stream.stop_stream()
            stream.close()
            audio.terminate()
            if self.q_out.empty():
                set_status("idle")

