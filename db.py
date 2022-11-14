from os import environ
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(".env")

client = MongoClient(
    environ["MONGODB_HOSTNAME"], 
    int(environ["MONGODB_PORT"])
)

db = client.spotify_collections
print("Database connection established.")


def create_collection(collection: dict):
    new_collection = db.collections.insert_one(collection).inserted_id
    return new_collection


def create_song(song: dict):
    new_song = db.songs.insert_one(song).inserted_id
    return new_song


def create_album(album: dict):
    new_album = db.albums.insert_one(album).inserted_id
    return new_album


def search_album_by_spotify_id(spotify_id):
    album = db.albums.find_one({"spotify_id": spotify_id})
    return album


def add_album_to_collection(collection_id: str, album: dict):
    update_result = db.collections.update_one(
        { "_id": collection_id },
        { "$addToSet": { "albums": album } }
    )
    return update_result.modified_count