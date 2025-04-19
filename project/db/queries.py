import redis
import json

r = redis.Redis(host='localhost', port=6777, db=0, decode_responses=True)

def store_user_relation(hash_name: str, user_id: int, related_ids: list[int]) -> None:
    value = json.dumps(related_ids)
    r.hset(hash_name, user_id, value)

def get_user_relation(hash_name: str, user_id: int) -> list[int]:
    value = r.hget(hash_name, user_id)
    return json.loads(value) if value else []
