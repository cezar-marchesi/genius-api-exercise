from uuid import uuid4
from config import Configuration
from lyricsgenius import Genius
from models import ArtistSongs


class GeniusApiRequests:
    def __init__(self) -> ArtistSongs:
        self.client_token = Configuration.client_token

    def get_artist_songs(self, artist_name: str):
        genius = Genius(access_token=self.client_token)
        result = genius.search_artist(
            artist_name=artist_name,
            max_songs=2,
            sort='popularity'
            )

        if result:
            song_list = [song.title for song in result.songs]
            artist = ArtistSongs(
                id=str(uuid4()),
                artist=result.name,
                most_popular_songs=song_list            
            )
        
            return artist
        return None


    