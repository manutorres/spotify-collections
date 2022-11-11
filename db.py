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

def create_record(record: dict):
    new_record = db.records.insert_one(record).inserted_id
    return new_record
