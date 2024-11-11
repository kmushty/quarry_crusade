# app/config.py
import os

class Config:
    KEY = os.environ.get("SOME_KEY", "some_key")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:3001/quarry_crusade")

