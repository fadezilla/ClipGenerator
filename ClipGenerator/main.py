from chat_monitor import start_chat_monitor
from auth import load_tokens, refresh_access_token, save_tokens
import os

def run_main(access_token=None):
    if access_token is None:
        access_token, refresh_token = load_tokens()
        access_token, refresh_token = refresh_access_token(refresh_token, os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET'))
        save_tokens(access_token, refresh_token)

    # Example functionality: Start monitoring Twitch chat
    start_chat_monitor('naowh', access_token)

if __name__ == "__main__":
    run_main()