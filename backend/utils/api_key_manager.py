import os
import redis
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read API keys from .env (comma-separated)
API_KEYS = os.getenv("API_KEYS")
if not API_KEYS:
    raise Exception("API_KEYS not found in .env file. Please add API_KEYS=key1,key2,key3,key4")
api_keys_list = [k.strip() for k in API_KEYS.split(",") if k.strip()]

# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.Redis.from_url(REDIS_URL)
REDIS_LIST_NAME = "api_keys"

# Initialize the Redis list if not already present
if r.llen(REDIS_LIST_NAME) == 0:
    r.delete(REDIS_LIST_NAME)
    r.rpush(REDIS_LIST_NAME, *api_keys_list)

def get_next_api_key():
    """
    Pops the least recently used API key from the front, pushes it to the end, and returns it.
    """
    key = r.lpop(REDIS_LIST_NAME)
    if key is not None:
        r.rpush(REDIS_LIST_NAME, key)
        return key.decode() if isinstance(key, bytes) else key
    else:
        raise Exception("No API keys available in Redis list.")

# Sample usage
if __name__ == "__main__":
    print("Current API keys order:", [k.decode() for k in r.lrange(REDIS_LIST_NAME, 0, -1)])
    key = get_next_api_key()
    print("Using API key:", key)
    print("New API keys order:", [k.decode() for k in r.lrange(REDIS_LIST_NAME, 0, -1)])
