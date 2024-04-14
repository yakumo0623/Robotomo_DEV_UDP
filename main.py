import queue
from vosk_recognizer import VoskRecognizer
from chatgpt_responder import ChatGPTResponder
from voicevox_synthesizer_local import VoiceVoxSynthesizerLocal
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--tx_port', type=int, default=50022, help='tx_port (default: 50022)')  # 相手(送信)のポート
parser.add_argument('--rx_port', type=int, default=50023, help='rx_port (default: 50023)')  # 自分(受信)のポート
args = parser.parse_args()

q_audio_to_text = queue.Queue()     # マイクの音声
q_text_to_gpt = queue.Queue()       # 音声認識したテキスト
q_gpt_to_voicevox = queue.Queue()   # ChatGPTの応答文
q_voicevox_to_play = queue.Queue()  # 音声合成したWAVデータ

vosk_recognizer = VoskRecognizer(q_audio_to_text, q_text_to_gpt, args.rx_port)
chatgpt_responder = ChatGPTResponder(q_text_to_gpt, q_gpt_to_voicevox)
voicevox_synthesizer_local = VoiceVoxSynthesizerLocal(q_gpt_to_voicevox, q_voicevox_to_play, args.tx_port)
