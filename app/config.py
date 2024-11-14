import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/quarry_crusade")
MAP_DEFAULT_CENTER = [40.604925, -89.480311]
MAP_DEFAULT_ZOOM = 15