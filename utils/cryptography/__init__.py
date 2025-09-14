import hmac
import hashlib
import settings


def hash_password(
    password: str,
    secret_key: bytes = settings.APP_SECRET_KEY
) -> str:
    key_bytes = secret_key.encode("utf-8")
    return hmac.new(key_bytes, password.encode("utf-8"), hashlib.sha256).hexdigest()


def verify_password(
    password: str,
    hashed_password: str,
    secret_key: str = settings.APP_SECRET_KEY
) -> bool:
    key_bytes = secret_key.encode("utf-8")
    return hmac.compare_digest(
        hmac.new(
            key_bytes, password.encode("utf-8"), hashlib.sha256()
        ).hexdigest(),
        hashed_password
    )