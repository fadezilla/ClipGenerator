import requests
import json

def get_app_access_token(client_id, client_secret):
    """Fetches an application access token using client credentials."""
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=params)
    response.raise_for_status()
    return response.json()['access_token']

def exchange_code_for_token(client_id, client_secret, code, redirect_uri):
    """Exchanges an authorization code for an access token."""
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri
    }
    response = requests.post(url, data=params)
    response.raise_for_status()  # This will raise an exception for HTTP request errors
    data = response.json()
    access_token = data['access_token']
    refresh_token = data.get('refresh_token', '')  # Sometimes refresh_token might be absent
    return access_token, refresh_token

def refresh_access_token(refresh_token, client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, data=params)
    response.raise_for_status()
    data = response.json()
    return data['access_token'], data.get('refresh_token', refresh_token)

def save_tokens(access_token, refresh_token):
    with open('tokens.json', 'w') as token_file:
        json.dump({'access_token': access_token, 'refresh_token': refresh_token}, token_file)

def load_tokens():
    with open('tokens.json', 'r') as token_file:
        tokens = json.load(token_file)
    return tokens['access_token'], tokens['refresh_token']
