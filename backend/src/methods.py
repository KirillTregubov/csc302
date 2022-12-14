import requests
import logging
from flask import Response, jsonify, make_response
from typing import Dict, List, Optional
from src.spotify_helper import get_access_token, get_tracks, get_playlist
from src.response_handler import log_error_res
from src.model.model import continue_playlist

top_playlists_cache: Dict[str, Dict] = {}


def recommend_tracks(track_uris: List[str]) -> Response:
    """
    Get recommended tracks for a list of track uris

    Preconditions:
    - track_uris is a list containing >= 1 "track_uris"
    Postconditions:
    - returns a list of <= 1000 recommended "track_uris"
    """
    logging.info(f"recommend_tracks({track_uris})")
    access_token = get_access_token()
    if access_token is None:
        return make_response(jsonify([]), 401)  # unauthorized

    recommended_track_uris = __recommend_using_ml(track_uris, 2)

    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"ids": ",".join(recommended_track_uris)}
    response = requests.get(
        "https://api.spotify.com/v1/tracks", headers=headers, params=params)

    tracks = []
    if response.status_code == 200:
        tracks = get_tracks(response.json()["tracks"])
    else:
        log_error_res(response, "GET")

    ret_res = make_response(jsonify(tracks), response.status_code)
    ret_res.headers["Content-Type"] = "application/json"
    return ret_res


def get_playlist_recommendations(playlist_id: str) -> Response:
    """
    Get the tracks of the playlist with the given playlist_id.

    Preconditions:
    - None
    Postconditions:
    - Returns a response with the tracks of the playlist with the given playlist_id.
        - Structure of the response JSON: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlists-tracks
        - If the request succeeds, the response contains a list of data.
        - If the request fails, the response contains an empty list and a corresponding error status_code.
    """
    access_token = get_access_token()
    if access_token is None:
        return make_response(jsonify([]), 401)

    data = []
    playlist = __get_playlist(playlist_id, access_token)
    if playlist is not None:
        data.append(playlist["tracks"])
    
    recommended_track_uris = __recommend_using_ml(data, 2)

    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"ids": ",".join(recommended_track_uris)}
    response = requests.get(
        "https://api.spotify.com/v1/tracks", headers=headers, params=params)

    tracks = []
    if response.status_code == 200:
        tracks = get_tracks(response.json()["tracks"])
    else:
        log_error_res(response, "GET")

    ret_res = make_response(jsonify(tracks), response.status_code)
    ret_res.headers["Content-Type"] = "application/json"
    return ret_res


def __recommend_using_ml(track_uris: List[str], max_ml_calls: Optional[int]) -> List[str]:
    """
    Return a list of track_uris recommended by the ML model given the input "track_uris".
    The ML model will be called a maximum of "max_ml_calls" times. If this value is None, the
    maximum allowed ML model calls of 100 will be used (not recommended).

    Preconditions:
    - max_ml_calls is None or 0 < max_ml_calls <= 100
    Postconditions:
    - returns a list of len <= 1000
    """
    segmented = __segment_list(track_uris, 10)
    if len(segmented) == 0:
        return []
    recommended = []
    num_loops = min(len(segmented), 100 if max_ml_calls is None else max_ml_calls)
    for i in range(num_loops):
        recommended.extend([uri.replace("spotify:track:", "") for uri in continue_playlist(segmented[i])])
    print('='*20, recommended, flush=True)
    return recommended


def __segment_list(lst: List, length: int) -> List[List]:
    """
    Segment the given lst into nested lists each with at most "length" elements. Each nested list
    will have "length" elements EXCEPT for the last one which will have the left over len(lst) % length
    elements. If "length" divides len(lst), then the last nested list will also have "length" elements.

    Preconditions:
    - length >= 1
    Postconditions:
    - If len(lst) % length == 0, each nested list in the returned list will have "length" elements.
      Otherwise, the last nested list in the returned list has len == len(lst) % length while
      every other list has "length" elements.
    """
    segmented = []
    current = []
    for item in lst:
        current.append(item)
        if (len(current) == length):
            segmented.append(current)
            current = []
    if len(current) > 0:
        segmented.append(current)
    return segmented


def search_tracks(query: str) -> Response:
    logging.info(f"search_tracks({query})")
    access_token = get_access_token()
    if access_token is None:
        return make_response(jsonify([]), 401)  # unauthorized

    headers = {"Authorization": f"Bearer {access_token}"}

    if len(query) == 0:
        # TODO: get list of 10 songs we want to show by default
        # params = {"type": "track", "limit": 10}
        return make_response(jsonify([]), 200)
    params = {"q": query, "type": "track", "limit": 10}
    response = requests.get(
        "https://api.spotify.com/v1/search", headers=headers, params=params)

    tracks = []
    if response.status_code == 200:
        tracks = get_tracks(response.json()["tracks"]["items"])
    else:
        log_error_res(response, "GET")

    ret_res = make_response(jsonify(tracks), response.status_code)
    ret_res.headers["Content-Type"] = "application/json"
    return ret_res


def search_playlist(query: str) -> Response:
    logging.info(f"search_playlist({query})")
    access_token = get_access_token()
    if access_token is None:
        return make_response(jsonify([]), 401)  # unauthorized

    headers = {"Authorization": f"Bearer {access_token}"}

    if len(query) == 0:
        return make_response(jsonify([]), 200)
    params = {"q": query, "type": "playlist", "limit": 10}
    response = requests.get(
        "https://api.spotify.com/v1/search", headers=headers, params=params)

    playlists = []
    if response.status_code == 200:
        for item in response.json()["playlists"]["items"]:
            playlists.append(get_playlist(item, True))
    else:
        log_error_res(response, "GET")

    ret_res = make_response(jsonify(playlists), response.status_code)
    ret_res.headers["Content-Type"] = "application/json"
    return ret_res


def get_general_info(track_uris: List[str]) -> Response:
    """
    Get general information about tracks with the given track_uris.

    Preconditions:
    - 0 <= len(track_uris) <= 50
    Postconditions:
    - Returns a response with general track info.
        - Structure of the response JSON: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-tracks
        - If the request succeeds, the response contains a list of data with length == len(track_uris).
        - If the request fails, the response contains an empty list and a corresponding error status_code.
    """
    logging.info(f"get_general_info({track_uris})")
    access_token = get_access_token()
    if access_token is None:
        return make_response(jsonify([]), 401)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"ids": ",".join(track_uris)}
    response = requests.get("https://api.spotify.com/v1/tracks", headers=headers, params=params)
    
    tracks = []
    if response.status_code == 200:
        tracks = response.json()["tracks"]
    else:
        log_error_res(response, "GET")

    ret_res = make_response(jsonify(tracks),response.status_code)
    ret_res.headers["Content-Type"] = "application/json"
    return ret_res


def get_audio_features(track_uris: List[str]) -> Response:
    """
    Get audio features of the tracks with the given track_uris.

    Preconditions:
    - 0 <= len(track_uris) <= 100
    Postconditions:
    - Returns a response with track audio features.
        - Structure of the response JSON: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-audio-features
        - If the request succeeds, the response contains a list of data with length == len(track_uris).
        - If the request fails, the response contains an empty list and a corresponding error status_code.
    """
    logging.info(f"get_audio_features({track_uris})")
    access_token = get_access_token()
    if access_token is None:
        return make_response(jsonify([]), 401)
    
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"ids": ",".join(track_uris)}
    response = requests.get("https://api.spotify.com/v1/audio-features", headers=headers, params=params)

    audio_features = []
    if response.status_code == 200:
        audio_features = response.json()["audio_features"]
    else:
        log_error_res(response, "GET")

    ret_res = make_response(jsonify(audio_features),response.status_code)
    ret_res.headers["Content-Type"] = "application/json"
    return ret_res


def get_top_playlists() -> Response:
    """
    Get the top playlists of the user.

    Preconditions:
    - None
    Postconditions:
    - Returns a response with the top playlists of the user.
        - Structure of the response JSON: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlist
        - If the request succeeds, the response contains a list of data.
        - If the request fails, the response contains an empty list and a corresponding error status_code.
    """
    access_token = get_access_token()
    if access_token is None:
        return make_response(jsonify([]), 401)

    data = []
    for playlist_id in ['37i9dQZF1DXcBWIGoYBM5M', '37i9dQZEVXbMDoHDwVN2tF', '37i9dQZF1DX0XUsuxWHRQd', '37i9dQZF1DX10zKzsJ2jva', '37i9dQZF1DWY7IeIP1cdjF', '37i9dQZF1DWXRqgorJj26U', '37i9dQZF1DX4o1oenSJRJd', '37i9dQZF1DX4UtSsGT1Sbe']:
        playlist = __get_playlist(playlist_id, access_token)
        playlist.pop("tracks")
        if playlist is not None:
            data.append(playlist)

    # Spotify's top playlists should never be empty. If it is empty, then something went wrong with all
    # of our requests to the Spotify API.
    status_code = 500 if len(data) == 0 else 200

    ret_res = make_response(jsonify(data), status_code)
    ret_res.headers["Content-Type"] = "application/json"
    return ret_res


def get_playlist_data(playlist_id: str):
    access_token = get_access_token()
    if access_token is None:
        return make_response(jsonify([]), 401)

    playlist = __get_playlist(playlist_id, access_token)
    track_ids: List[str] = playlist["tracks"]

    #
    audio_features = []
    for ids in __segment_list(track_ids, 100):
        res = get_audio_features(ids)
        if res.status_code != 200:
            return make_response(jsonify([]), res.status_code)
        audio_features.extend(res.json)
    audio_features.sort(key=condition_by_id)
    
    general_info = []
    for ids in __segment_list(track_ids, 50):
        res = get_general_info(ids)
        if res.status_code != 200:
            return make_response(jsonify([]), res.status_code)
        general_info.extend(res.json)
    general_info.sort(key=condition_by_id)

    track_data = []
    for i in range(len(audio_features)):
        track_data.append({
            "audio_features": audio_features[i],
            "general_info": general_info[i]
        })
    
    return make_response(jsonify({"tracks": track_data, "playlist": playlist}), 200)


def condition_by_id(data):
    return data["id"]


def __get_playlist(id: str, access_token: str) -> Optional[Dict]:
    """
    Return the playlist object associated with the given "id" from the playlist cache. If said
    playlist doesn't exist in the cache, fetch it from Spotify and add it to the cache. If something
    goes wrong with the fetch request, return None.
    
    "access_token" is used to authorize the fetch request from Spotify.
    """
    cached = top_playlists_cache.get(id)
    if cached is None:
        response = requests.get(f"https://api.spotify.com/v1/playlists/{id}", headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code == 200:
            new_playlist = get_playlist(response.json())
            top_playlists_cache[id] = new_playlist
            return new_playlist.copy()
        else:
            # TODO: do error logging here
            return None
    else:
        return cached.copy()
