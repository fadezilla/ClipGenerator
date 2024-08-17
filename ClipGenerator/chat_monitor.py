import websocket
import threading
import time
import json
import os
from auth import load_tokens, refresh_access_token, save_tokens

def on_message(ws, message):
    print("Received raw message:", message)
    try:
        parts = message.split(" :", 1)
        if len(parts) > 1:
            metadata_part, message_part = parts
            # Further processing to extract more details if necessary
            metadata_fields = metadata_part.split(';')
            metadata = {field.split('=')[0]: field.split('=')[1] if '=' in field else None for field in metadata_fields}
            print("User:", metadata.get('display-name'))
            print("Message:", metadata.get('display-name'), message_part)
    except Exception as e:
        print(f"Error parsing message: {e}")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket closed with status {close_status_code}, message: {close_msg}")
    try:
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        _, refresh_token = load_tokens() 
        access_token, new_refresh_token = refresh_access_token(refresh_token, client_id, client_secret)
        save_tokens(access_token, new_refresh_token) 
        attempt_reconnect(access_token)
    except Exception as e:
        print(f"Failed to load or refresh tokens: {e}")

def on_open(ws, access_token):
    def run(*args):
        ws.send("CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership")
        ws.send(f"PASS oauth:{access_token}")
        ws.send("NICK fadezilla")
        ws.send("JOIN #naowh")
        while True:
            time.sleep(1)
    threading.Thread(target=run).start()

def create_and_run_websocket(access_token):
    ws = websocket.WebSocketApp("wss://irc-ws.chat.twitch.tv:443",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=lambda ws: on_open(ws, access_token))
    ws.run_forever()  
def attempt_reconnect(access_token):
    MAX_RECONNECT_ATTEMPTS = 5
    reconnect_attempts = 0
    while reconnect_attempts < MAX_RECONNECT_ATTEMPTS:
        try:
            print(f"Attempting to reconnect, attempt {reconnect_attempts + 1}")
            create_and_run_websocket(access_token)
            print("Reconnected to WebSocket.")
            break
        except Exception as e:
            print(f"Reconnect attempt failed: {e}")
            reconnect_attempts += 1
            time.sleep(10)
        if reconnect_attempts >= MAX_RECONNECT_ATTEMPTS:
            print("Failed to reconnect after several attempts.")

def start_chat_monitor(streamer_name, access_token):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://irc-ws.chat.twitch.tv:443",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=lambda ws: on_open(ws, access_token))
                                

    wst = threading.Thread(target=lambda: ws.run_forever())
    wst.daemon = True
    wst.start()
