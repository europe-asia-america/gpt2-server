from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json
import gpt_2_simple as gpt2
import os
import requests

model_name = "124M"
if not os.path.isdir(os.path.join("models", model_name)):
	print(f"Downloading {model_name} model...")
	gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/

sess = gpt2.start_tf_sess()

def prompt_text(input: str) -> str:
    text = gpt2.generate(sess, prefix=input)
    text = text.split()
    text = text[:2]
    text = ' '.join(text)
    return text

def prediction(string: str):
    return {
        "message": {
            "prompt": string,
            "text_0": prompt_text(string),
            "text_1": "Today, I saw potato in the fields.",
            "text_2": "! Our crops are growing.",
            "text_3": "How will we drink coffee tomorrow?",
        }
    }

clients = []

class Prediction(WebSocket):
    def handleMessage(self):
        self.sendMessage(json.dumps(prediction(self.data)))

    def handleConnected(self):
        print (self.address, 'connected')
        for client in clients:
            client.sendMessage(self.address[0] + u' - connected :)')
        clients.append(self)


    def handleClose(self):
        clients.remove(self)
        print (self.address, 'closed')
        for client in clients:
            client.sendMessage(self.address[0] + u' - disconnected :(')


server = SimpleWebSocketServer('', 8008, Prediction)
server.serveforever()