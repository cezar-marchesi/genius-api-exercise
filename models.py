from typing import List
from pydantic import BaseModel

class ArtistSongs(BaseModel):
    id: str
    artist: str
    most_popular_songs: List