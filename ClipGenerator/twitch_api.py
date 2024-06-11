import requests

def check_stream_status(client_id, access_token, streamer_name):
    """Checks if a streamer is live by querying the Twitch API."""
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(f'https://api.twitch.tv/helix/streams?user_login={streamer_name}', headers=headers)
    response.raise_for_status()
    data = response.json()
    return data['data'][0]['type'] == 'live' if data['data'] else False
