from inspect import Attribute
from urllib import response
import boto3
from config import Configuration


class Boto3Connection:
    def __init__(self) -> None:
        self.endpoint_url = Configuration.dynamodb_endpoint
        self.aws_access_key_id = Configuration.aws_access_key_id
        self.aws_secret_access_key = Configuration.aws_secret_access_key
        self.ddb = boto3.resource('dynamodb',
                                  endpoint_url=self.endpoint_url,
                                  aws_access_key_id=self.aws_access_key_id,
                                  aws_secret_access_key=self.aws_secret_access_key,
                                  region_name='br')                

    def create_artist_table(self):
        try:
            response = self.ddb.create_table(
                TableName='ArtistSongs',
                KeySchema=[
                    {
                        'AttributeName': 'artist',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'artist',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
            return response
        except Exception as e:
            print(e)

    def put_artist(self, artist, cache_option):
        table = self.ddb.Table('ArtistSongs')
        response = table.put_item(
            Item={
                'artist': artist.artist,
                'cache': cache_option,
                'most_popular_songs': artist.most_popular_songs,
                'id': artist.id
            }
        )
        return response
