import json
import requests
import redis
import websocket
import random,time

ws=websocket.WebSocket()
ws.connect('ws://localhost:8000/ws/polData/')

for i in range(1000):
    time.sleep(3)
    ws.send(json.dumps({'value':random.randint(1,100)}))