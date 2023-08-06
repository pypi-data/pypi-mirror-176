import hashlib
import os


def __hash_api_key(api_key: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", api_key.encode("utf-8"), salt, 100000)


def hash_api_key(api_key: str) -> bytes:
    salt = os.urandom(32)
    key = __hash_api_key(api_key, salt)

    storage = salt + key

    return storage


def __get_salt_from_storage(storage: bytes) -> bytes:
    return storage[:32]


def __get_hashed_api_key_from_storage(storage: bytes) -> bytes:
    return storage[32:]


def verify_api_key(storage: str, api_key: str) -> bool:
    salt = __get_salt_from_storage(storage)
    hashed_api_key = __get_hashed_api_key_from_storage(storage)

    received_hashed_api_key = __hash_api_key(api_key, salt)

    return hashed_api_key == received_hashed_api_key
