import os
import uvicorn
import db
import spotify
import youtube
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from models import SongModel, AlbumModel, CollectionModel


app = FastAPI(title="SpotifyCollections App")


@app.get("/")
def root():
    return {"message": "SpotifyCollections App!"}


"""
Creates a new collection in database from user input data and returns it
"""
@app.post("/collections/add", response_description="Add new collection", response_model=CollectionModel)
def create_collection(collection: CollectionModel = Body(...)):
    collection = jsonable_encoder(collection)
    new_collection = db.create_collection(collection)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_collection)


"""
Creates a new album in database from user input data and returns it
"""
@app.post("/albums/add", response_description="Add new album", response_model=AlbumModel)
def create_album(album: AlbumModel = Body(...)):
    if not album.youtube_link:
        link = youtube.get_album_link(album.name)
        album.youtube_link = link if link else None
    album = jsonable_encoder(album)
    new_album = db.create_album(album)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_album)


"""
Creates a new song in database from user input data and returns it
"""
@app.post("/songs/add", response_description="Add new song", response_model=SongModel)
def create_song(song: SongModel = Body(...)):
    song = jsonable_encoder(song)
    new_song = db.create_song(song)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_song)


"""
Lists all collections from database
"""
@app.get("/collections", response_description="List all collections", response_model=List[CollectionModel])
def get_collections():
    collections = db.get_collections()
    return JSONResponse(content=collections)


"""
Lists collections that match the given name
"""
@app.get("/collections/match_name/{name}", response_description="Matching collections", response_model=List[CollectionModel])
def get_collections_by_name(name: str):
    collections = db.get_collections_by_name(name)
    if collections:
        return JSONResponse(content=collections)
    else:
        raise HTTPException(status_code=404, detail=f"Collections matching '{name}' not found")


"""
Lists all albums from database
"""
@app.get("/albums", response_description="List all albums", response_model=List[AlbumModel])
def get_albums():
    albums = db.get_albums()
    return JSONResponse(content=albums)


"""
Lists all Spotify albums present in the user's library
"""
@app.get("/spotify/saved_albums")
def get_spotify_saved_albums():
    albums = spotify.get_saved_albums()
    return JSONResponse(content=albums)


"""
Lists albums that match the given name from Spotify catalogue
"""
@app.get("/spotify/search_albums/{name}")
def get_spotify_search_albums(name: str):
    albums = spotify.get_search_albums(name)
    return JSONResponse(content=albums)


"""
Plays the album in available platform
"""
@app.get("/albums/play/{id}")
def play_album(id: str):
    album = db.get_album_by_id(id)
    if spotify.play_album(album["spotify_id"]):
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"Album {id} played in Spotify")
    
    youtube_link = album["youtube_link"]
    if youtube_link:
        youtube.play_video(youtube_link)
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"Album {id} played in Youtube")
    
    raise HTTPException(status_code=404, detail=f"Album '{id}' could not be played")


"""
Adds album with the given spotify_id to the specified collection
The album is also stored in database if not already present
"""
@app.put("/collections/{collection_id}/add_album/{spotify_id}", response_description="Add album to collection", response_model=str)
def add_album_to_collection(collection_id: str, spotify_id: str):
    album = db.search_album_by_spotify_id(spotify_id)
    if not album:
        album = spotify.get_album(spotify_id)
        link = youtube.get_album_link(album.name)
        album.youtube_link = link if link else None
        album = jsonable_encoder(album)
        _ = db.create_album(album)
   
    modified_count = db.add_album_to_collection(collection_id, album)
    if modified_count:
        return JSONResponse(status_code=status.HTTP_200_OK, content=f"Album {spotify_id} added to the collection")
    else:
        raise HTTPException(status_code=400, detail=f"Album {spotify_id} already in the collection")


"""
Initializes the web server if program run directly
"""
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)