from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from bson import ObjectId


"""
convert ObjectIds to strings before storing them as the _id.
"""
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid Objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class SongModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    artist: str = Field(...)
    
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "In your own sweet way",                
                "artist": "Wes Montgomery"
            }
        }

class RecordModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    artist: str = Field(...)
    
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Tore Down House",                
                "artist": "Scott Henderson"                
            }
        }


class CollectionModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    description: str = Field(...)
    type: Optional[str]
    aliases: Optional[list[str]]
    records: Optional[list[RecordModel]]
    songs: Optional[list[SongModel]]
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "guitar jazz",
                "type": "genre",
                "description": "Jazz music with prevalence of electric guitar playing",
                "aliases": ["guitar-jazz", "jazz guitar", "jazz-guitar"],
                "records": [
                    {
                        "_id": "ObjectId(...)",
                        "name": "Talk to Your Daughter",
                        "artist": "Robben Ford"
                    }
                ],
                "songs": [
                    {
                        "_id": "ObjectId(...)",
                        "name": "Bright Size Life",
                        "artist": "Pat Metheny"
                    }
                ]
            }
        }


