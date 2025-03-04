import os
import json
from typing import Any, Optional

import redis

CLIENT = None

def get_db_client():
    global CLIENT

    if not CLIENT:
        POOL = redis.ConnectionPool.from_url(os.environ.get("REDIS_HOST"))
        CLIENT = redis.Redis(connection_pool=POOL)

    return CLIENT

def set_value(key: str, value: Any, expiry: Optional[int] = None) -> bool:
    """Set a key-value pair in Redis. Supports optional expiration (in seconds)."""
    value_to_store = json.dumps(value) if isinstance(value, (dict, list)) else value
    client = get_db_client()
    return client.set(key, value_to_store, ex=expiry)


def get_value(key: str) -> Optional[Any]:
    """Retrieve a value from Redis, deserializing JSON if needed."""
    client = get_db_client()
    value = client.get(key)

    if value is None:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value
