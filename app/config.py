import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/quarry_crusade")
MAP_DEFAULT_CENTER = [63.4305, 10.3951]
MAP_DEFAULT_ZOOM = 13
