from os import environ
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.errors import InvalidId
from dotenv import load_dotenv

load_dotenv(".env")

client = MongoClient(
    environ["MONGODB_HOSTNAME"], 
    int(environ["MONGODB_PORT"])
)

db = client.spotify_collections
print("Database connection established.")


def get_collections():
    collections = list(db.collections.find())
    return collections


def get_collection_by_id(id: str):
    try:
        collection = db.collections.find_one({"_id": id})
        return collection
    except InvalidId as _:
        return None


def get_collections_by_name(name: str):
    name = "".join(char if char not in [" ", "-", "_", "//"] else "." for char in name)
    query = { "name": { "$regex": name, "$options": "i" }}
    projection = { "name": 1 }
    # print(query, projection)
    collections = db.collections.find(query, projection)
    return list(collections)


def get_music_by_collection_name(name: str):
    pass


def get_album_by_id(id: str):
    try:
        album = db.albums.find_one({"_id": id})
        return album
    except InvalidId as _:
        return None


def get_albums():
    albums = list(db.albums.find())
    return albums


"""
Creates new music collections in database
Returns the inserted collection (not only the id)
"""
def create_collection(collection: dict):
    new_collection_id = db.collections.insert_one(collection).inserted_id
    new_collection = get_collection_by_id(new_collection_id)
    return new_collection


"""
Creates new album in database
Returns the inserted album (not only the id)
"""
def create_album(album: dict):
    new_album_id = db.albums.insert_one(album).inserted_id
    new_album = get_album_by_id(new_album_id)
    return new_album


def create_song(song: dict):
    new_song = db.songs.insert_one(song).inserted_id
    return new_song


def search_album_by_spotify_id(spotify_id):
    album = db.albums.find_one({"spotify_id": spotify_id})
    return album


def update_album(id: str, album_data: dict):
    result = db.albums.update_one(
        {"_id": id}, 
        {"$set": album_data}
    )
    if not result or result.matched_count == 0:
        return None
    
    updated_album = get_album_by_id(id)
    return updated_album
    

"""
Adds an album to an existing music collection
MongoDB's "addToSet" ensures that there are no duplicate items using exact match comparison
Additional check for practicing and testing purposes only
"""
def add_album_to_collection(collection_id: str, album: dict):
    duplicate_album = db.collections.find_one({"albums.spotify_id": album["spotify_id"]})
    if duplicate_album:
        return None
    update_result = db.collections.update_one(
        { "_id": collection_id },
        { "$addToSet": { "albums": album } }
    )
    return update_result.modified_count