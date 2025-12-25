import hashlib


def get_code_hash(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()


def verify_code(plain_code: str, hashed_code: str) -> bool:
    return get_code_hash(plain_code) == hashed_code
