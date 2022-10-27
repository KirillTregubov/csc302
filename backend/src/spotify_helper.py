import json
from typing import Optional, List
import requests
import os


def get_access_token() -> Optional[str]:
    response = requests.post("https://accounts.spotify.com/api/token", {
        "grant_type": "client_credentials",
        "client_id": os.environ.get("CLIENT_ID"),
        "client_secret": os.environ.get("CLIENT_SECRET"),
    })

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        return None


def get_tracks(tracks) -> List[str]:
    # tracks = json.loads(input)
    result = []
    for track in tracks:
        images = track["album"]["images"]
        # last image is the largest one
        image_url = None if len(images) == 0 else images[-1]["url"]
        result.append({
            "name": track["name"],
            "artists": list(map(lambda artist: artist["name"], track["artists"])),
            "image_url": image_url,
            "uri": track["uri"],
            "explicit": track["explicit"]
        })
    return result
