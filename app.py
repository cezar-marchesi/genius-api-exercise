from uuid import uuid4
from models import ArtistSongs
from flask import Flask
from config import Configuration
from genius_api_requests import GeniusApiRequests
from redis_connection import RedisConnection
from dynamodb_connection import Boto3Connection


app = Flask(__name__)
redis_client = RedisConnection()
db = Boto3Connection()
db.create_artist_table()

@app.route("/genius/<artist_name>/cache=", defaults={'cache': True})
@app.route("/genius/<artist_name>/cache=<cache>")
def get_songs(artist_name, cache):
    
    if cache is True:
        cached_artist = redis_client.get_cache(artist_name.lower())
        if cached_artist is None:
            artist = GeniusApiRequests().get_artist_songs(artist_name=artist_name)
            if artist:        
                redis_client.set_cache(key=artist_name.lower(), data=artist.dict())
                redis_client.set_expiration(key=artist_name.lower())
                print('from api')
            else:
                return "<h1>Artist not found</h1>"
        else:
            artist = ArtistSongs(
                id=cached_artist['id'],
                artist=cached_artist['artist'],
                most_popular_songs=cached_artist['most_popular_songs']
            )
            print("from cache")            
    
    else:        
        artist = GeniusApiRequests().get_artist_songs(artist_name=artist_name)
        if artist:
            redis_client.delete_cache(artist_name.lower())
            redis_client.set_cache(key=artist_name.lower(), data=artist.dict())
            redis_client.set_expiration(key=artist_name.lower())   
        else:
            return "<h1>Artist not found</h1>"


    db.put_artist(artist, cache)
    return artist.dict()


@app.errorhandler(404)
def error(e):
    return "<h1>Oops, something went wrong</h1>", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=7007)