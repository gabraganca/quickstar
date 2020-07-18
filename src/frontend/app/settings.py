import os

BACKEND_PORT = os.getenv("BACKEND_PORT", "8000")
BACKEND_URL = os.getenv("BACKEND_URL", "localhost") + ":" + BACKEND_PORT
CACHE_TTL = os.getenv("CACHE_TTL", 24 * 60 * 60)  # 24 hour
