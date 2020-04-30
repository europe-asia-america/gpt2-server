import asyncio
import websockets
import json

def prediction(string):
    return {
        "message": {
            "prompt": string,
            "text_0": ". I am a test. That's wonderful.",
            "text_1": "Today, I saw potato in the fields.",
            "text_2": "! Our crops are growing.",
            "text_3": "How will we drink coffee tomorrow?",
        }
    }

async def hello(websocket, path):
    while True:
        msg = await websocket.recv()
        await websocket.send(json.dumps(prediction(msg)))

start_server = websockets.serve(hello, "localhost", 8008)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()