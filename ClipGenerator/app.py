from flask import Flask, request, redirect, url_for
from auth import exchange_code_for_token, save_tokens
import os
import threading
import main  # Ensure main.py contains the main function that needs to be run

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome! Click here to <a href="/login">login with Twitch</a>.'

@app.route('/login')
def login():
    client_id = os.getenv('CLIENT_ID')
    redirect_uri = os.getenv('REDIRECT_URI')
    auth_url = f"https://id.twitch.tv/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope=chat:read chat:edit&force_verify=true"
    return redirect(auth_url)

@app.route('/auth/twitch/callback')
def callback():
    code = request.args.get('code')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')
    access_token, refresh_token = exchange_code_for_token(client_id, client_secret, code, redirect_uri)
    save_tokens(access_token, refresh_token)
    threading.Thread(target=main.run_main, args=(access_token,)).start()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=int(os.getenv('SERVER_PORT', 3000)))