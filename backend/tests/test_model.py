import os
from src.model.model import continue_playlist
import pytest


def test_continue_playlist_no_input():
    with pytest.raises(ValueError):
        continue_playlist([])


def test_continue_playlist_valid_input():
    
    docker = os.environ.get("USING_DOCKER")
    if type(docker) == str and docker.lower() == 'true':
        my_uris = ["spotify:track:3QxXDiGzAb3SwB2ePuOiSw",
                   "spotify:track:1zUpNXz22EFtljQX3WPDzQ",
                   "spotify:track:5jEolaMASTe1FyYMUf8ulk",
                   "spotify:track:0dNiLb9FEHrRK7VFDJctiR",
                   "spotify:track:5TDEIDElkU2hrMnusjPLNu"]
        ret = continue_playlist(my_uris)
        for uri in ret:
            assert (uri.startswith("spotify:track:"))
        assert (len(ret) == 10)
