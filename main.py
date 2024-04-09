import queue
from vosk_recognizer import VoskRecognizer
from chatgpt_responder import ChatGPTResponder
from voicevox_synthesizer_local import VoiceVoxSynthesizerLocal

q_audio_to_text = queue.Queue()     # マイクの音声
q_text_to_gpt = queue.Queue()       # 音声認識したテキスト
q_gpt_to_voicevox = queue.Queue()   # ChatGPTの応答文
q_voicevox_to_play = queue.Queue()  # 音声合成したWAVデータ

vosk_recognizer = VoskRecognizer(q_audio_to_text, q_text_to_gpt)
chatgpt_responder = ChatGPTResponder(q_text_to_gpt, q_gpt_to_voicevox)
voicevox_synthesizer_local = VoiceVoxSynthesizerLocal(q_gpt_to_voicevox, q_voicevox_to_play)
