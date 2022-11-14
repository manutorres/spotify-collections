import os
import uvicorn
import db
import spotify
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from models import SongModel, AlbumModel, CollectionModel


app = FastAPI(title="SpotifyCollections App")


@app.get("/")
async def root():
    return {"message": "SpotifyCollections App!"}


@app.get("/spotify/saved_albums")
async def get_spotify_saved_albums():
    albums = spotify.get_saved_albums()
    return JSONResponse(content=albums)


@app.get("/spotify/search_albums")
async def get_spotify_search_albums(query: str):
    albums = spotify.get_search_albums(query)
    return JSONResponse(content=albums)


@app.post("/collections/add", response_description="Add new collection", response_model=CollectionModel)
async def create_collection(collection: CollectionModel = Body(...)):
    collection = jsonable_encoder(collection)
    new_collection = db.create_collection(collection)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_collection)


@app.post("/songs/add", response_description="Add new song", response_model=SongModel)
async def create_album(song: SongModel = Body(...)):
    song = jsonable_encoder(song)
    new_song = db.create_song(song)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_song)


# Creates new album in database from user input data
@app.post("/albums/add", response_description="Add new album", response_model=AlbumModel)
async def create_album(album: AlbumModel = Body(...)):
    album = jsonable_encoder(album)
    new_album = db.create_album(album)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_album)


@app.put("/collections/{collection_id}/add_album/{spotify_id}", response_description="Add album to collection")
async def add_album_to_collection(collection_id: str, spotify_id: str):
    album = db.search_album_by_spotify_id(spotify_id)
    if not album:
        album = spotify.get_album(spotify_id)
        album = jsonable_encoder(album)
        new_album = db.create_album(album)
    modified_count = db.add_album_to_collection(collection_id, album)
    return JSONResponse(status_code=status.HTTP_200_OK, content=modified_count)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)