import json
import os
import hashlib

CACHE_FILE = os.path.join("memory", "ai_cache.json")


def ensure_cache_folder():
    os.makedirs("memory", exist_ok=True)


def make_cache_key(prompt: str):
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def load_cache():
    ensure_cache_folder()

    if not os.path.exists(CACHE_FILE):
        return {}

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


def save_cache(cache):
    ensure_cache_folder()

    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(cache, file, indent=2)


def get_cached_response(prompt: str):
    cache = load_cache()
    key = make_cache_key(prompt)

    return cache.get(key)


def set_cached_response(prompt: str, response: dict):
    cache = load_cache()
    key = make_cache_key(prompt)

    cache[key] = response
    save_cache(cache)