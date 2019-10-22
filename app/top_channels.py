import os
import json
import requests

def top_channels(limit=50):
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': os.environ['CLIENT_ID']
    }

    response = requests.get(f'https://api.twitch.tv/kraken/streams?limit={limit}', headers=headers)
    data = json.loads(response.text).get('streams', [])

    return set([n['channel']['name'] for n in data])
