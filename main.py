import os
import uvicorn
import db
import spotify
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional, List
from models import SongModel, RecordModel, CollectionModel


app = FastAPI(title="SpotifyCollections App")


@app.get("/")
async def root():
    return {"message": "SpotifyCollections App!"}


@app.get("/spotify/saved_records")
async def saved_records():
    records = spotify.saved_records()
    return JSONResponse(content=records)


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


@app.post("/records/add", response_description="Add new record", response_model=RecordModel)
async def create_album(record: RecordModel = Body(...)):
    record = jsonable_encoder(record)
    new_record = db.create_record(record)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_record)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)