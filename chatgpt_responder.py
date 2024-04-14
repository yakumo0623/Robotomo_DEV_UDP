import openai
import threading
import time
import os

class ChatGPTResponder:
    def __init__(self, q_in, q_out):
        self.role = "あなたは、「女子高生のギャル」を演じてください。"
        self.role += "一人称は、「わたし」、二人称は、「あなた」です。"
        self.role += "５０文字以内で会話が継続できるような応答をしてください。"
        self.setting = [{"role": "system", "content": self.role}]
        openai.api_key = os.environ["STACK_CHAN_OPENAI"]
        self.chat_history = []
        self.chat_history_count = 10
        self.q_in = q_in
        self.q_out = q_out
        self.t = threading.Thread(target=self.respond)
        self.t.start()

    def __del__(self):
        self.t.join()

    def respond(self):
        while True:
            text = self.q_in.get()
            self.chat_history.append({"role": "user", "content": text})
            start_time = time.time()

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.setting + self.chat_history,
                stream=True
            )

            full_response = ""
            realtime_response = ""
            for chunk in response:
                text = chunk['choices'][0]['delta'].get('content')

                if(text==None):
                    pass
                else:
                    full_response += text
                    realtime_response += text

                    target_char = ["。", "！", "？", "\n"]
                    for index, char in enumerate(realtime_response):
                        if char in target_char:
                            pos = index + 2
                            sentence = realtime_response[:pos]
                            realtime_response = realtime_response[pos:]
                            print(f'応答文： {sentence}({f"{time.time() - start_time:.1f}"} 秒)')

                            self.q_out.put(sentence)
                            start_time = time.time()
                            break
                        else:
                            pass
            self.chat_history.append({"role": "user", "content": full_response})
            if len(self.chat_history) >= self.chat_history_count:
                del self.chat_history[:2]
                print(f'チャット履歴： 2件削除')
