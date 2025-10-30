import os

class Config:
    BASE_URL = os.getenv("BASE_URL", "https://api.example.com")
    TIMEOUT = float(os.getenv("TIMEOUT", 10))
    RETRY_COUNT = int(os.getenv("RETRY_COUNT", 2))
    HEADERS = {"User-Agent": "DataHarvester"}
    STREAM_CHUNK_SIZE = int(os.getenv("STREAM_CHUNK_SIZE", "8192"))